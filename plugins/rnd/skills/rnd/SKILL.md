---
name: rnd
description: General-purpose R&D investigation for any domain — software systems, tools, frameworks, techniques, product features, infrastructure, workflows, trading, or any "research it first, then develop it" topic. Use whenever the user types /R&D or /rnd followed by a topic, or asks to research, investigate, explore, or deep-dive something new. Note; for topics about the user's US-stocks auto trading system (strategies, indicators, trading features), the trading-rnd skill is the more specialized choice — prefer it when it is available, and handle those topics here otherwise.
---

# R&D Explorer

Turn a one-line topic in any domain into a decision-ready research report. The user is a
software engineer who self-learns by investigating new areas before building. The end
goal of every run is the same: **"should I pursue this, and what exactly would I do
next?"** — with the research done here and the code-level planning/implementation done
later in Claude Code.

This skill is deliberately lighter than a domain-specific one. The user's prompt (and
their answers to your questions) carry the domain detail; this skill carries the method.

## Phase 1 — Sharpen the target

The single biggest quality lever for general R&D is a sharp brief. Judge the prompt:

- **Already specific** (clear subject, clear purpose, clear context — e.g., a detailed
  paragraph about what they want and why): don't interrogate them. State your
  interpretation in one or two sentences and proceed.
- **Broad or ambiguous** (e.g., "/R&D vector databases", "/R&D home lab monitoring"):
  ask clarifying questions **once, as a single batch of 2–4 questions**, then wait for
  answers before researching. Never drip questions across multiple turns. When the
  interface provides interactive option widgets for questions, use them — tappable
  choices get better answers than asking the user to type.

Choose questions that most change what you'd research. The usual high-leverage ones:

1. **Goal** — learn the area broadly, evaluate options to pick one, or prepare to build
   something specific?
2. **Context** — where would this be used (personal project, work system, new idea)?
   What already exists that it must fit with?
3. **Constraints** — budget, self-hosted vs managed, timeline, must-have capabilities,
   things already ruled out.
4. **Deliverable depth** — quick landscape overview vs deep comparison vs
   build-ready recommendation.

Skip any question the prompt already answers. After the answers arrive, restate the
refined brief in 2–3 sentences ("So the target is: …") so the user can correct course
cheaply, then start.

## Improvement topics

"Improve/optimize my existing X" is a valid topic shape in any domain — a service, a
pipeline, a homelab setup, a workflow. Two extra rules apply. First, understand the
current state before researching fixes: pull it from the prompt, uploaded files, or
project knowledge; if how X currently works isn't available anywhere, ask for a short
description **plus the symptoms** that prompted the wish to improve (slow, flaky,
costly, noisy, hard to maintain) — fold this into the same Phase 1 question batch, not
a separate round. Second, research targeted fixes for the diagnosed causes, not generic
best-practice listicles. In the report, reframe the template accordingly: section 2
becomes current state & diagnosis, section 3 becomes prioritized improvement candidates
(each with a hypothesis and a way to test it), and the verdict names the top
recommendation.

## Phase 2 — Scope

Break the refined brief into 4–6 concrete sub-questions before searching. Typical axes:
what the thing is and how it works, the main approaches/options and their trade-offs,
what it requires (infrastructure, data, cost, prerequisite knowledge), what practitioners
report going wrong, and what the current state of the art / active development looks like.

## Phase 3 — Gather

Research the sub-questions across source types deliberately — each answers a different
kind of question:

- **Web search** — the landscape: overviews, comparisons, recent developments. Start
  broad (1–2 word queries), then narrow.
- **GitHub** — reference implementations and tool maturity. Fetch READMEs of the most
  promising repos; judge by stars, recent commit activity, open-issue health, and docs
  quality. Prefer 3–5 well-assessed options over a long link dump. `api.github.com` can
  be queried directly for structured data when available.
- **Community threads** (relevant subreddits, Hacker News, Stack Overflow/StackExchange
  sites for the domain) — the reality check. Official pages oversell; threads reveal
  production pain, migration regrets, and gotchas nobody documents. If a direct fetch
  is blocked, search for summaries or cached discussions rather than dropping this
  source class.
- **Official docs** — for any product, API, or library involved: confirm real
  capabilities, limits, and pricing at the source rather than second-hand claims.

Depth expectations: typically 5–10 searches plus several full-page fetches, scaled to
the deliverable depth the user chose in Phase 1. Fetch full pages for anything
load-bearing. Cross-check important claims across at least two independent sources and
record disagreements instead of silently picking a side. Stop when the sub-questions
are answered or clearly unanswerable, not at an arbitrary count.

**Use the full toolkit, not just search.** Code execution is available: query
`api.github.com` directly (repo search, stars, last-commit dates, open-issue counts)
for objective maturity stats instead of eyeballing search snippets, and crunch gathered
numbers (pricing tiers, benchmark figures, feature matrices) into a small comparison
table for the report. If network access happens to be restricted in the current
environment, fall back to web search/fetch without fuss.

**Recency discipline.** For fast-moving areas, include the current year in searches,
weight sources from the last 12–18 months, and date-stamp the key sources in the
report — a stale comparison of an active field misleads more than it informs.

**Scope honestly.** If genuine coverage would need 20+ searches (e.g., "/R&D the
entire MLOps landscape"), say so up front: offer a usefully scoped version now, and
mention that the platform's deeper Research feature suits the full sweep — let the
user choose rather than silently under-delivering.

## Phase 4 — Report

Write the report using the template in `references/report-template.md` (read it at this
point). A fixed structure keeps every run comparable so the user builds a personal
research library across domains.

Non-negotiable qualities:

- **Evidence, not vibes.** Attribute claims to linked sources; distinguish "the vendor
  claims" from "multiple practitioners report".
- **Honest trade-offs.** For option comparisons, say what each choice costs, not just
  what it offers. Favor boring, low-maintenance options for solo-maintained projects
  unless the user signals otherwise.
- **Calibrated verdict.** State confidence (high/medium/low) in the verdict and name
  the one or two findings that would most change it — this tells the user exactly what
  to verify or watch before committing.
- **Ends in action.** The final section is a concrete next step **plus a ready-to-paste
  Claude Code handoff prompt** containing the chosen direction, constraints, and first
  milestone. Keep the handoff free of code-level prescriptions — Claude Code will
  inspect the actual environment/codebase and plan implementation itself.

Save the report as `rnd-<topic-slug>-<YYYY-MM-DD>.md` and present the file so the user
can archive it. Also give a 3–5 sentence verdict summary in chat — the conclusion
should be readable without opening the file.

## Update mode

If the user asks to refresh a topic ("/R&D update <topic>") or a past report on the
same topic is available (in project knowledge or uploaded), read it first and run a
delta investigation instead of starting over: what changed since its date, new options
that appeared, options that died or stalled, and whether the old verdict still holds.
Lead the new report with a "What changed" section and revise the verdict explicitly.
This turns the user's research library into a living one instead of a pile of
snapshots.

## Boundaries

Produce research and recommendations, not guarantees — frame conclusions as "what the
evidence supports testing/building first". If the user asks to jump straight into
building, finish (or explicitly offer to skip) the report first so the build is
informed, then hand off to Claude Code for planning and execution.
