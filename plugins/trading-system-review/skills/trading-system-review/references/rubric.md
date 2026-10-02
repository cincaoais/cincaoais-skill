# Senior-trader rubric

Source tags:

- **[S]** primary or authoritative source.
- **[B]** practitioner or blog level.
- **[H]** this skill's synthesis.

Thresholds tagged [B] or [H] are defaults, not laws. Say so when one decides a score.
Metric paths refer to `metrics.json` from `review.py stats`.

## Review order

A senior reviewer reads a system in this order. Write your synthesis in the same order.

1. **Edge thesis.** Where does the P&L come from, who is on the other side, and why would it persist?
2. **Data and code integrity.** Hard gate.
3. **Research process.** How many variants and parameters were tried? If nobody knows, overfitting
   can't be ruled out [S Bailey et al. 2014].
4. **Statistics after deflation.**
5. **Robustness.**
6. **Costs, execution and capacity.**
7. **Risk and sizing.**
8. **Live vs backtest.**
9. **Operations.**
10. **Market currency.** Is the regime it was fitted on still here?

## Dimensions

Score each 0–5. Weighted score = Σ weight·score/5, which `render` computes.
Names and weights must match `RUBRIC` in `scripts/review.py`.

| name | weight | gate |
|---|---|---|
| `edge_thesis` | 10 | |
| `data_code_integrity` | 15 | gate |
| `statistical_significance` | 12 | |
| `overfitting_control` | 12 | gate |
| `robustness` | 10 | |
| `costs_execution` | 8 | |
| `risk_sizing` | 10 | |
| `live_tracking` | 8 | |
| `market_currency` | 10 | |
| `operations` | 5 | |

### edge_thesis (10)

- **5:** The mechanism and counterparty are stated, and the reason it persists fits the instrument.
  The breakdowns agree: P&L comes from where the thesis says.
- **3:** A plausible story that is only partly supported by the breakdowns.
- **0:** No rationale. Pure pattern-mining.
- **Inputs:** `system-map.md`; `breakdown.by_regime`, `breakdown.by_hour`, `breakdown.by_side`
  (P&L concentration).

### data_code_integrity (15, gate)

- **5:** The checklist below comes back clean, the backtest was reproduced in this review, and the
  tests pass.
- **3:** Minor issues with bounded, stated impact.
- **1:** An issue that plausibly inflates results materially. Examples: optimistic same-bar SL/TP
  ordering, fills at the signal bar's close, or using a higher-timeframe bar before it closes.
- **0:** Confirmed look-ahead or leakage, or results that can't be reproduced.
- **Inputs:** `code-audit.md`, `backtest-notes.md`.

### statistical_significance (12)

- **5:** `trade_stats.n` ≥ 200, `t_stat` > 3 [S Harvey-Liu-Zhu 2016], and a DSR above 0.95 at a
  realistic N [S Bailey & López de Prado 2014].
- **3:** n ≥ 100, t > 2, `deflation.psr0` > 0.95, but DSR weak.
- **1:** n < 100, or `expectancy_ci95` includes 0.
- **0:** expectancy ≤ 0.
- **Inputs:** `trade_stats.{n, expectancy, expectancy_ci95, t_stat, p_value, sqn, n_required}`,
  `deflation.{psr0, min_trl_periods, dsr}`.
- **DSR with no variants:** use the `deflation.dsr.rows` entry whose N is closest to the honest trial
  count: the parameters, filters and variants the author plausibly tried. Never use N = 1 unless the
  rules were fixed before seeing any data.
- **SQN bands** [B Tharp]: below 1.6 poor; 2.0–2.4 average; 2.5–2.9 good; 3.0–5.0 excellent; above 7
  is suspect.

### overfitting_control (12, gate)

- **5:** At most 5 free parameters, `pbo.pbo` < 0.1, the parameter neighbourhood is a plateau
  (±25% keeps Sharpe within 30% of the best [B aligrithm]), and `recency.split_70_30` holds out of
  sample.
- **3:** PBO < 0.3 [B aligrithm], with modest out-of-sample degradation.
- **1:** Any one of: PBO 0.3–0.5, `tripwires.curve_fit_suspect` true, or many parameters with no
  out-of-sample test.
- **0:** PBO > 0.5, or out-of-sample expectancy ≤ 0 while in-sample looks strong.
- **Inputs:** free-parameter count from `system-map.md`; `pbo.{pbo, p_oos_loss}`;
  `variants.csv` dispersion; `recency.split_70_30`; `tripwires`; `deflation.dsr`.

**Overfitting verdict** (goes in `scorecard.overfitting`):

| verdict | when |
|---|---|
| `overfit` | PBO > 0.5, or out-of-sample collapse |
| `likely overfit` | PBO 0.3–0.5, or curve-fit tripwires, or a sharp parameter peak |
| `inconclusive` | no variants and n < 100. Say what would settle it. |
| `not overfit` | PBO < 0.3, a plateau, out-of-sample holds, and DSR > 0.95 at an honest N |

### robustness (10)

- **5:** Profitable in most years (`breakdown.by_year`) and regimes (`breakdown.by_regime`, at least
  30 trades per bucket [B aligrithm]). The parameter plateau holds. The 2× cost shock costs at most
  0.5 Sharpe [B aligrithm] (`metrics-cost2x.json` `equity.sharpe` vs `metrics.json`).
- **3:** One year or regime carries much of the P&L, but the others are not negative.
- **0:** A single regime or year carries all the P&L.

### costs_execution (8)

- **5:** Spread, commission, slippage and swap are modelled at or above the venue's real levels.
  Entries fill at the next bar's open or later. Same-bar SL/TP is resolved pessimistically. The 2×
  cost shock survives.
- **0:** Frictionless or optimistic fills.
- **Inputs:** `code-audit.md`, `backtest-notes.md`, `metrics-cost2x.json`.

### risk_sizing (10)

- **5:** Monte Carlo drawdowns sit well inside the limit: `monte_carlo.reshuffle.max_dd.p99` <
  `--dd-limit` with margin, and `p_breach` < 5%. This is the 99th-percentile kill-switch idea
  [B aligrithm]. Sizing is fixed-fractional or vol-scaled.
- **3:** p95 is inside the limit and p99 is near it.
- **0:** Martingale, grid or averaging down without a hard stop, or p95 is above the limit.
- **Also read:** `monte_carlo.bootstrap.{p_loss, final_return.p5}`.

### live_tracking (8)

- **5:** At least 6 months and 50 trades of live or forward trading [B Davey incubation, 3–12
  months], with `live.hint` = `consistent`.
- **3:** A forward record exists, but `live.hint` is `inconclusive`.
- **1:** No forward record. That is unverifiable, which is not the same as failed.
- **0:** `live.hint` = `decay_suspected`, with ≥ 50 trades or `live.dd_vs_mc` = `above_p99`.

### market_currency (10)

- **5:** Today's regime (from `market-research.md`) is one where the system makes money
  (`breakdown.by_regime`). There are no adverse venue, contract or prop-rule changes. The
  `recency.recent` window matches `recency.prior`.
- **3:** Mixed.
- **0:** Today's regime is the one where it loses and the recent window is negative, or a rule or
  contract change breaks an assumption.

### operations (5)

- **5:** Kill switch, daily-loss and max-position limits enforced in code. Prop rules enforced in
  code. Reconnect and idempotent orders. State recovery. News blackout where required. Logging and
  alerting.
- **0:** None of these.

## Verdict

`render` enforces this and flags violations with "contradicts".

| weighted score | verdict |
|---|---|
| ≥ 85 | `DEPLOY` |
| 70–84.9 | `DEPLOY-REDUCED` (30–50% size, re-review) |
| 50–69.9 | `INCUBATE` (demo / forward only) |
| < 50 | `REVAMP` or `RETIRE` |

- **Gate rule:** if `data_code_integrity` or `overfitting_control` scores ≤ 1, only `REVAMP` or
  `RETIRE` is allowed. This follows aligrithm's "do not deploy" matrix [B].
- **Conservative verdicts are fine.** You may pick a less aggressive verdict than the band, for
  example `INCUBATE` at 78 with no forward record. You may never pick a more aggressive one.
- **`RETIRE` vs `REVAMP`:** choose `RETIRE` when there is no edge after costs on an adequate sample
  (`expectancy_ci95` ≤ 0 at n ≥ 200, or DSR < 0.5 at an honest N with PBO > 0.5), or when decay is
  confirmed and the thesis no longer applies. Otherwise choose `REVAMP`.
- The bands are [H] synthesis.

## Curve-fit tripwires [B]

`tripwires` checks these automatically:

- Sharpe > 3
- max DD < 5%
- PF > 4
- win rate > 80%
- n < 100

Add by judgment:

- more than about 10 free parameters
- no out-of-sample period
- longest losing streak under 3

Three or more hits means treat the system as curve-fit until proven otherwise.

## Code-integrity checklist (W1)

**Look-ahead:**

- An indicator uses the current bar's close, high or low before that bar closes.
- Signal and fill happen on the same bar's close.
- A higher-timeframe bar is used before it closes. Check resample `label`/`closed`, and MT5
  `copy_rates` index 0 vs 1.
- `shift(-n)` appears anywhere.
- Scaling or normalisation is fitted on the full sample.
- The day's high or low is used for intraday decisions.

**Same-bar SL/TP:** when both sit inside one bar, which one does the backtest assume hits first?
Optimistic ordering inflates results.

**Fill model:**

- Entry at the signal close vs the next open.
- Spread on both sides.
- Slippage, commission, swap or overnight financing.
- Broker minimum stop distance.
- Lot rounding and limits.

**Time:**

- Data timezone vs broker server time.
- DST handling.
- Session filters.
- Holiday, rollover and weekend gaps.

**Data:**

- Survivorship (stocks).
- Corporate actions.
- Futures roll method.
- Missing bars and bad ticks.
- Vendor feed vs broker feed differences.

**Backtest/live parity:** do backtest and live run the same signal code path, or duplicated logic
that can drift apart?

**AI/LLM components:**

- Backtested LLM decisions dated inside the model's training window are look-ahead
  [S arXiv 2601.13770, Look-Ahead-Bench].
- Check that prompts can't contain future data.
- Check how non-determinism and caching are handled.
- Only forward results or point-in-time-sanitised replays count.

**Risk code:**

- Max position, daily loss and prop-firm limits enforced in code.
- Any martingale, grid or averaging down.

**Ops:**

- Exception handling around broker calls.
- Reconnect.
- Idempotent order placement.
- State persistence.
- Kill switch.
- Alerting.

**Parameters:**

- Count the free parameters.
- Look for suspicious precision.
- Look for values that differ per symbol or period.

## Live vs backtest: decay rules [B/H]

- Live max DD above the backtest's MC p95, or above 1.5× the backtest max DD, means review.
  Above p99 means stop.
- Live expectancy outside the backtest's 95% CI after at least 50–100 trades means decay is
  suspected. With fewer trades, the result is inconclusive, not decayed.
- Separate execution decay (fills, spread, slippage worse than modelled) from edge decay (signals
  worse). Compare live fills with simulated fills before blaming the edge.
- If it only worked in a regime that has ended, revamp the regime filter. Don't retire the idea yet.
- Published anomalies lose about 58% of their returns after publication
  [S McLean & Pontiff 2016, SSRN 2156623]. Expect live results below the backtest.

## Sources

- Bailey & López de Prado, *The Deflated Sharpe Ratio* (2014) — https://www.davidhbailey.com/dhbpapers/deflated-sharpe.pdf
- Bailey, Borwein, López de Prado & Zhu, *The Probability of Backtest Overfitting* — SSRN 2326253
- Bailey et al., *Pseudo-Mathematics and Financial Charlatanism* (AMS Notices 2014) — https://www.ams.org/notices/201405/rnoti-p458.pdf
- Harvey, Liu & Zhu, *…and the Cross-Section of Expected Returns* (RFS 2016) — https://academic.oup.com/rfs/article/29/1/5/1843824
- McLean & Pontiff, *Does Academic Research Destroy Stock Return Predictability?* (JF 2016) — SSRN 2156623
- Resonanz Capital, quant DD framework (2026) — https://resonanzcapital.com/insights/quant-hedge-funds-in-2026-a-due-diligence-framework-by-strategy-type
- aligrithm, *Backtest Integrity Checklist* — https://aligrithm.com/the-backtest-integrity-checklist/
- Pardo, *The Evaluation and Optimization of Trading Strategies* (2008): walk-forward efficiency ≥ 50–60% [B]
- Davey, incubation and Monte Carlo practice — https://www.financialwisdomtv.com/post/building-winning-algorithmic-trading-systems-kevin-davey-s-complete-framework-for-trading-success
