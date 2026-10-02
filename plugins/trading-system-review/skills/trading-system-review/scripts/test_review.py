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
    m[:, 7] += 0.003  # per-period SR 0.3: PBO 0.0 on seeds 0-9 (0.0015 was seed-fragile)
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
