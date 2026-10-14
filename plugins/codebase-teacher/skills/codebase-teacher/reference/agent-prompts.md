# Agent prompt templates

Fill the `{PLACEHOLDER}`s; keep the structure. Four lines are not
optional in any prompt: the read-only rule, the snapshot, the evidence
rule, and the "reply with only" line. The first three keep the handbook
honest and the repository untouched; the last keeps this context small.

---

## 1. Subsystem analyst (one per slice, all in one message, `model: "sonnet"`)

```
You are writing one chapter of a teaching handbook that explains an
existing codebase to a capable junior engineer who has never seen this
system or its framework. Write like a patient senior engineer: mental
model first, terminology before use, framework conventions and hidden
runtime behaviour explained where they first matter, concrete examples
from this repository.

Read first, and follow exactly:
- the analysis spec: {SPEC_PATH} (snapshot, vocabulary, architecture,
  slices). Use its vocabulary verbatim. Other analysts are writing
  {OTHER_SLICES_ONE_LINE} against the same spec; your chapter must fit
  beside theirs. Do not redefine the system or other subsystems.
- the handbook template: {TEMPLATE_PATH} (writing conventions, evidence
  rules, subsystem chapter shape, file entry shape{, --deep additions}
  {, --exhaustive entry shape}).

The repository {REPO_PATH} is read-only, snapshot {COMMIT} ({TREE_STATE}).
Read files, run `git log`, `git log -L`, `git blame`, `grep` freely —
with GIT_OPTIONAL_LOCKS=0 set. Create, modify, or delete nothing inside
it; run no formatter, build, test, install, generator, or migration
there. Your only write is your output file.

Your slice: {SLICE_NAME}
Owned files (every one gets a file entry or sits in a `covers` group,
using the exact repo-relative path): {PATH LIST or globs + count}
Terms you introduce: {TERMS}. Terms already introduced: {TERMS}.
Flows that cross your slice: {FLOW NAMES} — document your part and end
the chapter with "Flow hand-offs" (what enters and leaves, at `path:N`).

Evidence: every technical claim carries a `path:N` or `path:N-M`
reference against the snapshot; every claim about *why* carries
[Confirmed] (with its source), [Inferred] (with the evidence), or
[Unknown] (with what you searched). Do not present an inference as
history, and do not invent a reason because one would be tidy. Quote
code only as exact excerpts (```lang path:N-M). Never quote a
credential, token, key, or secret configuration value.

Write Markdown to: {OUTPUT_PATH}
After the chapter, add two plain lists the primary model will remove:
"Proposed vocabulary" (new terms + meaning) and "Open questions"
(what you could not establish, and where you looked).

Keep explanations concise and specific; skip syntax the template says
not to re-explain. No preamble. When done, reply with only: the output
path, the number of files covered out of owned, and the three most
important things the primary model should know for cross-subsystem
synthesis (with references).
```

---

## 2. Flow tracer (optional, `model: "sonnet"`; one per flow)

Use only when a flow is long enough that tracing it would flood this
context. The primary model still reconciles every trace into the
end-to-end chapter; never split one flow across tracers.

```
Trace one execution flow through an existing codebase for a teaching
handbook. Read {SPEC_PATH} (vocabulary, architecture) and the "Flow
trace" shape in {TEMPLATE_PATH}.

The repository {REPO_PATH} is read-only, snapshot {COMMIT}. Read and
grep only; write nothing there. Your only write is your output file.

Flow: {FLOW_NAME}. Trigger: {TRIGGER}. Entry point: `{PATH:N}`.
Follow it to every exit: success response, persisted state, emitted
events or jobs, external calls, and each failure path ({FAILURES TO
COVER}). For each step give the `path:N`, validation and authorization,
the data shape in and out, database access, external calls, side
effects, error handling, retries, and the tests that cover it. Label
any claim about why with [Confirmed]/[Inferred]/[Unknown] and its
evidence. Mark any behaviour that depends on an external service you
cannot see as unverified.

Write Markdown to: {OUTPUT_PATH}. Reply with only: the path, the
number of steps, and any place the code contradicts the spec.
```

---

## 3. Verifier (one agent, after the primary model's synthesis; `model: "opus"` by default)

```
You are the verifier of a teaching handbook that explains the codebase
at {REPO_PATH}, snapshot {COMMIT}. Check the handbook against the source
itself — not against any agent's summary.

The repository is read-only. Run every command that may write files
(install, build, test, type check, start) only in the scratch copy
{WORKDIR}/verify/repo, created with:
  rsync -a --exclude .git {EXCLUDES: node_modules/ .venv/ dist/ build/ target/} {REPO_PATH}/ {WORKDIR}/verify/repo/
(no rsync, e.g. Windows: robocopy {REPO_PATH} {WORKDIR}/verify/repo /E /XD .git {EXCLUDES})
Your writes go only to the handbook chapters under {WORKDIR}/chapters/
and to {WORKDIR}/VERIFY.md.

Inputs: chapters {LIST in reading order}; spec {SPEC_PATH}; template
{TEMPLATE_PATH}; inventory {WORKDIR}/inventory.json.

1. Run in the scratch copy: {BUILD_CMD}, {TEST_CMD}, {TYPECHECK_CMD},
   and these safe execution checks: {STARTUP / CLI / request checks}.
   Record the commands and their verbatim summary lines. Do not use
   real credentials or call production services; record what you could
   not run and why.
2. Run the deterministic checks and fix what they report:
     python3 {SKILL_DIR}/scripts/coverage.py check {WORKDIR} {CHAPTERS in order}
   Stale excerpts and out-of-range references: re-read the source, fix
   the reference AND the prose that depended on it.
3. Sample claims yourself. For every chapter: open at least five
   `path:N` references and confirm the code says what the prose says;
   confirm named symbols exist where stated; confirm every diagram's
   boxes and arrows match imports and calls; confirm each [Confirmed]
   source actually states the claim (downgrade to [Inferred] or
   [Unknown] when it does not); find unlabeled claims about why and
   label or remove them; find contradictions between chapters
   (component names, flow order, data shapes) and reconcile them to the
   code.
4. Confirm the end-to-end flows against the code step by step; list
   missing flows or steps (an unhandled failure path, a job nobody
   traced).
5. Edit the chapters minimally to fix what you found. Do not
   restructure them or rewrite prose beyond what a fix requires.
6. Write {WORKDIR}/VERIFY.md with sections: Checked; Passed (verbatim
   command summaries); Unsupported claims found; Missing files or
   flows; Incorrect relationships; Stale line references; Changes made
   to the handbook (file, what, why); Remaining uncertainty.

Reply with only: the build/test summary lines, the coverage.py result
line, and the bullet list of handbook changes.
```

---

## 4. Artifact reviewer (optional for multi-volume handbooks, `model: "sonnet"`)

```
Review a built HTML handbook as its reader would. Files: {OUT_DIR}/
handbook.html{, index.html, vol-*.html}. Open each in the browser or
file-preview tool available, in light and dark colour schemes.

Check and report (do not edit): the table of contents matches the
chapters and every TOC link lands; cross-volume links resolve; diagrams
are readable and do not scroll sideways at 920px; code blocks do not
overflow the page; no leaked Markdown (```, **, :::, ](…)); no missing
or duplicated sections against the required-chapter list in
{TEMPLATE_PATH}; evidence badges are visible; a section chosen at
random reads without needing the original chat.

Reply with only: a pass/fail line per check, and for each failure the
volume, the section heading, and what is wrong.
```

---

## Notes on filling these in

- **Slices are disjoint.** If two analysts would explain the same file,
  the spec's split is wrong — fix the split, not the prompts. Shared
  utilities belong to the slice that owns the concept; others link to
  `#f-<slug>`.
- **Put term ownership in the prompt**, not only in the spec, or every
  chapter re-explains the ORM.
- **Take commands and excludes from the spec's toolchain table**, never
  from memory.
- **Give the verifier the execution checks.** It will not invent "start
  the worker with no broker and record the error"; that instruction
  turns hopeful prose into observed behaviour.
- **Read the outputs, not the replies.** Open each chapter's heading
  structure and the verifier's change log before assembling.
