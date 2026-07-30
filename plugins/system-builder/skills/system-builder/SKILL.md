---
name: system-builder
description: Phase-gated workflow for building a new system or project end to end — Phase 0 kickoff interview, Phase 1 multi-agent RND across web/GitHub/Reddit/social media (via the orchestrate skill), Phase 2 detailed planning, Phase 3 code execution with subagents, Phase 4 review, testing, and demo walkthrough. Use this skill whenever the user wants to build a new system, start a new project, kick off RND for an idea, or says things like "let's build X", "new system", "start phase 1", "run the phases", or "do RND on this" — even if they never mention this skill by name.
---

# System Builder

Run new-system projects through five ordered stages: Kickoff Interview → RND → Plan → Execute → Review. Never jump ahead, and never skip a stage. The `docs/` folder is the project's memory: every phase reads the documents written by earlier phases and writes its own, so any phase can resume in a fresh session without the user re-explaining anything.

## Roles and models

Act as the **commander** throughout — the expensive reasoning model this session runs on (Fable or Opus). Delegate all heavy research and coding to **Sonnet subagents** through the **`orchestrate` skill's** delegate protocol:

- Dispatch via the Agent tool with `model: "sonnet"` explicitly set — never omit `model`, or the agent inherits this session's expensive model.
- Batch all independent missions into a single message with multiple Agent calls so they run concurrently. Sequence only real dependencies (research before implementation, implementation before its own review).
- Compose each subagent a **self-contained prompt**: its character role (e.g., "open-source scout"), the mission, the relevant paths/sources already known from the plan, and what "done" looks like. Never make an agent re-derive decisions the commander already made.
- Per orchestrate's synthesize step, read each agent's actual output/diff — a summary describes intent, not necessarily what happened — and run verification yourself.
- Per orchestrate's skip rule: if a piece of work is trivial or has no real decomposition, do it directly rather than forcing a fake parallel split.

If orchestrate is not installed, apply these same conventions with general-purpose subagents via the Task tool.

Why this split matters: subagents burn their own context windows on raw searching, reading, and coding, returning only distilled results, while the commander's expensive context stays reserved for direction, synthesis, and quality control.

## Phase 0 — Kickoff & Interview

1. Create `docs/` in the project root if it doesn't exist.
2. Ask the two configuration questions (use the AskUserQuestion tool if available):
   - **Gate mode** — (a) *Manual gates*: hard stop after Phase 1 and after Phase 2; the user must approve before continuing (Phases 3→4 then flow automatically). (b) *Full auto*: a dedicated **Approver subagent** reviews each phase's output document against the checklist at the bottom of this file and either approves it or sends it back for revision; the user is notified at each gate but not blocked.
   - **Phase 3 execution style** — parallel subagents (capped at ~3 concurrent coding agents so the results stay reviewable) or one-by-one sequential. This genuinely varies per project, so always ask; never assume.
3. **Interview until ~90% understanding.** Ask batched, numbered questions covering: the goal and the problem it solves, target users, must-have vs nice-to-have scope, direction and constraints (stack, integrations, budget, deadline), and success criteria. Critical or uncomfortable questions are explicitly welcome — the user prefers hard questions now over misdirection later. Keep interviewing in rounds until you can restate the entire flow, how it will be done, and which direction it is heading, with honest ≥90% confidence.
4. Restate your understanding to the user, state your confidence, and get a "yes, that's it" before proceeding.
5. Write `docs/00-BRIEF.md`: the confirmed understanding, gate mode, execution style, scope, constraints, success criteria, and any assumptions still open. This file is the contract every later phase is checked against.

## Phase 1 — RND (Research & Discovery)

Goal: capture all knowledge and information already available online before designing anything.

1. Derive 4–8 research missions from the brief. Typical missions: existing solutions and competitors; relevant GitHub repos, libraries, and frameworks; Reddit/forums/social media for real user pain points and sentiment; best-practice architectures for this kind of system; API/pricing/licensing constraints; pitfalls and failure stories people report.
2. Dispatch all missions in one batched message via orchestrate's delegate protocol (`model: "sonnet"`): one subagent per mission, each prompt self-contained — a character role (e.g., "open-source scout", "community listener", "competitor analyst"), the sources it must cover (web, GitHub, Reddit, X, blogs, official docs), the specific questions it must answer, and a definition of done: summarized findings with source links, never raw dumps. Research missions are independent, so they all run in parallel.
3. Synthesize all findings into `docs/01-RND.md` following `references/rnd-report.md`. Resolve conflicts between subagent reports; spot-check any surprising claim with your own quick search before it goes in the report.
4. **Gate.** Manual mode: present the report and stop until the user approves. Auto mode: run the Approver subagent, revise until it passes, notify the user, and continue.

## Phase 2 — Detailed Plan

Read `docs/00-BRIEF.md` and `docs/01-RND.md` before writing anything.

1. Write `docs/02-PLAN.md` following `references/plan-template.md`: architecture overview, tech stack with justification that cites specific RND findings, then milestones broken into **vertical slices** — each slice cuts through all layers (data + logic + interface) and produces something runnable and testable. Avoid horizontal phasing ("all DB first, then all API, then all UI"), which delays end-to-end feedback.
2. Give every slice: tasks sized for a single subagent, acceptance criteria, and its own **test gate** — the specific tests that must pass before the slice counts as done. Do not defer all testing to Phase 4.
3. **Double-validation**: before presenting, spawn one plan-reviewer subagent with fresh eyes and instructions to attack the plan — gaps, wrong ordering, hidden dependencies, unstated assumptions. Fold in the valid criticism.
4. **Gate**: same mechanism as Phase 1.

## Phase 3 — Code Execution

1. Read the approved plan. Dispatch coding subagents through orchestrate using the execution style chosen at kickoff. In parallel mode, cap at ~3 concurrent agents and only parallelize slices that do not touch the same files. In sequential mode, complete one slice fully before starting the next.
2. Each subagent's assignment is exactly one slice, with its acceptance criteria and test gate attached. Require **evidence**: the subagent must run the slice's tests and report the actual test output. Then verify per orchestrate's synthesize step — read the actual diff and re-run the slice's test gate (plus build/lint) yourself. Never accept "it works", and never trust a self-report you haven't reproduced.
3. Log every dispatch and result in `docs/03-EXECUTION-LOG.md` (slice, agent role, status, test evidence, follow-ups) as you go — this log is how a fresh session resumes mid-execution.
4. If a slice fails twice with the same approach, stop looping: either take the slice over directly as commander or return to the plan and re-scope that slice.

## Phase 4 — Review, Testing & Demo

1. Review the entire workflow and codebase with fresh reviewer subagents: bugs, security issues, dead or duplicated code, and divergence from the plan.
2. Run the full test suite. Then write and run **scenario walkthrough test cases** that demo the environment end to end in different realistic scenarios — happy path, edge cases, and failure modes.
3. Fix what is found and re-run until green.
4. Write `docs/04-REVIEW.md` following `references/review-template.md`: findings, fixes applied, full test evidence, the scenario walkthrough results, known remaining issues, and suggested next steps. Present it to the user — Phase 4 always ends with the user, even in full-auto mode.

## Resuming a project

If this skill is invoked in a project that already contains `docs/` phase files, read them first, state which phase is complete and what comes next, confirm with the user, then continue from that point. Never restart Phase 0 unless `docs/` is missing or the user asks for a restart.

## Approver subagent checklist (full-auto mode)

The Approver approves a phase document only if all of these hold:

- It fully serves the brief (`docs/00-BRIEF.md`), with no unanswered question that blocks the next phase.
- Claims are sourced (Phase 1), decisions are justified (Phase 2), and evidence is attached (Phases 3–4).
- The logic is complete: no contradictions, no missing steps between inputs and outcomes.
- A stranger could execute the next phase from this document alone.

Otherwise it returns the document with specific revision instructions. Maximum two revision loops per gate; after that, escalate to the user instead of looping.
