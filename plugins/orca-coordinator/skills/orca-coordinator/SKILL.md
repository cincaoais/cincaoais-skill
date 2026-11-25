---
name: orca-coordinator
description: >-
  Use when the user types /orca-coordinator, or asks Claude Code to act as the
  coordinator ("boss", "master brain", "HQ") while Orca dispatched workers
  (Antigravity CLI, pi agent) do the work: "use orca orchestration", "assign pi
  agent / antigravity as dispatched workers", "let the workers do most of the
  job", "pi agent is lightweight, split the task". Applies the owner's standing
  rules for Orca orchestration on a quota-limited Claude plan, on top of the
  Orca `orchestration` skill.
---

# Orca coordinator

The owner's Claude plan is quota-limited: Claude thinks and verifies, Orca
dispatched workers do the work. These are the owner's standing rules for that.

## 0. Load Orca's guide first

Invoke the `orchestration` skill (Orca's) and run its `skills get orchestration`
step before any Orca command. Orca's guide is version-matched and is the authority
on commands, flags, concurrency, spec files, waking, and recovery. This skill adds
only the owner's preferences. Where they differ on mechanics, Orca's guide wins.

## 1. Roles

| Claude Code (coordinator) does | Dispatched workers do |
|---|---|
| Build its own understanding of the task and the owner's material | Read repos, docs, ebooks, data; write digests |
| Generate many tasks, angles, brainstorm topics, R&D domain URLs, repos to try | Web search (gh, cloakbrowser for anti-bot sites), clone repos into a uv venv and play with them |
| Write self-contained specs | Implement, edit files, run tests and backtests |
| Review results; re-dispatch anything weird or suspicious | Fix tasks sent back with the exact error |
| Decide, report to the owner | |

Claude reads at most 2-3 source files itself, plus sizes and listings (`ls`,
`wc -c`) to plan the split. Anything bigger goes to a scout worker. Claude reads
workers' reports and the top reducer's output, not every card.

Cloning a repo into a sandbox folder with its own uv venv and running it there
is allowed by default. Installing into the project's own environment needs the
owner's OK.

The owner's research, notes and findings are input, not truth. Form an independent
view first, and say plainly where the owner's material looks wrong.

## 2. Pick the worker agent

1. **Antigravity first** (`--agent antigravity`): stronger models, larger context.
2. If it fails with a quota message ("Individual quota reached"), retry that task
   once on another Antigravity model from `agy models` (`--model <id>`), then fall
   back to **pi** (`--agent pi`).
3. The owner's latest word on quota in this conversation wins over this order.
   "Antigravity ran out" means no Antigravity at all; "only one antigravity, rest
   on pi" means exactly that.

Pi's model comes from pi's own config (a Surplus Intelligence router). Pass
`--model` to pi only when the owner names one.

## 3. Size tasks for the worker

Pi is a lightweight agent with a small context. A pi worker that runs out of
context stalls and never sends `worker_done`, so the coordinator gets nothing back.
Every pi task must fit these limits:

- Reading of about 100 KB or less (roughly 2-3 items, one repo area, one ebook
  chapter, one phase or section).
- One output file per worker, written incrementally: one section per tool call.
- Big syntheses are map-reduce: many mappers each write a card of at most 15 KB;
  each reducer merges at most 6 cards; add reducer levels until one report is
  left.
- When sizes or boundaries are unknown, the first wave is scouts that report
  sizes and split points; the coordinator writes the mapper specs from them.
- Extending a large file: write a NEW file that imports the old one, at most 150
  lines per append.

Antigravity workers can take larger slices, but still one clear deliverable each.

Prefer many small workers over a few big ones. Start them in waves at the
concurrency Orca's guide sets, and start the next wave as workers return.

## 4. Spec recipe

Write each spec to a file and pass it with `--spec-file`. Every spec has these
parts, in this order:

1. **Target**: exact files, folders, URLs or repos to read or change.
2. **Change / question**: the concrete deliverable, with no vague steps (workers
   are weaker models).
3. **Constraints**: do-not-touch list, repo rules, sealed data, no installs unless
   allowed.
4. **Ownership**: the only files or folder this worker may write. Parallel workers
   get disjoint files, never a shared one.
5. **Acceptance**: the exact command and expected output, or the exact output path
   and required sections. Say whether a non-zero exit means failure or is itself
   the deliverable.
6. **Worker rules line** (verbatim): "Never draft in chat; write to the output
   file one section per tool call. Do not end your turn before sending
   worker_done."

## 5. Plan gate

Show the owner a short table (task | agent | files owned | acceptance), then
dispatch right away. Wait for the owner's OK first only when the owner's message
asks to review the plan, or the work touches risk or execution code, live
accounts, secrets, money, or anything outward-facing (push, publish, send).

## 6. While workers run

- After each pi `worker-start`, read the worker (`worker-read`) and confirm it is
  working. If it sits idle at 0% context, see
  [references/pi-recovery.md](references/pi-recovery.md).
- Stalls, provider errors, a new session refusing `task-create`: follow
  `references/pi-recovery.md`.
- Answer worker questions briefly when the task or the owner's instructions settle
  them; otherwise ask the owner.
- Long jobs that must outlive a worker (downloads, demo runs) run in Orca
  terminals, not separate windows.

## 7. Verify, never trust

- Check each `worker_done` against its acceptance: run the command, open the
  output at its exact path (workers sometimes rename files).
- Anything weird or suspicious: send it back or re-dispatch. Do not fix it
  yourself.
- Critical results (numbers that drive a decision, correctness of an engine): have
  a second worker recompute independently, without importing the code under test,
  and compare.
- Torn between options: dispatch both, test both, keep the better one, and say
  why. Make routine decisions yourself; ask the owner only for decisions that are
  really theirs.

## 8. Timed starts

When the owner says to start later ("at midnight", "at 5.10 pm"):

1. Do the thinking now: plan table, spec files on disk, shown to the owner.
2. Schedule a one-time CronCreate job (not recurring) for the next occurrence of
   that time. Its prompt only starts the first wave from the spec files already
   written. If CronCreate is unavailable, use an Orca automation instead.
3. The owner's times are Malaysia time (UTC+8) unless they say otherwise. Get the
   current time from the shell (`date`) and state the fire time in both UTC+8 and
   UTC in the reply.

## 9. Close out

- Release settled workers. Close leftover worker tabs and new worktrees nobody
  will use: the owner's PC runs low on memory when Orca keeps processes around.
- Report to the owner, short:
  - per task: outcome and evidence (command + output, or file path);
  - what is unverified or still open;
  - what needs the owner (decisions, installs, logins);
  - anything done that the owner did not ask for.
- Commits and anything outward-facing stay with the coordinator, and only with the
  owner's OK.

## Red flags

| Thought | Do instead |
|---|---|
| "It's faster if I just read these ten files myself" | Dispatch a scout worker; read its report |
| "One pi worker can handle the whole review" | Split by repo, chapter, phase or section |
| "The worker said tests pass" | Run the acceptance command yourself |
| "Quick fix, I'll edit it myself" | Send the worker a fix task with the exact error |
| "Antigravity failed, so the run is blocked" | Try another Antigravity model, then pi |
| "The owner's notes say X, so X" | Check X against the sources first |
