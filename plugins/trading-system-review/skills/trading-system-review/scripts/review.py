"""review.py: numbers (stats) and offline HTML report (render) for a trading-system review.

Usage:
  python review.py stats  --trades trades.csv --capital 10000 [--prices prices.csv]
                          [--variants variants.csv] [--live live.csv] [--live-capital 10000]
                          [--dd-limit 0.10] [--periods-per-year 252] [--recent-days 180]
                          [--sims 10000] [--seed 0] --out metrics.json
  python review.py render --metrics metrics.json --scorecard scorecard.json --out report.html [--open]

Inputs (CSV, or .parquet if pyarrow is installed):
  trades / live : entry_time, exit_time, side, pnl  (+ optional symbol, entry, exit, size, r_multiple)
                  side: long/short/buy/sell/1/-1 (case-insensitive); pnl net, account currency;
                  closed trades only; naive timestamps read as UTC, aware ones converted to UTC,
                  integer epoch seconds/ms accepted.
  prices        : time, high, low, close  (any bar size; resampled to daily; regimes use prior day only)
  variants      : date + one column of daily net returns (fractions) per parameter variant;
                  name the current-parameters column "base"; non-numeric columns are ignored
  scorecard     : {system, verdict, dimensions[{name, weight, gate, score 0-5, evidence}], ...optional}
All ratios in metrics.json are fractions. JSON is strict (NaN/inf -> null).
"""
import argparse
import datetime as dt
import html
import io
import itertools
import json
import math
import sys
import warnings
import webbrowser
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.dates as mdates  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from scipy import stats as st  # noqa: E402

warnings.filterwarnings("ignore")
plt.rcParams["svg.fonttype"] = "none"
plt.rcParams["text.parse_math"] = False  # untrusted labels: a "$" must not trigger mathtext

RUBRIC = [
    ("edge_thesis", 10, False), ("data_code_integrity", 15, True),
    ("statistical_significance", 12, False), ("overfitting_control", 12, True),
    ("robustness", 10, False), ("costs_execution", 8, False), ("risk_sizing", 10, False),
    ("live_tracking", 8, False), ("market_currency", 10, False), ("operations", 5, False),
]
VERDICTS = ["DEPLOY", "DEPLOY-REDUCED", "INCUBATE", "REVAMP", "RETIRE"]
VERDICT_RANK = {"DEPLOY": 3, "DEPLOY-REDUCED": 2, "INCUBATE": 1, "REVAMP": 0, "RETIRE": 0}
GAMMA = 0.5772156649015329


# ---------------------------------------------------------------- formulas
def _var_term(sr, skew, kurt):
    return 1 - skew * sr + (kurt - 1) / 4 * sr ** 2


def psr(sr, T, skew, kurt, sr_star=0.0):
    """Probabilistic Sharpe Ratio (raw kurtosis); None if the radicand is <= 0."""
    rad = _var_term(sr, skew, kurt)
    if T < 2 or not rad > 0:
        return None
    return float(st.norm.cdf((sr - sr_star) * math.sqrt(T - 1) / math.sqrt(rad)))


def min_trl(sr, skew, kurt, sr_star=0.0, alpha=0.05):
    """Minimum track-record length (periods); None if sr <= sr*."""
    if sr <= sr_star:
        return None
    z = st.norm.ppf(1 - alpha)
    return float(1 + _var_term(sr, skew, kurt) * (z / (sr - sr_star)) ** 2)


def expected_max_sr(V, N):
    """Expected maximum Sharpe of N unskilled trials with Sharpe variance V."""
    if N <= 1:
        return 0.0
    return float(math.sqrt(V) * ((1 - GAMMA) * st.norm.ppf(1 - 1 / N)
                                 + GAMMA * st.norm.ppf(1 - 1 / (N * math.e))))


def pbo_cscv(matrix, s=16):
    """Probability of backtest overfitting via CSCV on a T x N return matrix."""
    m = np.asarray(matrix, dtype=float)
    if m.ndim != 2 or m.shape[1] < 2:
        return None
    T, N = m.shape
    s = min(s, (T // 5) // 2 * 2)
    if s < 4:
        return None
    blocks = np.array_split(np.arange(T), s)
    cnt = np.array([len(b) for b in blocks], float)
    b1 = np.array([m[b].sum(0) for b in blocks])
    b2 = np.array([(m[b] ** 2).sum(0) for b in blocks])
    combos = np.array(list(itertools.combinations(range(s), s // 2)))
    mask = np.zeros((len(combos), s))
    np.put_along_axis(mask, combos, 1.0, axis=1)

    def sharpe(w):  # w: C x s block mask -> C x N per-column Sharpe
        n = w @ cnt
        s1, s2 = w @ b1, w @ b2
        mean = s1 / n[:, None]
        var = np.maximum((s2 - n[:, None] * mean ** 2) / (n[:, None] - 1), 0)
        sd = np.sqrt(var)
        return np.where(sd > 1e-12, mean / np.where(sd > 1e-12, sd, 1), 0.0)

    is_sr, oos_sr = sharpe(mask), sharpe(1 - mask)
    best = is_sr.argmax(1)
    rows = np.arange(len(combos))
    rank = st.rankdata(oos_sr, axis=1)[rows, best]
    w = rank / (N + 1)
    logit = np.log(w / (1 - w))
    return {"pbo": float(np.mean(logit <= 0)), "n_variants": N, "s": s, "n_combos": len(combos),
            "p_oos_loss": float(np.mean(oos_sr[rows, best] < 0)),
            "logit_median": float(np.median(logit))}


# ---------------------------------------------------------------- loading
def _read(path):
    p = Path(path)
    return pd.read_parquet(p) if p.suffix.lower() == ".parquet" else pd.read_csv(p)


def _side(v):
    k = str(v).strip().lower()
    if k in ("buy", "long", "1", "1.0", "+1"):
        return 1
    if k in ("sell", "short", "-1", "-1.0"):
        return -1
    raise SystemExit(f"unrecognised side value {v!r} (use long/short/buy/sell/1/-1)")


def normalize(df):
    """Validate a trades frame: UTC times, side as +-1, float pnl, sorted by exit_time."""
    for c in ("entry_time", "exit_time", "side", "pnl"):
        if c not in df.columns:
            raise SystemExit(f"trades file is missing required column: {c}")
    if df.empty:
        raise SystemExit("trades file has no rows")
    df = df.copy()
    for c in ("entry_time", "exit_time"):
        if pd.api.types.is_numeric_dtype(df[c]):  # epoch seconds / ms (e.g. MT5 exports)
            unit = "ms" if df[c].abs().max() > 1e11 else "s"
            df[c] = pd.to_datetime(df[c], unit=unit, utc=True)
        else:
            df[c] = pd.to_datetime(df[c], utc=True, format="mixed")
    bad = int(df[["entry_time", "exit_time"]].isna().any(axis=1).sum())
    if bad:
        raise SystemExit(f"{bad} trade(s) have an empty or unparseable entry_time/exit_time "
                         "(open trades?) - drop them first")
    if df["entry_time"].min().year < 1990:
        raise SystemExit("timestamps parse to before 1990 - check the time unit/format")
    df["side"] = df["side"].map(_side).astype(int)
    df["pnl"] = pd.to_numeric(df["pnl"]).astype(float)
    return df.sort_values("exit_time").reset_index(drop=True)


def load_trades(path):
    return normalize(_read(path))


def daily_pnl(trades, periods_per_year):
    """P&L per exit date; weekends roll to Monday when ppy < 365; gaps filled with 0."""
    biz = periods_per_year < 365

    def day(s):
        d = s.dt.tz_convert("UTC").dt.tz_localize(None).dt.normalize()
        return d.map(lambda x: x + pd.offsets.BDay(0)) if biz else d

    s = trades["pnl"].groupby(day(trades["exit_time"])).sum()
    first, last = day(trades["entry_time"]).min(), day(trades["exit_time"]).max()
    first = min(first, s.index.min())
    idx = pd.bdate_range(first, last) if biz else pd.date_range(first, last)
    return s.reindex(idx.union(s.index)).fillna(0.0).sort_index()


# ---------------------------------------------------------------- stats
def _div(a, b):
    if a is None or b is None or not np.isfinite(a) or not np.isfinite(b) or b == 0:
        return None
    return float(a / b)


def _pf(p):
    losses = -p[p < 0].sum()
    return float(p[p > 0].sum() / losses) if losses > 0 else None


def _basic(p):
    p = np.asarray(p, float)
    n = len(p)
    return {"n": n, "expectancy": float(p.mean()) if n else None,
            "win_rate": float((p > 0).mean()) if n else None, "profit_factor": _pf(p) if n else None}


def _welch(a, b):
    if len(a) < 2 or len(b) < 2:
        return None
    return float(st.ttest_ind(a, b, equal_var=False).pvalue)


def _equity(daily, capital, ppy):
    eq = capital + daily.cumsum()
    prev = eq.shift(1).fillna(capital)
    r = (daily / prev).replace([np.inf, -np.inf], np.nan).dropna()
    peak = np.maximum(eq.cummax(), capital)
    dd = (peak - eq) / peak
    # longest calendar span from a peak to recovery (or to the end)
    longest, pk, pk_date, last = 0, capital, eq.index[0], eq.index[-1]
    for d, v in eq.items():
        if v >= pk:
            longest = max(longest, (d - pk_date).days)
            pk, pk_date = v, d
    longest = max(longest, (last - pk_date).days)
    T = len(r)
    mean, sd = (r.mean(), r.std(ddof=1)) if T else (None, None)
    down = math.sqrt(np.mean(np.minimum(r, 0) ** 2)) if T else None
    end = float(eq.iloc[-1])
    cagr = (end / capital) ** (ppy / len(daily)) - 1 if end > 0 else -1.0
    max_dd = float(dd.max())
    out = {
        "series": [[d.strftime("%Y-%m-%d"), float(e), float(x)] for d, e, x in zip(eq.index, eq, dd)],
        "total_return": end / capital - 1, "cagr": cagr, "max_dd": max_dd,
        "max_dd_duration_days": int(longest), "calmar": _div(cagr, max_dd),
        "sharpe": _div(mean, sd) and _div(mean, sd) * math.sqrt(ppy),
        "sortino": _div(mean, down) and _div(mean, down) * math.sqrt(ppy),
    }
    return r, out


def _trade_stats(t):
    p = t["pnl"].to_numpy()
    n = len(p)
    wins, losses = p[p > 0], p[p < 0]
    mean = p.mean()
    sd = p.std(ddof=1) if n > 1 else None
    z = 1.96
    wr = len(wins) / n
    c = 1 + z * z / n
    centre = (wr + z * z / (2 * n)) / c
    half = z * math.sqrt(wr * (1 - wr) / n + z * z / (4 * n * n)) / c
    if sd:
        h = st.t.ppf(0.975, n - 1) * sd / math.sqrt(n)
        ci, tstat = [mean - h, mean + h], mean / (sd / math.sqrt(n))
        pval = float(2 * st.t.sf(abs(tstat), n - 1))
    else:
        ci, tstat, pval = None, None, None
    basis = "r_multiple" if "r_multiple" in t and t["r_multiple"].notna().any() else "pnl"
    x = t["r_multiple"].dropna().to_numpy(float) if basis == "r_multiple" else p
    xsd = x.std(ddof=1) if len(x) > 1 else None
    run = best = 0
    for v in p:
        run = run + 1 if v < 0 else 0
        best = max(best, run)
    avg_win = float(wins.mean()) if len(wins) else None
    avg_loss = float(-losses.mean()) if len(losses) else None
    return {
        "n": n, "win_rate": wr, "win_rate_ci95": [centre - half, centre + half],
        "avg_win": avg_win, "avg_loss": avg_loss, "payoff": _div(avg_win, avg_loss),
        "profit_factor": _pf(p), "expectancy": float(mean), "expectancy_ci95": ci,
        "t_stat": tstat, "p_value": pval, "total_pnl": float(p.sum()),
        "sqn": _div(x.mean(), xsd) and _div(x.mean(), xsd) * math.sqrt(min(len(x), 100)),
        "sqn_basis": basis, "max_consec_losses": best,
        "n_required": math.ceil(((1.96 + 0.8416) * sd / mean) ** 2) if sd and mean > 0 else None,
    }


def _deflation(r, variants):
    T = len(r)
    sd = r.std(ddof=1) if T > 1 else 0
    if T < 4 or not sd > 0:
        return {"T": T, "psr0": None, "min_trl_periods": None,
                "dsr": {"source": "null_grid", "rows": [], "note": "too few daily returns"}}
    sr = float(r.mean() / sd)
    sk, ku = float(st.skew(r)), float(st.kurtosis(r, fisher=False))
    out = {"sr_period": sr, "T": T, "skew": sk, "kurt": ku, "psr0": psr(sr, T, sk, ku),
           "min_trl_periods": min_trl(sr, sk, ku)}
    if variants is not None and variants.shape[1] >= 2:
        v_sr = variants.mean() / variants.std(ddof=1).replace(0, np.nan)
        V, N = float(v_sr.var(ddof=1)), variants.shape[1]
        sr0 = expected_max_sr(V, N)
        out["dsr"] = {"source": "variants", "n": N, "v": V, "sr0": sr0,
                      "dsr": psr(sr, T, sk, ku, sr0)}
    else:
        V = _var_term(sr, sk, ku) / (T - 1)
        rows = []
        for N in (1, 10, 50, 100, 500):
            s0 = expected_max_sr(V, N) if V > 0 else None
            rows.append({"n": N, "sr0": s0, "dsr": psr(sr, T, sk, ku, s0) if s0 is not None else None})
        out["dsr"] = {"source": "null_grid", "rows": rows,
                      "note": "no variants supplied: V assumes every trial has true Sharpe 0"}
    return out


def _max_dd_paths(paths, capital):
    eq = capital + np.cumsum(paths, axis=1)
    peak = np.maximum(np.maximum.accumulate(eq, axis=1), capital)
    return ((peak - eq) / peak).max(axis=1), eq[:, -1]


def _monte_carlo(pnl, capital, sims, seed, dd_limit):
    rng = np.random.default_rng(seed)
    n = len(pnl)
    dds = {"reshuffle": [], "bootstrap": []}
    fin = []
    step = max(1, min(1000, 2_000_000 // max(n, 1)))  # cap each chunk at ~2M cells (~16 MB)
    for done in range(0, sims, step):
        k = min(step, sims - done)
        d, _ = _max_dd_paths(rng.permuted(np.tile(pnl, (k, 1)), axis=1), capital)
        dds["reshuffle"].append(d)
        d, f = _max_dd_paths(pnl[rng.integers(0, n, (k, n))], capital)
        dds["bootstrap"].append(d)
        fin.append(f)
    out = {"sims": sims, "dd_limit": dd_limit}
    for name in dds:
        d = np.concatenate(dds[name])
        p50, p95, p99 = np.percentile(d, [50, 95, 99])
        out[name] = {"max_dd": {"p50": p50, "p95": p95, "p99": p99},
                     "p_breach": float((d >= dd_limit).mean())}
        if name == "reshuffle":
            counts, edges = np.histogram(d, bins=40, range=(0.0, max(float(d.max()), 1e-9)))
            out[name]["hist"] = {"counts": counts, "edges": edges}
    f = np.concatenate(fin) / capital - 1
    p5, p50, p95 = np.percentile(f, [5, 50, 95])
    out["bootstrap"]["final_return"] = {"p5": p5, "p50": p50, "p95": p95}
    out["bootstrap"]["p_loss"] = float((f < 0).mean())
    return out


def _regimes(prices_path, trades):
    """Label each trade with the previous day's vol/trend regime."""
    px = _read(prices_path)
    px["time"] = pd.to_datetime(px["time"], utc=True, format="mixed")
    px = px.sort_values("time").set_index("time")[["high", "low", "close"]].astype(float)
    if px.index.to_series().diff().median() < pd.Timedelta(days=1):
        px = px.resample("1D").agg({"high": "max", "low": "min", "close": "last"}).dropna()
    c = px["close"]
    tr = pd.concat([px["high"] - px["low"], (px["high"] - c.shift()).abs(),
                    (px["low"] - c.shift()).abs()], axis=1).max(axis=1)
    natr = tr.rolling(14).mean() / c
    rank = natr.expanding(min_periods=20).rank(pct=True)
    vol = pd.cut(rank, [0, 1 / 3, 2 / 3, 1], labels=["low", "mid", "high"], include_lowest=True)
    er = (c - c.shift(20)).abs() / c.diff().abs().rolling(20).sum()
    trend = pd.Series(np.where(er > 0.3, "trend", "range"), index=px.index).where(er.notna())
    label = (vol.astype(object) + "-vol " + trend).shift(1)
    lab = pd.DataFrame({"time": px.index.astype("datetime64[ns, UTC]"), "regime": label.to_numpy()})
    left = trades[["entry_time"]].reset_index().sort_values("entry_time")
    left["entry_time"] = left["entry_time"].astype("datetime64[ns, UTC]")
    m = pd.merge_asof(left, lab, left_on="entry_time", right_on="time").set_index("index")["regime"]
    return m.reindex(trades.index).fillna("unknown")


def _breakdown(t, key):
    rows = []
    for k, g in t.groupby(key):
        b = _basic(g["pnl"])
        rows.append({"key": k.item() if hasattr(k, "item") else k, "n": b["n"],
                     "win_rate": b["win_rate"], "expectancy": b["expectancy"],
                     "profit_factor": b["profit_factor"], "total_pnl": float(g["pnl"].sum()),
                     "low_n": b["n"] < 30})
    return rows


def _recency(t, recent_days):
    cut = t["exit_time"].max() - pd.Timedelta(days=recent_days)
    rec, pri = t[t["exit_time"] > cut]["pnl"].to_numpy(), t[t["exit_time"] <= cut]["pnl"].to_numpy()
    k = int(len(t) * 0.7)
    a, b = t["pnl"].to_numpy()[:k], t["pnl"].to_numpy()[k:]
    return {"recent_days": recent_days,
            "recent": _basic(rec), "prior": _basic(pri), "welch_p": _welch(rec, pri),
            "split_70_30": {"first": _basic(a), "last": _basic(b), "welch_p": _welch(a, b)}}


def _live(live, bt, capital, sims, seed):
    p, pb = live["pnl"].to_numpy(), bt["pnl"].to_numpy()
    n, nb = len(p), len(pb)
    eq = capital + np.cumsum(p)
    peak = np.maximum(np.maximum.accumulate(eq), capital)
    max_dd = float(((peak - eq) / peak).max())
    # Length-matched DD band: n-trade paths bootstrapped from the backtest trades.
    rng = np.random.default_rng(seed)
    step = max(1, min(1000, 2_000_000 // max(n, 1)))
    dds = np.concatenate([_max_dd_paths(pb[rng.integers(0, nb, (min(step, sims - i), n))], capital)[0]
                          for i in range(0, sims, step)])
    p95, p99 = np.percentile(dds, [95, 99])
    dd_vs = "above_p99" if max_dd > p99 else "above_p95" if max_dd > p95 else "within"
    b = _basic(p)
    # Band where an n-trade live mean lands if the edge is unchanged (difference-of-means).
    inside = None
    if nb > 1:
        h = st.t.ppf(0.975, nb - 1) * pb.std(ddof=1) * math.sqrt(1 / n + 1 / nb)
        inside = bool(abs(b["expectancy"] - pb.mean()) <= h)
    mw = float(st.mannwhitneyu(p, pb).pvalue) if n > 1 else None
    ks = float(st.ks_2samp(p, pb).pvalue) if n > 1 else None
    if n < 50:
        hint = "inconclusive (<50 live trades)"
    elif inside is False or dd_vs != "within":
        hint = "decay_suspected"
    else:
        hint = "consistent"
    return {**b, "max_dd": max_dd, "capital": capital, "dd_band": {"p95": p95, "p99": p99},
            "welch_p": _welch(p, pb), "mannwhitney_p": mw, "ks_p": ks,
            "expectancy_in_band95": inside, "dd_vs_mc": dd_vs, "hint": hint}


def _variant_summary(v, ppy):
    """Annualised Sharpe per variant + plateau measures (column 'base' = current parameters)."""
    sr = v.mean() / v.std(ddof=1).replace(0, np.nan) * math.sqrt(ppy)
    best = float(sr.max())
    return {"sharpe": {str(k): x for k, x in sr.items()}, "best": best, "median": float(sr.median()),
            "share_within_30pct": float((sr >= 0.7 * best).mean()) if best > 0 else None,
            "base_vs_best": _div(float(sr["base"]), best) if "base" in sr and best > 0 else None}


def _clean(o):
    """Recursively make JSON-safe: NaN/inf -> None, numpy/pandas -> python."""
    if isinstance(o, dict):
        return {str(k): _clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple, np.ndarray)):
        return [_clean(v) for v in o]
    if isinstance(o, (np.bool_, bool)):
        return bool(o)
    if isinstance(o, (np.integer, int)):
        return int(o)
    if isinstance(o, (np.floating, float)):
        return float(o) if np.isfinite(o) else None
    if isinstance(o, (pd.Timestamp, dt.datetime, dt.date)):
        return o.isoformat()
    return o


def run_stats(a):
    t = load_trades(a.trades)
    n = len(t)
    daily = daily_pnl(t, a.periods_per_year)
    r, eqm = _equity(daily, a.capital, a.periods_per_year)
    variants, dropped = None, []
    if a.variants:
        v = _read(a.variants)
        num = v.apply(pd.to_numeric, errors="coerce")
        dropped = [c for c in v.columns if str(c).lower() in ("date", "time", "datetime", "timestamp")
                   or num[c].notna().mean() < 0.9]
        variants = num.drop(columns=dropped).dropna()
        if variants.shape[1] < 2 or len(variants) < 20:
            raise SystemExit(f"variants file needs >= 2 numeric return columns and >= 20 complete rows "
                             f"(got {variants.shape[1]} columns, {len(variants)} rows; dropped {dropped})")
    ts = _trade_stats(t)
    mc = _monte_carlo(t["pnl"].to_numpy(), a.capital, a.sims, a.seed, a.dd_limit)
    t["regime"] = _regimes(a.prices, t) if a.prices else None
    t["year"], t["hour"] = t["exit_time"].dt.year, t["entry_time"].dt.hour
    t["side_name"] = np.where(t["side"] > 0, "long", "short")
    bd = {"by_year": _breakdown(t, "year"), "by_side": _breakdown(t, "side_name"),
          "by_hour": _breakdown(t, "hour"),
          "by_regime": _breakdown(t, "regime") if a.prices else []}
    w = max(10, min(50, n // 4))
    roll = t["pnl"].rolling(w).mean()
    keep = roll.notna()
    trip = []
    for name, val, thr, hit in [
        ("Sharpe > 3", eqm["sharpe"], 3, lambda v: v > 3),
        ("max drawdown < 5%", eqm["max_dd"], 0.05, lambda v: v < 0.05),
        ("profit factor > 4", ts["profit_factor"], 4, lambda v: v > 4),
        ("win rate > 80%", ts["win_rate"], 0.8, lambda v: v > 0.8),
        ("fewer than 100 trades", n, 100, lambda v: v < 100)]:
        trip.append({"name": name, "value": val, "threshold": thr,
                     "hit": val is not None and bool(hit(val))})
    hits = sum(i["hit"] for i in trip)
    warns = []
    if n < 30:
        warns.append(f"only {n} trades — statistics unreliable (<30 trades)")
    if n < 100:
        warns.append("fewer than 100 trades")
    if not a.prices:
        warns.append("no prices file: regime breakdown skipped")
    if variants is None:
        warns.append("no variants file: PBO not computed; DSR uses the null grid")
    elif dropped:
        warns.append(f"variants file: non-return columns ignored: {', '.join(map(str, dropped))}")
    if not a.live:
        warns.append("no live file: decay not tested")
    out = {
        "meta": {"generated_at": dt.datetime.now(dt.timezone.utc).isoformat(), "capital": a.capital,
                 "periods_per_year": a.periods_per_year, "first_entry": t["entry_time"].min(),
                 "last_exit": t["exit_time"].max(),
                 "inputs": {"trades": a.trades, "prices": a.prices, "variants": a.variants,
                            "live": a.live}},
        "trade_stats": ts, "equity": eqm, "deflation": _deflation(r, variants),
        "monte_carlo": mc, "breakdown": bd, "recency": _recency(t, a.recent_days),
        "rolling": {"window": w, "values": [[e.isoformat(), v] for e, v in
                                            zip(t["exit_time"][keep], roll[keep])]},
        "tripwires": {"items": trip, "hits": hits, "curve_fit_suspect": hits >= 3},
        "warnings": warns,
        "pbo": pbo_cscv(variants.to_numpy()) if variants is not None else None,
        "variants": _variant_summary(variants, a.periods_per_year) if variants is not None else None,
    }
    if a.live:
        out["live"] = _live(load_trades(a.live), t, a.live_capital or a.capital, a.sims, a.seed)
    Path(a.out).write_text(json.dumps(_clean(out), allow_nan=False, indent=1), encoding="utf-8")
    print(f"wrote {a.out} ({n} trades)")


# ---------------------------------------------------------------- render
# Light palette from the dataviz reference: blue = main series, orange = loss/limit.
BLUE, ORANGE, INK, INK2, GRID, SURF = "#2a78d6", "#eb6834", "#0b0b0b", "#52514e", "#e4e3de", "#fcfcfb"

CSS = f"""
:root{{--surface:{SURF};--ink:{INK};--ink2:{INK2};--grid:{GRID};--blue:{BLUE};--orange:{ORANGE}}}
body{{margin:0;background:#f3f2ee;color:var(--ink);font:15px/1.5 system-ui,-apple-system,"Segoe UI",Roboto,Arial,sans-serif}}
main{{max-width:980px;margin:0 auto;padding:24px 16px 64px}}
section{{background:var(--surface);border:1px solid var(--grid);border-radius:8px;padding:16px 20px;margin:16px 0}}
h1{{margin:0 0 4px;font-size:26px}}h2{{margin:0 0 10px;font-size:18px}}
.muted{{color:var(--ink2)}}.big{{font-size:44px;font-weight:700;line-height:1.1}}
.badge{{display:inline-block;padding:2px 10px;border-radius:12px;border:1px solid var(--ink2);font-size:13px;font-weight:600}}
table{{border-collapse:collapse;width:100%;font-size:14px}}
th,td{{text-align:left;padding:5px 8px;border-bottom:1px solid var(--grid);vertical-align:top}}
th{{color:var(--ink2);font-weight:600}}.n{{text-align:right;font-variant-numeric:tabular-nums}}
.warn{{border-left:4px solid var(--orange);padding:6px 12px;margin:8px 0;background:#fdf1ec}}
svg{{max-width:100%;height:auto;display:block;margin:8px 0}}
"""


def _e(x):
    return "" if x is None else html.escape(str(x), quote=True)


def _num(x, d=2):
    return "n/a" if x is None else f"{x:,.{d}f}"


def _pct(x, d=1):
    return "n/a" if x is None else f"{x * 100:.{d}f}%"


def _link(title, url):
    u = str(url or "").strip()
    if u.lower().startswith(("http://", "https://")):
        return f'<a href="{_e(u)}" rel="noopener noreferrer">{_e(title or u)}</a>'
    return _e(title or u)


def _table(head, rows, num_from=1, num_to=99):
    """Columns num_from <= i < num_to are numeric (right-aligned, header included)."""
    isnum = lambda i: num_from <= i < num_to  # noqa: E731
    h = "".join(f'<th class="n">{_e(c)}</th>' if isnum(i) else f"<th>{_e(c)}</th>"
                for i, c in enumerate(head))
    body = "".join("<tr>" + "".join(
        f'<td class="n">{c}</td>' if isnum(i) and not raw else f"<td>{c}</td>"
        for i, (c, raw) in enumerate(r)) + "</tr>" for r in rows)
    return f"<table><tr>{h}</tr>{body}</table>"


def _tbl(head, rows, num_from=1, num_to=99):
    return _table(head, [[(_e(c), False) for c in r] for r in rows], num_from, num_to)


def _svg(fig):
    buf = io.StringIO()
    fig.savefig(buf, format="svg", metadata={"Date": None})
    plt.close(fig)
    s = buf.getvalue()
    return s[s.index("<svg"):]


def _ax_style(ax, title):
    ax.set_facecolor(SURF)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    for sp in ("left", "bottom"):
        ax.spines[sp].set_color(INK2)
    ax.grid(axis="y", color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    ax.tick_params(colors=INK2, labelsize=9)
    ax.set_title(title, loc="left", fontsize=11, color=INK)


def _fig(rows=1, ratios=None, h=3.2):
    fig, axes = plt.subplots(rows, 1, figsize=(9, h), sharex=rows > 1,
                             gridspec_kw={"height_ratios": ratios} if ratios else None)
    fig.patch.set_facecolor(SURF)
    fig.subplots_adjust(left=0.09, right=0.97, top=0.9, bottom=0.12)
    return fig, axes


def _dates(ax):
    loc = mdates.AutoDateLocator()
    ax.xaxis.set_major_locator(loc)
    ax.xaxis.set_major_formatter(mdates.ConciseDateFormatter(loc))


def chart_equity(m):
    s = m["equity"]["series"]
    if not s:
        return ""
    x = pd.to_datetime([r[0] for r in s])
    fig, (a1, a2) = _fig(2, [3, 1], 4.2)
    _ax_style(a1, "Equity (account currency)")
    a1.plot(x, [r[1] for r in s], color=BLUE, linewidth=2)
    a1.annotate(f"{s[-1][1]:,.0f}", (x[-1], s[-1][1]), xytext=(-4, 6), textcoords="offset points",
                ha="right", fontsize=9, color=INK)
    _ax_style(a2, "Drawdown")
    dd = [-r[2] * 100 for r in s]
    a2.fill_between(x, dd, 0, color=ORANGE, alpha=0.35, linewidth=0)
    a2.plot(x, dd, color=ORANGE, linewidth=1.5)
    a2.set_ylabel("%", color=INK2, fontsize=9)
    i = int(np.argmin(dd))
    right = i > len(dd) / 2
    a2.annotate(f"max {m['equity']['max_dd'] * 100:.1f}%", (x[i], dd[i]), xytext=(-6 if right else 6, 2),
                textcoords="offset points", ha="right" if right else "left", fontsize=9, color=INK)
    _dates(a2)
    return _svg(fig)


def chart_rolling(m):
    v = m["rolling"]["values"]
    if not v:
        return ""
    fig, ax = _fig()
    _ax_style(ax, f"Rolling expectancy per trade (window {m['rolling']['window']} trades)")
    x = pd.to_datetime([r[0] for r in v])
    ax.axhline(0, color=INK2, linewidth=1)
    ax.plot(x, [r[1] for r in v], color=BLUE, linewidth=2)
    _dates(ax)
    return _svg(fig)


def chart_mc(m):
    mc = m["monte_carlo"]
    h = mc["reshuffle"]["hist"]
    edges = np.array(h["edges"]) * 100
    fig, ax = _fig()
    _ax_style(ax, "Monte Carlo max drawdown (reshuffled trade order)")
    ax.bar(edges[:-1], h["counts"], width=np.diff(edges), align="edge", color=BLUE,
           edgecolor=SURF, linewidth=0.6)
    top = max(h["counts"]) or 1
    ax.axvline(mc["dd_limit"] * 100, color=ORANGE, linewidth=2)
    ax.text(mc["dd_limit"] * 100, top, f" limit {mc['dd_limit'] * 100:.0f}%", color=INK, fontsize=9, va="top")
    real = m["equity"]["max_dd"] * 100
    ax.axvline(real, color=INK, linewidth=1.5, linestyle="--")
    ax.text(real, top * 0.8, f" realised {real:.1f}%", color=INK, fontsize=9, va="top")
    ax.set_xlabel("max drawdown (%)", color=INK2, fontsize=9)
    ax.set_ylabel("simulations", color=INK2, fontsize=9)
    return _svg(fig)


def chart_year(m):
    rows = m["breakdown"]["by_year"]
    if not rows:
        return ""
    fig, ax = _fig()
    _ax_style(ax, "P&L by exit year")
    xs = [str(r["key"]) for r in rows]
    ys = [r["total_pnl"] for r in rows]
    bars = ax.bar(xs, ys, color=[BLUE if y >= 0 else ORANGE for y in ys], width=0.6)
    ax.axhline(0, color=INK2, linewidth=1)
    for b, y, r in zip(bars, ys, rows):
        lab = f"{y:,.0f}" + ("*" if r["low_n"] else "")
        ax.annotate(lab, (b.get_x() + b.get_width() / 2, y), xytext=(0, 4 if y >= 0 else -12),
                    textcoords="offset points", ha="center", fontsize=9, color=INK)
    if any(r["low_n"] for r in rows):
        ax.set_xlabel("* fewer than 30 trades", color=INK2, fontsize=9)
    return _svg(fig)


def chart_scores(dims):
    fig, ax = _fig(h=0.45 * len(dims) + 1)
    _ax_style(ax, "Weighted score by dimension (points earned / weight)")
    ax.grid(axis="y", visible=False)
    ys = list(range(len(dims)))[::-1]
    for y, d in zip(ys, dims):
        ax.barh(y, d["weight"], color=GRID, height=0.6)
        ax.barh(y, d["weight"] * d["score"] / 5, color=BLUE, height=0.6)
        ax.text(d["weight"] + 0.2, y, f"{d['weight'] * d['score'] / 5:.1f}/{d['weight']:g}",
                va="center", fontsize=9, color=INK)
    ax.set_yticks(ys)
    ax.set_yticklabels([d["name"] + (" (gate)" if d["gate"] else "") for d in dims], fontsize=9)
    ax.set_xlim(0, max(d["weight"] for d in dims) + 3)
    fig.subplots_adjust(left=0.3)
    return _svg(fig)


def _isnum(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(x)


def _validate(sc):
    miss = [k for k in ("system", "verdict", "dimensions") if k not in sc]
    if miss:
        raise SystemExit(f"scorecard missing required key(s): {', '.join(miss)}")
    if sc["verdict"] not in VERDICTS:
        raise SystemExit(f"scorecard verdict {sc['verdict']!r} invalid; use one of {', '.join(VERDICTS)}")
    if not isinstance(sc["dimensions"], list):
        raise SystemExit("scorecard dimensions must be a list")
    rub = {n: (w, g) for n, w, g in RUBRIC}
    dims = []
    for d in sc["dimensions"]:
        if not isinstance(d, dict) or not _isnum(d.get("score")) or not 0 <= d["score"] <= 5:
            raise SystemExit(f"scorecard dimension score must be a number 0-5: {d!r}")
        name = str(d.get("name", ""))
        w = d["weight"] if _isnum(d.get("weight")) else rub.get(name, (0, False))[0]
        g = bool(d.get("gate", rub.get(name, (0, False))[1]))
        dims.append({"name": name, "weight": w, "gate": g, "score": d["score"],
                     "evidence": d.get("evidence", "")})
    return dims


def _items(x):
    if not x:
        return "<p>Not provided.</p>"
    li = []
    for i in x:
        if isinstance(i, dict):
            i = "; ".join(f"{k}: {v}" for k, v in i.items())
        li.append(f"<li>{_e(i)}</li>")
    return "<ul>" + "".join(li) + "</ul>"


def build_html(m, sc):
    dims = _validate(sc)
    overall = sum(d["weight"] * d["score"] / 5 for d in dims)
    warns = []
    band = 3 if overall >= 85 else 2 if overall >= 70 else 1 if overall >= 50 else 0
    gated = [d["name"] for d in dims if d["gate"] and d["score"] <= 1]
    allowed = 0 if gated else band
    if VERDICT_RANK[sc["verdict"]] > allowed:
        why = f"gate dimension(s) {', '.join(gated)} scored <= 1" if gated else f"score {overall:.1f} is below the band"
        warns.append(f"Verdict {sc['verdict']} contradicts the rubric: {why}.")
    if sorted((d["name"], d["weight"]) for d in dims) != sorted((n, w) for n, w, _ in RUBRIC):
        warns.append("Scorecard dimension names or weights differ from the canonical rubric.")
    mdl = sc.get("model") or {}
    ind = sc.get("independence") or {}
    clean = ind.get("clean") is True
    ts, eq = m["trade_stats"], m["equity"]
    dsr, tw = m["deflation"], m["tripwires"]
    S = []

    def sec(title, body):
        S.append(f"<section><h2>{_e(title)}</h2>{body}</section>")

    S.append(f"""<section><h1>{_e(sc['system'])}</h1>
<div class="muted">Review date {_e(sc.get('review_date'))} &middot; model {_e(mdl.get('name'))}
(knowledge cutoff {_e(mdl.get('knowledge_cutoff'))}) &middot;
<span class="badge">{'Independent review (clean)' if clean else 'Independence not guaranteed'}</span></div>
{f'<p class="muted">{_e(sc.get("repo"))}</p>' if sc.get('repo') else ''}</section>""")
    sec("Verdict and score", f'<div class="big">{_e(sc["verdict"])} &middot; {overall:.1f}/100</div>'
        + "".join(f'<div class="warn">{_e(w)}</div>' for w in warns)
        + f'<p>{_e(sc.get("summary")) or "Not provided."}</p>'
        + (f'<p class="muted">Edge thesis: {_e(sc["edge_thesis"])}</p>' if sc.get("edge_thesis") else ""))
    sec("Scorecard", _tbl(["Dimension", "Weight", "Gate", "Score (0-5)", "Evidence"],
                          [[d["name"], f"{d['weight']:g}", "yes" if d["gate"] else "", f"{d['score']:g}",
                            d["evidence"]] for d in dims], 1, 4) + (chart_scores(dims) if dims else ""))
    trip = _tbl(["Tripwire", "Value", "Threshold", "Hit"],
                [[i["name"], _num(i["value"], 3), i["threshold"], "HIT" if i["hit"] else "no"]
                 for i in tw["items"]], 1, 3)
    flag = f'<div class="warn">{tw["hits"]} tripwires hit: curve-fit suspected.</div>' if tw["curve_fit_suspect"] else ""
    ci = ts["expectancy_ci95"]
    stats_rows = [
        ["Trades", ts["n"]], ["Win rate", f"{_pct(ts['win_rate'])} (95% CI {_pct(ts['win_rate_ci95'][0])} to {_pct(ts['win_rate_ci95'][1])})"],
        ["Expectancy / trade", f"{_num(ts['expectancy'])}" + (f" (95% CI {_num(ci[0])} to {_num(ci[1])})" if ci else "")],
        ["Profit factor", _num(ts["profit_factor"]) if ts["profit_factor"] is not None else "n/a (no losers)"],
        ["Payoff", _num(ts["payoff"])], ["t-stat (p)", f"{_num(ts['t_stat'])} ({_num(ts['p_value'], 4)})"],
        [f"SQN ({ts['sqn_basis']})", _num(ts["sqn"])], ["Trades needed (80% power)", ts["n_required"] or "n/a"],
        ["Sharpe", _num(eq["sharpe"])], ["Sortino", _num(eq["sortino"])], ["CAGR", _pct(eq["cagr"])],
        ["Total return", _pct(eq["total_return"])], ["Max drawdown", _pct(eq["max_dd"])],
        ["Max DD duration (days)", eq["max_dd_duration_days"]], ["Calmar", _num(eq["calmar"])],
        ["Max consecutive losses", ts["max_consec_losses"]],
    ]
    sec("Tripwires and key statistics", flag + trip + "<br>" + _tbl(["Statistic", "Value"], stats_rows, 9)
        + "".join(f'<div class="warn">{_e(w)}</div>' for w in m["warnings"]))
    of = sc.get("overfitting") or {}
    d = dsr["dsr"]
    if d["source"] == "variants":
        dtab = _tbl(["N variants", "V", "SR0", "DSR"], [[d["n"], _num(d["v"], 6), _num(d["sr0"], 4), _num(d["dsr"], 4)]], 0)
    else:
        dtab = _tbl(["N trials", "SR0 (per period)", "DSR"], [[r["n"], _num(r["sr0"], 4), _num(r["dsr"], 4)] for r in d["rows"]], 0) \
            + f'<p class="muted">{_e(d.get("note"))}</p>'
    pbo = m.get("pbo")
    sec("Overfitting", f'<p><b>{_e(of.get("verdict")) or "Not provided."}</b> {_e(of.get("why"))}</p>'
        + f'<p>PSR vs 0: {_num(dsr.get("psr0"), 4)} &middot; min track record: {_num(dsr.get("min_trl_periods"), 0)} periods</p>'
        + dtab + ("<p>PBO not computed (no variants).</p>" if not pbo else
                  f'<p>PBO {_num(pbo["pbo"], 3)} over {pbo["n_variants"]} variants, {pbo["n_combos"]} CSCV combos '
                  f'(s={pbo["s"]}); P(OOS loss of IS-best) {_num(pbo["p_oos_loss"], 3)}.</p>'))
    mc = m["monte_carlo"]
    charts = "".join([chart_equity(m), chart_rolling(m), chart_mc(m), chart_year(m)])
    sec("Charts", charts + _tbl(["Monte Carlo", "DD p50", "DD p95", "DD p99", "P(DD >= limit)"],
        [[k, _pct(mc[k]["max_dd"]["p50"]), _pct(mc[k]["max_dd"]["p95"]), _pct(mc[k]["max_dd"]["p99"]),
          _pct(mc[k]["p_breach"])] for k in ("reshuffle", "bootstrap")], 1)
        + f'<p class="muted">Bootstrap: P(final < capital) {_pct(mc["bootstrap"]["p_loss"])}; final return p5/p50/p95 '
          f'{_pct(mc["bootstrap"]["final_return"]["p5"])} / {_pct(mc["bootstrap"]["final_return"]["p50"])} / '
          f'{_pct(mc["bootstrap"]["final_return"]["p95"])}.</p>')
    bd = ""
    for k, title in (("by_year", "By exit year"), ("by_side", "By side"), ("by_hour", "By entry hour (UTC)"),
                     ("by_regime", "By regime (prior day)")):
        rows = m["breakdown"][k]
        bd += f"<h3>{_e(title)}</h3>" + (_tbl(["Key", "N", "Win rate", "Expectancy", "Profit factor", "Total P&L", ""],
              [[r["key"], r["n"], _pct(r["win_rate"]), _num(r["expectancy"]), _num(r["profit_factor"]),
                _num(r["total_pnl"], 0), "low n" if r["low_n"] else ""] for r in rows], 1, 6) if rows else "<p>Not provided.</p>")
    sec("Breakdowns", bd)
    rc = m["recency"]
    rrow = lambda lab, b: [lab, b["n"], _num(b["expectancy"]), _pct(b["win_rate"]), _num(b["profit_factor"])]  # noqa: E731
    live = m.get("live")
    lv = "<p>Not provided.</p>" if not live else (
        _tbl(["Live n", "Expectancy", "Win rate", "PF", "Max DD", "DD vs band", "In expected band", "Welch p", "MW p", "KS p"],
             [[live["n"], _num(live["expectancy"]), _pct(live["win_rate"]), _num(live["profit_factor"]),
               _pct(live["max_dd"]), live["dd_vs_mc"], live["expectancy_in_band95"],
               _num(live["welch_p"], 3), _num(live["mannwhitney_p"], 3), _num(live["ks_p"], 3)]], 0)
        + f'<p><b>{_e(live["hint"])}</b></p><p class="muted">DD band = p95/p99 max drawdown of '
          f'{live["n"]}-trade paths bootstrapped from the backtest ({_pct(live["dd_band"]["p95"])} / '
          f'{_pct(live["dd_band"]["p99"])}) on capital {_num(live["capital"], 0)}. Expected band = where a '
          f'{live["n"]}-trade mean should land if the edge is unchanged.</p>')
    sec("Recency and live", _tbl(["Slice", "N", "Expectancy", "Win rate", "PF"], [
        rrow(f"last {rc['recent_days']} days", rc["recent"]), rrow("prior", rc["prior"]),
        rrow("first 70%", rc["split_70_30"]["first"]), rrow("last 30%", rc["split_70_30"]["last"])])
        + f'<p class="muted">Welch p recent vs prior {_num(rc["welch_p"], 3)}; 70/30 {_num(rc["split_70_30"]["welch_p"], 3)}</p>'
        + "<h3>Live vs backtest</h3>" + lv)
    f = sc.get("findings") or []
    sec("Code findings", _tbl(["Severity", "Location", "Finding", "Fix"],
        [[x.get("severity"), x.get("location"), x.get("finding"), x.get("fix")] for x in f], 0, 0) if f else "<p>Not provided.</p>")
    sec("What is outdated", _items(sc.get("outdated")))
    sec("New features", _items(sc.get("new_features")))
    sec("Revamp plan", _items(sc.get("revamp_plan")))
    src = sc.get("sources") or []
    sec("Sources", _table(["Source", "Tier", "Published", "Retrieved"],
        [[(_link(s.get("title"), s.get("url")), True), (_e(s.get("tier")), False), (_e(s.get("published")), False),
          (_e(s.get("retrieved")), False)] for s in src], 0, 0) if src else "<p>Not provided.</p>")
    sec("Independence and limitations",
        f'<p>{_e(ind.get("notes")) or "Not provided."}</p>' + _items(sc.get("limitations")))
    return (f'<!doctype html><html lang="en"><head><meta charset="utf-8">'
            f'<meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{_e(sc["system"])} - trading system review</title><style>{CSS}</style></head>'
            f'<body><main>{"".join(S)}</main></body></html>')


def run_render(a):
    m = json.loads(Path(a.metrics).read_text(encoding="utf-8"))
    sc = json.loads(Path(a.scorecard).read_text(encoding="utf-8"))
    out = Path(a.out)
    out.write_text(build_html(m, sc), encoding="utf-8")
    print(f"wrote {out}")
    if a.open:
        webbrowser.open(out.resolve().as_uri())


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("stats")
    s.add_argument("--trades", required=True)
    s.add_argument("--capital", type=float, required=True)
    s.add_argument("--prices")
    s.add_argument("--variants")
    s.add_argument("--live")
    s.add_argument("--live-capital", type=float, help="live account size (default: --capital)")
    s.add_argument("--dd-limit", type=float, default=0.10)
    s.add_argument("--periods-per-year", type=int, default=252)
    s.add_argument("--recent-days", type=int, default=180)
    s.add_argument("--sims", type=int, default=10000)
    s.add_argument("--seed", type=int, default=0)
    s.add_argument("--out", required=True)
    r = sub.add_parser("render")
    r.add_argument("--metrics", required=True)
    r.add_argument("--scorecard", required=True)
    r.add_argument("--out", required=True)
    r.add_argument("--open", action="store_true")
    a = ap.parse_args(argv)
    (run_stats if a.cmd == "stats" else run_render)(a)


if __name__ == "__main__":
    main(sys.argv[1:])
