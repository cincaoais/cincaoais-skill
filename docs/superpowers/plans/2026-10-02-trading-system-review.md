# trading-system-review Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a `trading-system-review` plugin to the cincaoais-skill marketplace that rates an existing trading system like a senior trader and emits an offline HTML report with charts.

**Architecture:** SKILL.md orchestrates (model `best`). It hands delegation to the `orchestrate` skill. One script, `review.py`, does all the numbers (`stats`) and the report (`render`). Two references hold the rubric and the web-search playbook.

**Tech Stack:** Python 3.13, numpy, pandas, scipy, matplotlib (SVG), pytest. All are already installed; there are no new dependencies.

**Spec:** `docs/superpowers/specs/2026-10-02-trading-system-review-design.md`

## Global Constraints

- Plugin root: `plugins/trading-system-review/`. Skill dir: `plugins/trading-system-review/skills/trading-system-review/`.
- No dependencies beyond numpy, pandas, scipy, matplotlib (pyarrow is optional, only for reading parquet).
- Every ratio in `metrics.json` is a fraction (0.12 means 12%). JSON is strict: NaN and ±inf become `null` (`json.dump(..., allow_nan=False)`).
- Every string in `report.html` is `html.escape`d. Only `http://` and `https://` URLs become links.
- Ponytail "full": one script file, one test file, no classes unless needed, no config files.
- Files end with LF (enforced by `.gitattributes`).
- Rubric (canonical, in `review.py` as `RUBRIC`; mirrored in `references/rubric.md`):
  `edge_thesis 10`, `data_code_integrity 15 (gate)`, `statistical_significance 12`, `overfitting_control 12 (gate)`, `robustness 10`, `costs_execution 8`, `risk_sizing 10`, `live_tracking 8`, `market_currency 10`, `operations 5`. Sum = 100.
- Verdicts, from most to least aggressive: `DEPLOY` ≥85, `DEPLOY-REDUCED` 70–84.9, `INCUBATE` 50–69.9, then `REVAMP` / `RETIRE` below 50. If any gate dimension scores ≤1, only `REVAMP` or `RETIRE` is allowed.

## Review Focus

1. Trade exits on weekends when `--periods-per-year 252` must not drop P&L. They roll forward to Monday.
2. Mixed naive and tz-aware timestamps in one CSV must all parse to UTC.
3. A profit factor of ∞ (no losers) and n < 5 must not crash or emit invalid JSON.
4. Untrusted text in `scorecard.json` must be escaped. That includes web-sourced findings and `javascript:` URLs.
5. Intraday price files (M1/H1) must be resampled to daily before computing regimes. Regimes use the previous day only (no look-ahead).

All five are pinned by tests in Task 1.

---

### Task 1: `review.py` (stats + render) with tests

**Files:**
- Create: `plugins/trading-system-review/skills/trading-system-review/scripts/review.py`
- Create: `plugins/trading-system-review/skills/trading-system-review/scripts/test_review.py`

**Interfaces (Produces):**
- `psr(sr, T, skew, kurt, sr_star=0.0) -> float | None`: `Φ((sr−sr*)·√(T−1) / √(1 − skew·sr + (kurt−1)/4·sr²))`. Uses raw (non-excess) kurtosis. Returns None if the radicand is ≤ 0.
- `min_trl(sr, skew, kurt, sr_star=0.0, alpha=0.05) -> float | None`: `1 + (1 − skew·sr + (kurt−1)/4·sr²)·(z_{1−α}/(sr−sr*))²`. Returns None if sr ≤ sr*.
- `expected_max_sr(V, N) -> float`: `√V·((1−γ)·Φ⁻¹(1−1/N) + γ·Φ⁻¹(1−1/(N·e)))`, with γ = 0.5772156649015329. Returns 0.0 when N ≤ 1.
- `pbo_cscv(matrix, s=16) -> dict | None`: CSCV as defined below. Returns None if there are fewer than 2 columns or the effective s is below 4.
- `normalize(df) -> DataFrame`: validates and normalizes a trades frame. Columns: `entry_time`/`exit_time` as UTC tz-aware, `side` as int ±1, `pnl` as float, plus any optional columns. Sorted by `exit_time`.
- `load_trades(path) -> DataFrame`: reads CSV or parquet, then calls `normalize`. A missing required column raises `SystemExit` naming the column.
- `daily_pnl(trades, periods_per_year) -> Series`: P&L summed per exit date. For `periods_per_year < 365` the index is business days; weekend dates roll forward with `d + pd.offsets.BDay(0)`. Days with no trades are filled with 0, from the first entry date to the last exit date.
- `main(argv: list[str] | None = None)`: argparse with subcommands `stats` and `render`, using the exact flags in the spec's "review.py contract".
- `RUBRIC`: a list of `(name, weight, gate)` tuples in the order given in Global Constraints.

**Algorithm notes (implement exactly):**

- **Side parsing:** case-insensitive. `buy`, `long` and `1` map to +1; `sell`, `short` and `-1` map to −1. Anything else raises `SystemExit`.
- **Timestamps:** `pd.to_datetime(col, utc=True, format="mixed")`. Naive values are read as UTC; aware values are converted to UTC.
- **Daily returns:** `r_t = pnl_t / E_{t−1}`, where `E_0 = capital` and `E_t = E_{t−1} + pnl_t`.
- **Equity metrics:**
  - Sharpe = mean/std(ddof=1)·√ppy.
  - Sortino = mean/√mean(min(r,0)²)·√ppy.
  - CAGR = (E_end/capital)^(ppy/T) − 1.
  - Max DD is measured on daily equity: (peak − E)/peak, with the starting capital included as the first peak.
  - DD duration is the longest number of calendar days from a peak to recovery, or to the end if equity never recovers.
  - Calmar = CAGR / max DD, or None if max DD is 0.
- **Trade stats on `pnl`:**
  - win_rate, with the Wilson 95% CI.
  - avg_win; avg_loss (a positive number); payoff = avg_win/avg_loss.
  - profit_factor = Σwins/|Σlosses|.
  - expectancy = mean, with its t-based 95% CI.
  - t_stat and the two-sided p-value.
  - SQN = √min(n,100)·mean/std. Uses `r_multiple` if present, otherwise `pnl`; the basis used is stored as `sqn_basis`.
  - max_consec_losses.
  - n_required = ⌈((1.96+0.8416)·std/mean)²⌉ when mean > 0, else None.
- **Deflation:**
  - Use daily returns `r`: `sr_period = mean/std`, `T = len(r)`, `skew = scipy.stats.skew`, `kurt = scipy.stats.kurtosis(fisher=False)`.
  - `psr0 = psr(sr_period, T, skew, kurt)`; `min_trl_periods = min_trl(...)`.
  - With variants: `dsr = {"source": "variants", "n": N, "v": var(per-period Sharpe of each variant, ddof=1), "sr0": ..., "dsr": psr(sr_period, T, skew, kurt, sr0)}`.
  - Without variants: `dsr = {"source": "null_grid", "rows": [{"n": N, "sr0": ..., "dsr": ...} for N in (1, 10, 50, 100, 500)], "note": ...}`. Here V = (1 − skew·sr + (kurt−1)/4·sr²)/(T−1), which is the dispersion of estimated Sharpe ratios when every trial's true Sharpe is 0.
- **Monte Carlo** (`--sims`, default 10000, `--seed`; process in chunks of ≤1000 sims to bound memory). The equity path is `capital + cumsum(pnl)` and DD is measured as a fraction of the running peak.
  - `reshuffle`: permutations. Outputs `max_dd {p50, p95, p99}`, `p_breach` (max_dd ≥ `--dd-limit`), and `hist {counts, edges}` (40 bins of max_dd).
  - `bootstrap`: sampling with replacement. Outputs `max_dd {p50, p95, p99}`, `final_return {p5, p50, p95}` (= final equity/capital − 1), `p_loss` (final < capital), and `p_breach`.
- **CSCV (`pbo_cscv`):**
  - `s = min(s, (T//5)//2*2)`. Split row indices into `s` contiguous blocks with `np.array_split`.
  - For each combination of `s/2` blocks: IS = the chosen blocks, OOS = the rest. Compute the per-column Sharpe (mean/std; 0 if std is 0) on IS and on OOS.
  - `best = argmax(IS)`. `rank = scipy.stats.rankdata(OOS)[best]`, where 1 is worst and N is best.
  - `w = rank/(N+1)`, `logit = ln(w/(1−w))`.
  - Return `{"pbo": mean(logit ≤ 0), "n_variants": N, "s": s, "n_combos": ..., "p_oos_loss": mean(OOS[best] < 0), "logit_median": ...}`.
- **Regimes (`--prices`):**
  - Parse `time` as UTC. If the median bar spacing is under 1 day, resample to daily (high max, low min, close last, then dropna).
  - TR = max(h−l, |h−c₋₁|, |l−c₋₁|). ATR14 = rolling mean of TR. natr = ATR/close.
  - `vol = expanding(min_periods=20).rank(pct=True)` of natr, bucketed into thirds → `low` / `mid` / `high`.
  - ER20 = |c − c₋₂₀| / Σ₂₀|Δc|. Above 0.3 → `trend`, otherwise `range`.
  - Label = `f"{vol}-vol {trend}"`, then `.shift(1)` so only the previous day is used.
  - Attach to trades with `pd.merge_asof` on `entry_time`, direction backward. Rows with no label become `unknown`.
- **Breakdown rows:** `{key, n, win_rate, expectancy, profit_factor, total_pnl, low_n: n < 30}`. Groups: `by_year` (exit year), `by_side`, `by_hour` (entry hour UTC), `by_regime` (empty list without prices).
- **Recency:**
  - `recent` = trades with exit within the last `--recent-days` days of the sample. `prior` = the rest. Each gets `{n, expectancy, win_rate, profit_factor}`, plus `welch_p` comparing the two pnl sets.
  - `split_70_30` = the first 70% of trades vs the last 30%, with the same fields.
- **Live (`--live`):**
  - `{n, expectancy, win_rate, profit_factor, max_dd, welch_p, mannwhitney_p, ks_p, expectancy_in_backtest_ci95, dd_vs_mc, hint}`.
  - `dd_vs_mc` is one of `within`, `above_p95`, `above_p99`, measured against the reshuffle percentiles.
  - `hint` is one of:
    - `inconclusive (<50 live trades)` if n < 50
    - `decay_suspected` if the live expectancy is outside the CI or `dd_vs_mc` is not `within`
    - `consistent` otherwise
- **Rolling:** `{window: max(10, min(50, n//4)), values: [[exit_time_iso, rolling_mean_pnl], ...]}`. Omit the leading NaNs.
- **Tripwires:** items `{name, value, threshold, hit}` for:
  - Sharpe > 3
  - max_dd < 0.05
  - profit_factor > 4
  - win_rate > 0.8
  - n < 100

  Plus `hits` and `curve_fit_suspect = hits >= 3`. A missing value counts as no hit.
- **Warnings (strings):**
  - n < 30 → "only N trades — statistics unreliable (<30 trades)"
  - n < 100 → "fewer than 100 trades"
  - no prices → regime breakdown skipped
  - no variants → PBO not computed; DSR uses the null grid
  - no live → decay not tested
- **`metrics.json` top-level keys:** `meta, trade_stats, equity, deflation, monte_carlo, breakdown, recency, rolling, tripwires, warnings`, plus `pbo` (null without variants) and `live` (present only with `--live`).
  - `equity` = `{series: [[date, equity, dd], ...], total_return, cagr, max_dd, max_dd_duration_days, calmar, sharpe, sortino}`.
  - `meta` = `{generated_at, capital, periods_per_year, first_entry, last_exit, inputs}`.
- **`render`:**
  - Load both JSON files. Validate the scorecard: `system`, `verdict` and `dimensions` are required; the verdict must be one of the 5; every score must be in 0–5. Otherwise raise `SystemExit` with the reason.
  - `overall = Σ weight·score/5`, printed with 1 decimal.
  - Warn (in the HTML) with the word "contradicts" when the verdict is more aggressive than the band or gate rule allows.
  - Also warn when the scorecard's dimension names or weights differ from `RUBRIC`.
  - Charts are matplotlib SVG (Agg backend, `svg.fonttype = "none"`), inlined in the HTML:
    - equity with a drawdown sub-panel
    - rolling expectancy
    - Monte Carlo max-DD histogram, with the `dd_limit` line and the realised max DD marked
    - P&L by year
    - weighted dimension scores as horizontal bars
  - Before writing chart code, invoke the `dataviz` skill and follow its palette and mark rules.
  - Section order:
    1. header (system, date, model, independence badge)
    2. verdict and score
    3. scorecard table and chart
    4. tripwires and key statistics
    5. overfitting (scorecard `overfitting`, DSR, PBO)
    6. charts
    7. breakdowns
    8. recency and live
    9. code findings
    10. what's outdated
    11. new features
    12. revamp plan
    13. sources
    14. independence and limitations
  - Missing optional sections render as "Not provided."
  - `--open` calls `webbrowser.open(out.resolve().as_uri())`.

- [ ] **Step 1: Write the failing tests** — create `test_review.py` with exactly this content:

```python
"""Tests for review.py: synthetic data only. Run: python -m pytest scripts/test_review.py -q"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).parent))
import review as rv  # noqa: E402


def make_trades(n=300, seed=1, edge=0.15, start="2023-01-02"):
    rng = np.random.default_rng(seed)
    entry = pd.date_range(start, periods=n, freq="17h", tz="UTC")
    return pd.DataFrame({
        "entry_time": entry,
        "exit_time": entry + pd.Timedelta(hours=5),
        "side": np.where(rng.random(n) > 0.5, "BUY", "SELL"),
        "pnl": rng.normal(edge, 1.0, n) * 100,
    })


def run_stats(tmp_path, df, *extra):
    tp = tmp_path / "trades.csv"
    df.to_csv(tp, index=False)
    out = tmp_path / "metrics.json"
    rv.main(["stats", "--trades", str(tp), "--capital", "10000", "--sims", "500",
             "--out", str(out), *extra])
    return json.loads(out.read_text(encoding="utf-8"))


# Reference values verified in Python on 2026-10-02.
def test_psr_reference():
    assert rv.psr(0.1, 250, -0.5, 5.0) == pytest.approx(0.9373, abs=1e-4)


def test_min_trl_reference():
    assert rv.min_trl(0.1, -0.5, 5.0) == pytest.approx(287.79, abs=0.01)
    assert rv.min_trl(-0.1, -0.5, 5.0) is None


def test_expected_max_sr_reference():
    assert rv.expected_max_sr(0.25, 100) == pytest.approx(1.2653, abs=1e-4)
    assert rv.expected_max_sr(0.25, 1) == 0.0


def test_dsr_reference():
    sr0 = rv.expected_max_sr(0.01, 100)
    assert rv.psr(0.1, 250, -0.5, 5.0, sr0) == pytest.approx(0.0095, abs=1e-4)


def test_pbo_noise_near_half():
    m = np.random.default_rng(0).normal(0, 0.01, (800, 50))
    assert 0.35 <= rv.pbo_cscv(m, s=8)["pbo"] <= 0.65


def test_pbo_real_edge_near_zero():
    m = np.random.default_rng(0).normal(0, 0.01, (800, 50))
    m[:, 7] += 0.0015
    assert rv.pbo_cscv(m, s=8)["pbo"] < 0.1


def test_side_parsing_and_missing_column(tmp_path):
    df = make_trades(8)
    df["side"] = ["BUY", "sell", "1", "-1", "long", "Short", "buy", "SELL"]
    p = tmp_path / "t.csv"
    df.to_csv(p, index=False)
    assert list(rv.load_trades(p)["side"]) == [1, -1, 1, -1, 1, -1, 1, -1]
    df.drop(columns="pnl").to_csv(p, index=False)
    with pytest.raises(SystemExit, match="pnl"):
        rv.load_trades(p)


def test_mixed_naive_and_aware_timestamps(tmp_path):
    p = tmp_path / "t.csv"
    p.write_text(
        "entry_time,exit_time,side,pnl\n"
        "2024-01-02 10:00:00,2024-01-02T12:00:00+00:00,BUY,5\n"
        "2024-01-03T10:00:00+02:00,2024-01-03 15:00:00,SELL,-3\n")
    t = rv.load_trades(p)
    assert str(t["exit_time"].dt.tz) == "UTC"
    assert t["entry_time"].iloc[1] == pd.Timestamp("2024-01-03 08:00", tz="UTC")


def test_weekend_exit_pnl_is_kept():
    df = make_trades(60)
    df.loc[5, "exit_time"] = pd.Timestamp("2023-01-07 12:00", tz="UTC")  # Saturday
    t = rv.normalize(df)
    daily = rv.daily_pnl(t, periods_per_year=252)
    assert daily.sum() == pytest.approx(t["pnl"].sum())
    assert all(d.weekday() < 5 for d in daily.index)


def test_stats_end_to_end(tmp_path):
    m = run_stats(tmp_path, make_trades())
    for key in ["meta", "trade_stats", "equity", "deflation", "monte_carlo", "breakdown",
                "recency", "rolling", "tripwires", "warnings"]:
        assert key in m
    assert m["trade_stats"]["n"] == 300
    mc = m["monte_carlo"]["reshuffle"]["max_dd"]
    assert mc["p99"] >= mc["p95"] >= mc["p50"] > 0
    assert m["pbo"] is None
    assert m["deflation"]["dsr"]["source"] == "null_grid"


def test_all_winners_profit_factor_serialises(tmp_path):
    df = make_trades(20)
    df["pnl"] = df["pnl"].abs() + 1
    m = run_stats(tmp_path, df)
    assert m["trade_stats"]["profit_factor"] is None
    assert m["tripwires"]["items"][3]["hit"] is True  # win_rate > 0.8


def test_tiny_sample_does_not_crash(tmp_path):
    m = run_stats(tmp_path, make_trades(3))
    assert m["trade_stats"]["n"] == 3
    assert any("trades" in w for w in m["warnings"])


def test_prices_variants_and_live(tmp_path):
    rng = np.random.default_rng(3)
    hours = pd.date_range("2022-10-01", "2023-12-31", freq="h", tz="UTC")  # intraday bars
    close = 1800 + np.cumsum(rng.normal(0, 2, len(hours)))
    pd.DataFrame({"time": hours, "high": close + 1, "low": close - 1, "close": close}).to_csv(
        tmp_path / "prices.csv", index=False)
    var = pd.DataFrame(rng.normal(0, 0.01, (300, 12)), columns=[f"v{i}" for i in range(12)])
    var.insert(0, "date", pd.date_range("2023-01-02", periods=300, freq="B"))
    var.to_csv(tmp_path / "variants.csv", index=False)
    make_trades(40, seed=9, edge=-0.3, start="2024-01-02").to_csv(tmp_path / "live.csv", index=False)
    m = run_stats(tmp_path, make_trades(), "--prices", str(tmp_path / "prices.csv"),
                  "--variants", str(tmp_path / "variants.csv"), "--live", str(tmp_path / "live.csv"))
    regimes = {row["key"] for row in m["breakdown"]["by_regime"]}
    assert regimes and regimes <= {f"{v}-vol {t}" for v in ("low", "mid", "high")
                                   for t in ("trend", "range")} | {"unknown"}
    assert 0.0 <= m["pbo"]["pbo"] <= 1.0
    assert m["deflation"]["dsr"]["source"] == "variants"
    assert m["live"]["n"] == 40
    assert m["live"]["hint"].startswith("inconclusive")


def test_render_escapes_and_recomputes_score(tmp_path):
    run_stats(tmp_path, make_trades())
    sc = {
        "system": "demo<script>alert(1)</script>",
        "review_date": "2026-10-02",
        "model": {"name": "test-model", "knowledge_cutoff": "2026-06"},
        "independence": {"clean": False, "notes": "memory loaded"},
        "verdict": "DEPLOY",
        "summary": "x",
        "dimensions": [{"name": n, "weight": w, "gate": g, "score": 1, "evidence": "e"}
                       for n, w, g in rv.RUBRIC],
        "findings": [{"severity": "high", "location": "a.py:1",
                      "finding": "<img src=x onerror=alert(1)>", "fix": "f"}],
        "sources": [{"title": "bad", "url": "javascript:alert(1)", "published": "",
                     "retrieved": "", "tier": "anecdotal"}],
    }
    (tmp_path / "scorecard.json").write_text(json.dumps(sc), encoding="utf-8")
    out = tmp_path / "report.html"
    rv.main(["render", "--metrics", str(tmp_path / "metrics.json"),
             "--scorecard", str(tmp_path / "scorecard.json"), "--out", str(out)])
    html = out.read_text(encoding="utf-8")
    assert "<script>alert(1)" not in html and "<img src=x" not in html
    assert 'href="javascript:' not in html
    assert "20.0" in html          # all ten dimensions at 1/5 -> 20.0
    assert "contradicts" in html   # DEPLOY with gates at 1
    assert "<svg" in html


def test_render_rejects_bad_scorecard(tmp_path):
    run_stats(tmp_path, make_trades())
    (tmp_path / "scorecard.json").write_text(json.dumps({"system": "x", "verdict": "YOLO",
                                                         "dimensions": []}), encoding="utf-8")
    with pytest.raises(SystemExit, match="verdict"):
        rv.main(["render", "--metrics", str(tmp_path / "metrics.json"),
                 "--scorecard", str(tmp_path / "scorecard.json"),
                 "--out", str(tmp_path / "r.html")])
```

- [ ] **Step 2: Run the tests to verify they fail**
  - Run: `python -m pytest plugins/trading-system-review/skills/trading-system-review/scripts/test_review.py -q`
  - Expected: collection error `ModuleNotFoundError: No module named 'review'`.

- [ ] **Step 3: Implement `review.py`** per the Interfaces and Algorithm notes above.
  - Add a module docstring giving the two CLI usages and the input schemas.
  - Invoke the `dataviz` skill before writing the chart functions.

- [ ] **Step 4: Run the tests to verify they pass**
  - Run: `python -m pytest plugins/trading-system-review/skills/trading-system-review/scripts/test_review.py -q`
  - Expected: `15 passed`.
  - Then render a sample report and open it to eyeball the layout:
    `python review.py render ... --open`, using the files from a `stats` run on `make_trades()` data.

- [ ] **Step 5: Commit**

```bash
git add plugins/trading-system-review/skills/trading-system-review/scripts/
git commit -m "feat(trading-system-review): add review.py stats/render engine with tests"
```

### Task 2: SKILL.md + references

**Files:**
- Create: `plugins/trading-system-review/skills/trading-system-review/SKILL.md`
- Create: `plugins/trading-system-review/skills/trading-system-review/references/rubric.md`
- Create: `plugins/trading-system-review/skills/trading-system-review/references/search-playbook.md`

**Interfaces:**
- **Consumes:** the `review.py` CLI and the `metrics.json` keys from Task 1, and `RUBRIC` names and weights.
- **Produces:** the `scorecard.json` schema (the one `render` validates). Required keys: `system`, `verdict`, `dimensions[{name, weight, gate, score 0-5, evidence}]`. Optional keys: `repo, review_date, model{name, knowledge_cutoff}, independence{clean, notes}, summary, edge_thesis, overfitting{verdict, why}, findings[], outdated[], new_features[], revamp_plan[], sources[], limitations[]`.

- [ ] **Step 1: Write SKILL.md**
  - Frontmatter: `name`, a "Use when…" description, `model: best`, `argument-hint`.
  - Phases 0–5 as in the spec.
  - The "Evidence rules" block that every subagent prompt must include verbatim.
  - The exclusion patterns from the repo survey.
  - The clean-launch recipe.
  - The work-item definitions W1–W4 with their output files.
  - The scorecard schema.
  - Boundaries.
- [ ] **Step 2: Write `references/rubric.md`**
  - Review order.
  - The 10 dimensions, each with weight, gate, what scores 0/3/5 look like, the metrics to use (keyed to `metrics.json` paths), and source tags.
  - Verdict bands and the gate rule.
  - Tripwires.
  - The code-integrity checklist.
  - Live-vs-backtest decay rules.
  - Sources.
- [ ] **Step 3: Write `references/search-playbook.md`**
  - Recency rules and source tiers.
  - Query templates A–E with placeholders.
  - CloakBrowser fallback one-liner.
  - Output discipline (claim, date, tier, verified/unverified).
- [ ] **Step 4: Verify**
  - Every `metrics.json` path cited in rubric.md exists in a real `metrics.json` produced by Task 1 (grep each path).
  - The scorecard example in SKILL.md passes `render` (save it as JSON, run `render` against the Task 1 sample metrics, expect exit 0).
- [ ] **Step 5: Commit**: `git commit -m "feat(trading-system-review): add SKILL.md orchestration brain + rubric + search playbook"`

### Task 3: Plugin wiring + README

**Files:**
- Create: `plugins/trading-system-review/.claude-plugin/plugin.json`
- Modify: `.claude-plugin/marketplace.json` (add the plugin entry, keeping alphabetical order: after `system-builder`, before `trading-rnd`)
- Modify: `README.md`:
  - the "seven" → "eight" mentions
  - the install line
  - the at-a-glance row
  - the which-one row
  - the duplicate-copies list
  - a new user-guide section
  - repo layout

- [ ] **Step 1: Write `plugin.json`**: `{name, description, version: "1.0.0", author: {name: "Tang Cong Han"}}`.
- [ ] **Step 2: Edit `marketplace.json` and `README.md`.**
- [ ] **Step 3: Verify**
  - Both JSON files parse: `python -c "import json;json.load(open(...))"`.
  - Run `claude plugin validate plugins/trading-system-review` if the command exists.
  - Run `git grep -n "seven"` on README.md and expect no stale counts.
- [ ] **Step 4: Commit**: `git commit -m "feat(trading-system-review): register plugin in marketplace + README"`

### Task 4: Whole-branch review

- [ ] One fresh reviewer, on the most capable model, reads the spec and the branch diff and reports defects.
- [ ] Fix confirmed defects, re-run the tests, and commit.
