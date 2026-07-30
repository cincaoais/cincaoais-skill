---
name: trading-rnd
description: Deep R&D investigation pipeline for topics about the user's US-stocks auto trading system — trading strategies, indicators, market data, broker capabilities, risk management, backtesting, or new features for the trading system. Researches across the web (search engines, GitHub, Reddit, Hacker News, official docs) and produces a structured report with a feasibility assessment against the user's system. Use when the user types /R&D or /rnd with a trading-related topic, or asks to research/investigate a strategy or trading-system feature — e.g. "/R&D mean reversion strategies", "investigate real-time risk monitoring for my trading system", "research pairs trading". For non-trading R&D topics, the rnd skill handles those instead.
---

# R&D Investigator

Turn a one-line topic into a decision-ready research report. The user is a software engineer who self-learns by investigating new features and trading strategies, and who runs a personal US-stocks auto trading system. Every investigation should end by answering one practical question: **"should I build this, and if so, how?"** — not just "here is what the internet says."

## Phase 0 — Load context

Read `references/my-system.md` first. It describes the user's trading system at the domain level (broker, data sources, validation process, live strategies, constraints — deliberately no code-level details, which Claude Code discovers itself later). Every report's fit assessment is written against this file. If it still contains unfilled placeholders, continue anyway, but note in the report which fit conclusions are assumptions and gently remind the user they can fill the file in for sharper assessments.

## Phase 1 — Classify and scope

Classify the topic into one of three types, since each needs different sub-questions and a different report template:

- **Strategy** — a trading approach (e.g., mean reversion, pairs trading, momentum, options wheel). Quant-flavored.
- **Feature** — a capability for the system (e.g., risk dashboard, order-execution improvement, alerting, data pipeline). Engineering-flavored.
- **General tech** — pure self-learning topics not tied to the trading system (e.g., a new framework or ML technique). Use the feature template minus the trading-specific sections, and make the fit assessment about the user's skills/stack rather than the trading system.
- **Improve** — upgrading something that already exists in the system (e.g., "improve my momentum strategy", "reduce drawdown on X", "make my alerting less noisy"). Diagnosis-flavored; follow the Improve mode section below instead of the standard flow.

Then break the topic into 4–6 concrete sub-questions before searching. Scoping first prevents shallow, unfocused gathering. For example, "/R&D mean reversion on US equities" might scope into: what signal definitions are common, what data granularity it needs, how practitioners backtest it, known failure modes, reference implementations, and why any edge would persist today.

If the topic is genuinely ambiguous (can't tell what the user means at all), ask one clarifying question before starting. Otherwise don't interrupt — state your interpretation in the report intro and proceed.

## Improve mode

Improvement runs differ from fresh research in one crucial way: understand the current implementation and its symptoms **before** researching fixes — "improve" without a diagnosis is just redecorating.

1. **Acquire the current definition.** Check in order: the prompt itself, uploaded files, project knowledge (past R&D reports on this strategy/feature), and `references/my-system.md`. This skill cannot see the user's codebase — if the actual rules (entry/exit logic, universe, holding period, sizing) aren't available from those sources, ask the user to paste a short summary rather than guessing from the strategy's name.
2. **Get the symptoms.** If not already stated, ask what prompted the improvement wish: backtest-vs-live gap, drawdowns too deep, whipsaws in ranging markets, costs eating returns, missed fills, noisy alerts. Combine this with step 1's request into **one** batch of questions. Symptoms decide what to research.
3. **Diagnose, then research targeted fixes.** Map symptoms to candidate causes and research those specifically — e.g., whipsaw → regime filters; deep drawdowns → exit/stop and position-sizing research; cost drag → execution tactics and turnover reduction — plus what practitioners report actually helping for this strategy class. Generic "10 ways to improve X" listicles are the trap to avoid.
4. **Report with Template C** in `references/report-templates.md`: prioritized improvement candidates, each with a hypothesis, an exact comparison test, and a kill criterion — ending in the Claude Code handoff that implements the experiments against the real codebase.

## Phase 2 — Gather

Research the sub-questions using multiple source types. Different sources answer different questions, so hit them deliberately rather than stopping at the first decent search results:

- **Web search** — the landscape: overview articles, comparisons, tutorials, recent developments. Start broad (1–2 word queries), then narrow.
- **GitHub** — reference implementations. Search for repos, then fetch READMEs of the most promising ones. Judge quality by stars, recent commit activity, open-issue health, and documentation quality. Prefer 3–5 well-assessed repos over a list of 15 links. When available, `api.github.com` can be queried directly for structured repo data.
- **Community threads** (r/algotrading, r/quant, r/datascience, Hacker News, Stack Overflow, Quantitative Finance StackExchange) — the reality check. Blog posts oversell; forum threads reveal what breaks in production, live-trading results vs backtest results, and gotchas nobody documents. If a direct fetch is blocked, search for summaries or cached discussions instead of giving up on this source class.
- **Official docs** — for any broker API, data vendor, or library involved: confirm actual capabilities, rate limits, and costs from the source rather than second-hand claims.

Depth expectations: a real investigation typically needs on the order of 5–10 searches plus several full-page fetches. Fetch full pages for anything load-bearing — snippets are not enough to assess a repo or a strategy. Cross-check important claims across at least two independent sources, and record where sources disagree instead of silently picking one.

Stop gathering when the sub-questions are answered or clearly unanswerable — not when a fixed search count is hit.

**Use the full toolkit, not just search.** Code execution is available: query `api.github.com` directly (repo search, stars, last-commit dates, open issues) for objective repo-maturity stats instead of eyeballing snippets, and turn gathered numbers (data-vendor pricing, broker fee schedules, feature matrices) into a small comparison table. For strategy topics, small simulations on **synthetic data** can make mechanics concrete — e.g., how transaction costs and slippage erode a given win-rate/turnover profile, or how position sizing changes drawdown shape. Label these clearly as illustrations of mechanics, never as backtests: the sandbox has no real market data, and real backtesting belongs to the user's own validation process. If network access happens to be restricted, fall back to web search/fetch without fuss.

**Recency discipline.** Broker offerings, data-vendor pricing, and market structure change fast. Include the current year in searches for anything product- or cost-related, weight practitioner reports from the last 12–18 months, and date-stamp key sources in the report.

## Phase 3 — Evaluate fit

Assess the findings against `references/my-system.md`:

- **Data**: does this need data (granularity, asset classes, fields like options chains or fundamentals) the system already ingests? If not, what's the cheapest way to get it?
- **Execution model**: is the required trading frequency/latency compatible with the system's loop and broker?
- **Implementation effort**: concept-level sizing only — what components are new vs modified and rough order of work. Stay at the design level; code-level planning and implementation happen later in Claude Code, which inspects the actual codebase itself.
- **Risk**: for strategies, what could make it lose money in live trading; for features, what could break existing behavior.

## Phase 4 — Report

Write the report using the exact matching template in `references/report-templates.md` (read it at this point). Templates keep every run comparable so the user can build a personal research library.

Non-negotiable qualities of a good report:

- **Skepticism over hype, especially for strategies.** Public strategies are mostly decayed alpha — if it's free on GitHub with thousands of stars, assume the easy edge is gone. Every strategy report must answer "why would this edge still exist?" honestly, and treat found strategies as learning material and building blocks rather than plug-and-play systems.
- **Evidence, not vibes.** Attribute claims to sources (link them). Distinguish "the author claims" from "multiple practitioners report".
- **Calibrated verdict.** State confidence (high/medium/low) and name the one or two findings that would most change the verdict — for strategies this is often a data-cost discovery or a practitioner report of live decay; make it explicit so the user knows what to verify first.
- **Ends in action.** The final section is always a concrete starter plan — first thing to build, first experiment/backtest to run, a measurable success criterion — plus a ready-to-paste Claude Code handoff prompt with the chosen approach, requirements, and first milestone. Keep the handoff free of code-level prescriptions; Claude Code plans against the real codebase itself.

Save the report as a markdown file named `rnd-<topic-slug>-<YYYY-MM-DD>.md` and present it to the user so they can download and archive it. Also give a 3–5 sentence verdict summary in the chat — busy-day readers should get the conclusion without opening the file.

## Update mode

If the user asks to refresh a topic ("/R&D update <topic>") or a past report on the same topic is available (in project knowledge or uploaded), read it first and run a delta investigation instead of starting over: what changed since its date — new tools or data offerings, pricing changes, fresh practitioner reports of the edge decaying or persisting — and whether the old verdict still holds. Lead the new report with a "What changed" section and revise the verdict explicitly. Strategy verdicts in particular have a shelf life; treating past reports as refreshable keeps the research library honest.

## Boundaries

This skill produces research and feasibility analysis, not financial advice — never present a strategy as a recommendation to trade real money, and keep the framing "here is what to test" rather than "this will be profitable". If the topic drifts outside research (e.g., "just build the whole feature now"), that's fine — finish the report first so the build is informed, unless the user explicitly says to skip it.
