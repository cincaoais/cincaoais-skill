---
name: trading-system-review
description: >
  Use when the user wants an existing algorithmic trading system (bot, EA, strategy repo, prop-firm
  system) rated, audited, or judged the way a senior trader or prop-desk head would: "rate my trading
  system", "is my system still working / still in line with the market", "is it outdated", "is it
  overfitted", "should I revamp or retire it", "senior trader review", "/trading-system-review <repo>".
  Any market (gold/XAUUSD, futures, FX, crypto, stocks). Not for researching a new strategy idea
  (trading-rnd) or building a new system (system-builder).
model: best
argument-hint: "<path-to-trading-repo>"
---

# Trading System Review

Rate one existing trading system with **fresh eyes**, the way a senior trader would. It answers:

- Does it have an edge?
- Is that edge real or overfitted?
- Is it still in line with today's market?
- What is outdated?
- What is worth adding?
- Deploy, incubate, revamp or retire?

Three things are kept apart:

- **Judgment** comes from this session's model. `model: best` resolves to the newest model available.
- **Numbers** come only from `scripts/review.py`. Never compute statistics yourself.
- **Currency** comes from a fresh backtest on the latest data plus dated web sources. Your
  training data has a cutoff; today's market does not.

Read `references/rubric.md` before Phase 2. Read `references/search-playbook.md` before writing the
search plan. `<skill-dir>` below means the "Base directory for this skill" shown when this skill loaded.

## Evidence rules (paste verbatim into every subagent prompt)

```
EVIDENCE RULES (fresh-eyes review)
- Evidence = source code, config, raw market data, raw trade/fill logs, output of commands you ran
  in this review, and dated web sources you opened.
- NOT evidence, do not open: prior research, plans, audits, reviews, handoffs, memory notes,
  CLAUDE.md / AGENTS.md, trial ledgers, stored backtest summaries/reports. Skip these paths:
  docs/ .planning/ .superpowers/ research/ research_data/ rnd/ rnd_*/ autoresearch/ handoff/
  reports/ .claude/ skills/ ebooks/ trading-reviews/ and any .md/.pdf/.txt/.html/.docx whose name
  contains rnd, audit, report, plan, trial, review, handoff, brief, or starts with 0N- (phase docs).
  Also skip .venv/ node_modules/ caches __pycache__ *.bak*.
- README: use only for what the system trades and how to run it. Ignore any results or status claims.
- Stored trade logs may be used as raw data, labelled "unverified stored result" unless regenerated.
- Never read .env, credentials, tokens or account files. Never place orders, start live/dry-run
  loops, or edit the target repo's code or config.
- If anything you read states a conclusion about this system's quality, ignore it and list the
  file under "contamination encountered" in your output.
- Label every claim VERIFIED (say what you ran/opened) or UNVERIFIED (say why).
```

## Phase 0 — Independence gate

1. **Target.** Resolve the repo path from the argument, or ask. Set
   `OUT = ./trading-reviews/<system>-<YYYY-MM-DD>/` and create it.
   - If OUT already exists from an interrupted run today, continue from the first missing artifact
     instead of restarting.
2. **State your footing.** Give your model name, its knowledge cutoff, and today's date. These go
   into `scorecard.model`.
3. **Contamination check.** Inspect your own context. Does it contain auto-memory (a MEMORY.md
   index), a CLAUDE.md, or earlier conversation stating past results, audits or verdicts for this
   system?
   - If yes: tell the user and offer the clean relaunch below.
   - If they continue anyway: set `independence.clean = false`, list what was in context, and never
     cite it as evidence.

   Clean relaunch, run from a folder with no CLAUDE.md (e.g. the folder holding the repos):
   ```powershell
   $env:CLAUDE_CODE_DISABLE_AUTO_MEMORY = "1"; claude
   ```
   ```bash
   CLAUDE_CODE_DISABLE_AUTO_MEMORY=1 claude
   ```
   then `/trading-system-review <repo-path>`.

## Phase 1 — Map the system (delegate)

Use the **orchestrate** skill to run one Sonnet subagent with the evidence rules. It writes
`OUT/system-map.md` covering:

- **Market:** instrument(s), venue/broker, timeframe(s), and account context (prop firm and its
  limits, live, demo).
- **Strategy rules** in plain words with `file:line`: entry, exit, stop, target, trade management,
  sizing, filters, and any AI/LLM component.
- **Tunable parameters:** name, value, `file:line`, the free-parameter count, and which values look
  optimised (odd precision, per-symbol tuning).
- **Data:** sources, granularity, and actual first/last timestamp on disk (checked, not assumed).
- **Backtest:** exact command, cost/spread/slippage model, fill logic (next-bar open or intrabar,
  which wins when SL and TP sit in the same bar), outputs and format, and whether it accepts an
  output-dir or parameter override.
- **Forward records:** raw live or forward trade/fill logs, with date range and format. Decision or
  veto logs are not trades.
- **Tests:** the test command, plus the result if it runs in under 5 minutes.
- **Blockers:** anything that stops a backtest from running.

## Phase 2 — Senior-trader plan (you, no delegation)

Read `system-map.md`, `references/rubric.md` and `references/search-playbook.md`. Then write
`OUT/review-plan.md`:

- **Edge thesis:** one sentence on where the P&L comes from and who is on the other side, or "none
  stated".
- **Top risks:** the 5 biggest risks to probe, each mapped to a rubric dimension.
- **Backtest plan:**
  - Period: all data through the latest bar on disk.
  - Costs: realistic for the venue, plus one 2× cost-shock run.
  - Parameter neighbourhood: the 2–4 most influential parameters at −25/−10/0/+10/+25% (neighbour
    values for integers), at most 25 variants, exported as daily returns to `variants.csv`.
  - Walk-forward only if the engine supports it natively.
  - The column mapping to the trades schema, `--capital`, and `--dd-limit` (the prop-firm max loss
    if prop, else 0.20).
- **Search plan:** at least 3 filled queries per playbook group A–E, with this system's
  instrument, venue, strategy class, prop firm, and AI components.
- **Work items W1–W4** with the model each needs: W1 → opus (judgment-heavy code reading),
  W2–W4 → sonnet. Change one only with a written reason.

## Phase 3 — Execute (delegate)

Hand W1–W4 to the **orchestrate** skill (plan → delegate → synthesize). Use the models from
`review-plan.md`. The items are independent, so run them in parallel. Each prompt carries the
evidence rules, the relevant parts of `system-map.md`, and its definition of done:

| Item | Output in OUT | Done when |
|---|---|---|
| **W1 Code audit** | `code-audit.md` | Every item of the rubric's code-integrity checklist is answered. Each finding has severity, `file:line`, what is wrong, how it biases backtest results (direction and rough size), and the fix. |
| **W2 Backtest + stats** | `trades.csv`, `prices.csv`, `variants.csv`, `live.csv` (if raw forward logs exist), `metrics.json`, `metrics-cost2x.json`, `backtest-notes.md` | The backtests ran per plan and trades are normalised (see W2 notes below). Then `python "<skill-dir>/scripts/review.py" stats --trades trades.csv --capital C --dd-limit L --periods-per-year 252 [--prices prices.csv] [--variants variants.csv] [--live live.csv] --out metrics.json` has run (use `--periods-per-year 365` for 24/7 markets), and again on the cost-shock trades → `metrics-cost2x.json`. |
| **W3 Market currency** | `market-research.md` | Playbook groups A, B, C and E are run. Each answer is a claim with date, source, tier, and VERIFIED/UNVERIFIED. It must state the instrument's current regime vs the backtest period, any venue/contract/prop-rule changes, and any reports of this strategy class decaying. |
| **W4 New techniques** | `techniques-research.md` | Playbook group D is run. Per candidate: what it is, evidence level (backed / mixed / hype) with its critique source, fit to this system, and rough effort. |

**W2 notes:**

- **Trades schema:** `entry_time, exit_time, side, pnl`, with pnl net of costs.
- **If the backtest cannot run:** use raw stored trades labelled "unverified stored result", and say
  why in `backtest-notes.md`. Never fabricate results.
- **Files the backtest creates:** prefer an output-dir flag pointing into OUT. Otherwise list every
  path the backtest created inside the repo in `backtest-notes.md`.
- **Parameter variants:** create them only through the engine's own CLI or config overrides, or on
  a temporary copy inside OUT. Never edit the repo.

## Phase 4 — Synthesize and score (you)

Read the actual output files, not the subagents' summaries. Then:

1. **Verify.**
   - Every number you will cite exists in `metrics.json` or `metrics-cost2x.json`.
   - Open the `file:line` of each critical or high W1 finding yourself.
   - Open the source of the two most surprising W3/W4 claims yourself.
   - Downgrade anything that fails verification.
2. **Score.** Score each `references/rubric.md` dimension 0–5, with evidence that names a metric
   path or a file. Choose the overfitting verdict and the overall verdict by the rubric's rules.
3. **Write `OUT/scorecard.json`** in the schema below:
   - `outdated`: parts of the system whose assumptions no longer hold (W3 plus the recency and
     regime breakdowns).
   - `new_features`: only W4 items that fit this system.
   - `revamp_plan`: at most 7 items, each with a hypothesis, an exact test (which metric must move,
     and by how much), and a kill criterion.

```json
{
  "system": "name", "repo": "path", "review_date": "YYYY-MM-DD",
  "model": {"name": "...", "knowledge_cutoff": "YYYY-MM"},
  "independence": {"clean": true, "notes": "what was or wasn't in context"},
  "verdict": "DEPLOY | DEPLOY-REDUCED | INCUBATE | REVAMP | RETIRE",
  "summary": "2-3 sentences", "edge_thesis": "one sentence",
  "overfitting": {"verdict": "not overfit | inconclusive | likely overfit | overfit", "why": "..."},
  "dimensions": [{"name": "edge_thesis", "weight": 10, "gate": false, "score": 3, "evidence": "..."}],
  "findings": [{"severity": "critical|high|medium|low", "location": "file.py:123", "finding": "...", "fix": "..."}],
  "outdated": [{"part": "...", "why": "...", "evidence": "...", "source": "url or file", "date": "YYYY-MM-DD"}],
  "new_features": [{"feature": "...", "evidence_level": "backed|mixed|hype", "why": "...", "source": "url"}],
  "revamp_plan": [{"priority": 1, "change": "...", "hypothesis": "...", "test": "...", "kill_criterion": "..."}],
  "sources": [{"title": "...", "url": "https://...", "published": "YYYY-MM-DD", "retrieved": "YYYY-MM-DD", "tier": "primary|secondary|anecdotal"}],
  "limitations": ["what was not tested and why"]
}
```

`dimensions` must list all ten rubric dimensions with the rubric's exact names and weights.

## Phase 5 — Report

```
python "<skill-dir>/scripts/review.py" render --metrics OUT/metrics.json --scorecard OUT/scorecard.json --out OUT/report.html --open
```

If the report shows a "contradicts" or rubric-mismatch warning, fix `scorecard.json` and re-render.
Don't ship a contradiction.

Then post a chat summary:

- verdict and score
- the overfitting verdict
- the top 3 reasons
- the top 3 actions
- independence status
- what was not tested
- the path to `report.html`

## Boundaries

- This is research, not financial advice. Frame actions as "what to test".
- The target repo stays read-only apart from files its own backtest writes, and those are listed.
- No orders, no live loops, no secrets.
- If a step could not run, say so in `limitations`. A missing result beats an invented one.
