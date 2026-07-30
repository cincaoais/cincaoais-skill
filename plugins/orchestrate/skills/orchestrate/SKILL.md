---
name: orchestrate
description: "Think hard about a task using this session's active (expensive) model — Opus or Fable — to produce a concrete plan, then fan execution out to parallel Sonnet subagents for research, coding, and other well-specified grunt work, saving tokens. Use when the user types /orchestrate, or whenever they want a heavyweight-plan / cheap-execute split, ask to spin up agents to research or build several things in parallel, or describe a big multi-part task where the planning deserves the strong model but the pieces are routine execution — even if they never say \"orchestrate.\""
---

# Orchestrate: think here, execute on Sonnet

Two-phase protocol: expensive reasoning stays on this session's active model
(the user switches to Opus or Fable when they want strong thinking).
Execution fans out to Sonnet subagents to save tokens and run independent
work in parallel.

## Phase 1 — Plan (this model)

- Think hard before writing any code or dispatching anything. This is the
  expensive, high-value reasoning step — the whole point of this skill is to
  not waste it on execution that a cheaper model can do just as well.
- Produce a concrete plan: files/systems involved, sequence of changes, edge
  cases and tradeoffs.
- If something is genuinely ambiguous in a way only the user can resolve, ask
  before dispatching anything — don't let a subagent discover the ambiguity
  three levels down.
- Decompose the plan into discrete work items. For each, judge: does it need
  ongoing architectural judgment (keep it here), or is it well-specified
  execution/research a competent engineer could do from the spec alone
  (delegate)?

## Phase 2 — Delegate (Sonnet)

- Dispatch delegatable items via the Agent tool with `model: "sonnet"`
  explicitly set. Do not omit `model` — Agent otherwise inherits this
  session's (expensive) model.
- Batch everything independent into a single message with multiple Agent
  calls so they run concurrently.
- Give each agent a self-contained prompt: what to do, the relevant file
  paths/line numbers already known from the plan, and what "done" looks
  like. Don't make it re-derive the plan you already worked out in Phase 1.
- Sequence only what has a real dependency (e.g. research before
  implementation, implementation before its own review) — everything else
  goes out in parallel.

## Phase 3 — Synthesize (this model)

- Read each subagent's actual diff/output — an agent's summary describes
  what it intended to do, not necessarily what it did.
- Integrate the results, resolve conflicts between agents, and run
  verification (tests/build/lint) yourself rather than trusting subagent
  self-reports.
- Report back concisely: what changed, what's left.

## When to skip this

- Trivial, single-file, few-line changes: just do them directly. Spinning up
  subagents costs more than it saves.
- Tasks with no real decomposition (one tight change that has to happen in
  one place, in order): do it directly rather than forcing a fake parallel
  split.
