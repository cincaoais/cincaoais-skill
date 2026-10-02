# trading-system-review — design

Date: 2026-10-02 · Status: approved (user, 2026-10-02) · Plugin: `trading-system-review`

## Goal

A skill that rates one of the user's existing algorithmic trading systems the way a senior
trader / prop-desk head would, with fresh eyes: performance, overfitting, whether it is still in
line with the current market, what is outdated, which new features are worth adding, and whether
to deploy, incubate, revamp or retire. Output is a self-contained HTML report with charts.

## Requirements (from the user)

1. Runs on the newest model; that model plans the review as a senior trader.
2. Does **not** read old data: prior research, plans, audits, memory. It judges from the latest
   model's understanding plus fresh web search.
3. Delegates execution to cheaper subagents (Sonnet/Opus) through the user's `orchestrate` skill
   ("mention the orchestrate skill will do" — orchestrate will be modified later).
4. Web search prefers CloakBrowser for pages that block plain fetches.
5. Ends with a visual report: rating, performance, results, revamp needed or not and why, which
   part is outdated, recommended new features, overfitting verdict, charts.

## Decisions and premise corrections

| Topic | Decision | Basis |
|---|---|---|
| "Artifact" | Self-contained HTML file opened in the browser. Claude Code CLI has no Artifact tool. | Artifact is claude.ai-only (Claude Code docs, tools reference); the build session's tool list has none |
| Newest model | SKILL.md frontmatter `model: best`. That alias resolves to Fable where available, otherwise Opus, so nothing hard-codes a model name. | code.claude.com/docs/en/model-config (fetched 2026-10-02) |
| Model knowledge | The model supplies judgment, not current facts (Opus 5.5 cutoff: June 2026). Current facts come from dated web sources plus a fresh backtest on the latest data. | — |
| No old data | Skill instructions alone can't stop auto-memory from loading. The skill does four things: (a) a Phase-0 contamination check, (b) a documented clean-launch recipe `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1` from a directory with no CLAUDE.md, (c) a file-exclusion list given to every subagent, (d) an "independence" section in the report. | code.claude.com/docs/en/memory (fetched 2026-10-02). During R&D a subagent quoted the user's MEMORY.md, so subagents do see it |
| Stored results | Treated as claims. Backtests are re-run where possible; otherwise stored trade logs are labelled "unverified". | The surveyed repos' own docs warn that earlier profit-factor claims were overfit |
| Numbers | Every statistic comes from `scripts/review.py`, never from the model's arithmetic. `render` also recomputes the weighted score and flags verdicts that contradict the gates or bands. | — |
| Orchestration | SKILL.md hands phases 1 and 3 to the `orchestrate` skill. The review plan states which model each work item needs (code audit → Opus; backtest, stats and web research → Sonnet). | User answer, 2026-10-02 |
| Simplicity | Ponytail "full" rules apply: 1 script, 2 references, 1 test file. No plugin agents (delegation belongs to orchestrate, and the plugin-agent `subagent_type` string is undocumented). CloakBrowser use is a one-liner, not a script. | User request, 2026-10-02 |
| Charts | matplotlib → inline SVG, so the report works offline. matplotlib 3.10.5, numpy 2.2.6, pandas 2.3.2, scipy 1.16.1 and pyarrow 24.0.0 are already installed. | Checked on this machine |
| CloakBrowser | `cloakbrowser` 0.5.10 is installed in system Python with the Chromium 146 binary. API: `from cloakbrowser import launch; b = launch(headless=True)`. Do not use the Claude-in-Chrome extension for research. | Checked on this machine; user preference recorded in goldman memory |

## R&D summary: how a senior trader rates a system

Source tags: **[S]** primary or authoritative source, **[B]** practitioner or blog level,
**[H]** our synthesis. Thresholds tagged [B] or [H] are defaults to tune, not laws.

**Review order** [H, anchored on Resonanz DD framework [S] and aligrithm checklist [S]]:

1. **Edge thesis:** where the P&L comes from and who is on the other side.
2. **Data and code integrity:** a hard gate.
3. **Research process:** the trial count.
4. **Statistics after deflation.**
5. **Robustness.**
6. **Costs, execution and capacity.**
7. **Risk and sizing.**
8. **Live vs backtest.**
9. **Operations.**
10. **Market currency.**

**Key thresholds:**

- **Significance:** t-stat > 3 for a new strategy [S Harvey-Liu-Zhu 2016, cross-sectional standard, extrapolated]. At least 100 trades, 200+ preferred [B / aligrithm].
- **Deflated Sharpe:** DSR > 0.95 [S Bailey & López de Prado 2014, formula verified against the paper].
- **Overfitting and robustness:**
  - PBO < 0.3 [aligrithm].
  - Parameters ±25% keep Sharpe within 30% of the optimum [aligrithm].
  - Walk-forward efficiency ≥ 50–60% [B Pardo].
  - Cost shock costs ≤ 0.5 Sharpe [aligrithm].
  - At least 30 trades per regime [aligrithm].
- **Kill switch:** at the 99th percentile of the bootstrap drawdown [aligrithm].
- **SQN bands:** below 1.6 poor; 2.5–2.9 good; above 7 "too good to be true" [B Tharp].
- **Curve-fit tripwires:** three or more of these mean "suspect": Sharpe > 3, max DD < 5%, PF > 4, win rate > 80%, fewer than 100 trades, many parameters, no OOS [B].
- **Decay rules** [B / H]:
  - Live DD above the Monte Carlo 95th percentile, or above 1.5× the backtest max DD → review.
  - Live expectancy outside the backtest 95% CI after at least 50–100 trades → decayed. Fewer trades → inconclusive.
  - Separate execution decay from edge decay.

Primary references:

- Bailey & López de Prado, Deflated Sharpe Ratio: https://www.davidhbailey.com/dhbpapers/deflated-sharpe.pdf
- PBO / CSCV: SSRN 2326253
- Bailey et al., Pseudo-Mathematics and Financial Charlatanism: https://www.ams.org/notices/201405/rnoti-p458.pdf
- Harvey-Liu-Zhu: https://academic.oup.com/rfs/article/29/1/5/1843824
- Harvey & Liu, Backtesting: SSRN 2345489
- McLean & Pontiff 2016 (58% post-publication decay): SSRN 2156623
- Resonanz Capital DD framework: https://resonanzcapital.com/insights/quant-hedge-funds-in-2026-a-due-diligence-framework-by-strategy-type
- aligrithm, Backtest Integrity Checklist: https://aligrithm.com/the-backtest-integrity-checklist/

**What the user's repos look like** (survey of 2026-10-01). There are about 8 systems:

- goldman, gold-scalping, trolltrader: XAUUSD on MT5/FTMO
- orderflow: MGC futures on Databento
- crypto-trading: crypto CFDs
- mugen: US stocks
- deepseek-harness-quant: A-shares
- liquidity-sweep: MQL5

Results formats differ: CSV, parquet, JSONL, and markdown-only reports. So the backtest step
must normalize trades to one schema, or re-run the backtest. Prior-research patterns to exclude
are listed in SKILL.md.

## Architecture

```
plugins/trading-system-review/
  .claude-plugin/plugin.json
  skills/trading-system-review/
    SKILL.md                    orchestration brain (model: best)
    references/rubric.md        review order, 10 dimensions, gates, thresholds, verdict bands, code checklist, decay rules
    references/search-playbook.md  recency rules, source tiers, query templates A–E, CloakBrowser one-liner
    scripts/review.py           `stats` → metrics.json ; `render` → report.html
    scripts/test_review.py      pytest, synthetic data only
```

**Run flow:**

- **Phase 0 — Independence gate (main model):** resolve the target repo, state model, cutoff and date, run the contamination check, create `trading-reviews/<system>-<date>/`.
- **Phase 1 — System map (orchestrate, Sonnet):** write `system-map.md`.
- **Phase 2 — Senior-trader plan (main model):** write `review-plan.md` with hypotheses, the backtest and parameter grid, filled search queries, and the model per work item.
- **Phase 3 — Execute (orchestrate), in parallel:**
  - W1 code audit (Opus) → `code-audit.md`
  - W2 backtest, normalize and stats (Sonnet) → `trades.csv`, `metrics.json`, `backtest-notes.md`
  - W3 market currency (Sonnet) → `market-research.md`
  - W4 new techniques (Sonnet) → `techniques-research.md`
- **Phase 4 — Synthesize and score (main model):** verify every claim, score the rubric, write `scorecard.json`.
- **Phase 5 — Report:** `review.py render` produces `report.html`; open it and post a short chat summary.

### review.py contract

```
python review.py stats  --trades trades.csv --capital 10000 [--prices prices.csv] [--variants variants.csv]
                        [--live live.csv] [--live-capital C] [--dd-limit 0.10] [--periods-per-year 252] [--recent-days 180]
                        [--sims 10000] [--seed 0] --out metrics.json
python review.py render --metrics metrics.json --scorecard scorecard.json --out report.html
```

- `trades.csv`:
  - Required columns: `entry_time, exit_time, side, pnl` (net, account currency).
  - Optional columns: `symbol, entry, exit, size, r_multiple`.
  - Side accepts `long/short/buy/sell/1/-1`, case-insensitive.
  - Naive timestamps are read as UTC.
- `prices.csv`: `time, high, low, close`, any bar size. Resampled to daily. Regime labels come from the previous day only.
- `variants.csv`: `date` plus one column of daily net returns (fractions) per parameter variant. It drives PBO (CSCV) and DSR with real N and V.
- `live.csv`: same schema as trades, holding live or forward trades. Used for the decay tests.
- `scorecard.json`: written by the main model. Its schema is in SKILL.md. `render` recomputes `overall_score` = Σ weight·score/5 and warns when the verdict contradicts the gates or bands.
- All text in the report is HTML-escaped. Only http(s) URLs become links.

## Testing

- `pytest scripts/test_review.py` with synthetic data. Reference values were checked in Python on 2026-10-02:
  - PSR(SR=0.1, T=250, γ3=−0.5, γ4=5) = 0.9373
  - MinTRL = 287.79
  - SR0(V=0.25, N=100) = 1.2653
  - DSR(N=100, V=0.01) = 0.0095
  - PBO on pure noise ≈ 0.5; PBO with one strong-edge variant ≈ 0
- Edge inputs: weekend exits keep their P&L, PF = ∞ serialises, n < 5, mixed tz-aware and naive timestamps, `<script>` in scorecard text is escaped, a missing column gives a clear error.
- No end-to-end trial run on a real repo (user's choice, 2026-10-02). Agent-behaviour (RED/GREEN) skill testing is likewise not done.

## Out of scope

Editing the target system, placing orders, starting live loops, financial advice, walk-forward
re-optimisation inside `review.py` (repo-specific, so it is done by the W2 subagent with the
repo's own engine when supported).
