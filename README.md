# claude-skills

A personal [Claude Code](https://claude.com/claude-code) plugin marketplace. Skills live in git,
so adding the marketplace once on each machine or account keeps them updated from a single source
of truth.

- **Repo:** [`cincaoais/cincaoais-skill`](https://github.com/cincaoais/cincaoais-skill) (public)
- **Marketplace name (used in install commands):** `claude-skills`

---

## Contents

- [Install](#install)
- [The eight plugins at a glance](#the-eight-plugins-at-a-glance)
- [Which one do I use?](#which-one-do-i-use)
- [User guide](#user-guide)
  - [`/codebase-teacher`](#codebase-teacher--turn-an-existing-codebase-into-a-teaching-handbook)
  - [`/ebook-lecture-notes`](#ebook-lecture-notes--turn-a-book-into-notes-youll-actually-read)
  - [`/rnd`](#rnd--research-anything-before-building-it)
  - [`/orchestrate`](#orchestrate--plan-expensive-execute-cheap)
  - [`/system-builder`](#system-builder--build-a-whole-system-in-five-gated-phases)
  - [`/trading-system-review`](#trading-system-review--a-senior-traders-verdict-on-an-existing-system)
  - [`/skill-scout`](#skill-scout--check-for-an-existing-skill-before-a-big-task)
  - [`/smart-money-concepts`](#smart-money-concepts--a-two-book-smc-knowledge-base)
- [ebook-lecture-notes changes from upstream](#ebook-lecture-notes-changes-from-upstream)
- [Repo layout](#repo-layout)
- [Attribution](#attribution)
- [Line endings](#line-endings)

---

## Install

### 1. Add the marketplace — once per machine or account

```
/plugin marketplace add cincaoais/cincaoais-skill
```

This registers the marketplace under the name **`claude-skills`** (taken from
`.claude-plugin/marketplace.json`), which is the name every later command uses. The SSH form,
`/plugin marketplace add git@github.com:cincaoais/cincaoais-skill.git`, works too.

### 2. Install the plugins you want

```
/plugin install codebase-teacher@claude-skills
/plugin install ebook-lecture-notes@claude-skills
/plugin install rnd@claude-skills
/plugin install orchestrate@claude-skills
/plugin install system-builder@claude-skills
/plugin install trading-system-review@claude-skills
/plugin install skill-scout@claude-skills
/plugin install smart-money-concepts@claude-skills
```

Or run `/plugin` with no arguments for the interactive browser.

### 3. Restart Claude Code

Skills are loaded at session start. Restart (or run `/reload-plugins`) before expecting the new
commands to appear.

### Updating

```
/plugin marketplace update claude-skills
```

Then reinstall or update the individual plugins if a version bumped.

### Removing

```
/plugin uninstall rnd@claude-skills
/plugin marketplace remove claude-skills
```

**Plugins dropped from this marketplace** (`trading-rnd`, `find-skills`, `video-analysis`,
`web-pentest`) stay installed on machines that already have them until you uninstall them:
`/plugin uninstall <name>@claude-skills`.

### ⚠️ Watch for duplicate copies in `~/.claude/skills/`

If you previously dropped these skills straight into `~/.claude/skills/`, those loose copies stay
active after you install the plugin versions, and you end up with two of each. Check with:

```bash
ls ~/.claude/skills
```

If you see any of the plugin names below in there **and** you've installed them from this
marketplace, delete the loose directories and let the marketplace be the single source of truth.

---

## The eight plugins at a glance

| Plugin | Command | Version | What it does |
|---|---|---|---|
| `codebase-teacher` | `/codebase-teacher` | 1.0.0 | Reverse-engineers an existing codebase read-only into an evidence-labelled HTML teaching handbook, with a script-checked file-coverage ledger and build/test verification |
| `ebook-lecture-notes` | `/ebook-lecture-notes` | 1.1.0 | Turns an ebook or a folder of ebooks into layered lecturer-voice study notes, with charts and a self-test |
| `rnd` | `/rnd` | 1.0.1 | Researches any topic → decision-ready report + Claude Code handoff prompt |
| `orchestrate` | `/orchestrate` | 1.0.0 | Plans with the expensive model, fans execution out to parallel Sonnet subagents |
| `system-builder` | `/system-builder` | 1.0.0 | Phase-gated build workflow: interview → R&D → plan → execute → review |
| `trading-system-review` | `/trading-system-review` | 1.0.1 | Fresh-eyes senior-trader review of an existing trading system: fresh backtest, deflated Sharpe / PBO / Monte Carlo stats, today's-market research, gated rubric → offline HTML report with a deploy / incubate / revamp / retire verdict |
| `skill-scout` | `/skill-scout:skill-scout` | 0.1.0 | Before a substantial task, finds existing agent skills that fit it, security-reviews them, and installs only the ones you approve |
| `smart-money-concepts` | `/smart-money-concepts` | 1.0.0 | Two-book SMC knowledge base: structure, BOS/CHoCH, inducement, sweeps, order blocks, FVG, premium/discount, with testable algorithmic definitions and where the books disagree |

All eight are **skills**, so you don't strictly need the slash command. Describing the task in
plain language triggers them too — saying "teach me this codebase" fires `codebase-teacher`,
"summarize this book, I don't have time to read it" fires `ebook-lecture-notes`, "let's build a
habit tracker app" fires `system-builder`. The slash command is just the explicit way to ask.

---

## Which one do I use?

| You want to… | Use |
|---|---|
| Understand an existing codebase well enough to teach it | `/codebase-teacher` |
| Digest a book or a folder of ebooks without reading them | `/ebook-lecture-notes` |
| Learn a new area / compare options / decide whether to adopt something (trading topics included) | `/rnd` |
| Improve something that already exists (a service, a pipeline, a strategy) | `/rnd` — it has an "improve" mode |
| Do one big multi-part task faster and cheaper | `/orchestrate` |
| Build a whole new system from a vague idea | `/system-builder` |
| Find out if an existing trading system still works, is overfitted, or is outdated | `/trading-system-review` |
| Check for an installable skill before building a capability by hand | `/skill-scout:skill-scout` |
| Apply or code Smart Money Concepts rules (BOS/CHoCH, order blocks, FVG…) | `/smart-money-concepts` |

**`orchestrate` vs `system-builder`** — `orchestrate` is a *tactic* for one task. `system-builder`
is a *project workflow* covering the whole arc, and it uses orchestrate's delegate protocol
internally for its research and coding fan-out. Install both; system-builder falls back to
general-purpose subagents if orchestrate is missing, but that's the degraded path.
`codebase-teacher` and `trading-system-review` follow the same plan → delegate → synthesize pattern.

---

## User guide

### `/codebase-teacher` — turn an existing codebase into a teaching handbook

**What it does.** Studies a repository you didn't write (or wrote long ago) and produces a
handbook a senior would use to teach it to a junior: the mental model, architecture and flow
diagrams, every first-party file explained, and every claim about *why* labelled with its evidence.
Nothing in the repository changes.

**How to invoke**

```
/codebase-teacher
/codebase-teacher src/billing
/codebase-teacher --deep --exhaustive src/core/scheduler.py
```

Plain language works too — *"teach me this entire codebase"*, *"explain why it was built this
way"*, *"create onboarding notes I can teach another junior from"*.

| Argument | Effect |
|---|---|
| *(scope)* | A path or subsystem name; empty means the whole repository |
| `--deep` | Function-by-function depth for the scope |
| `--exhaustive <path>` | Adds line-by-line volume(s) for that file or directory |
| `--harder` | Runs analysts and the verifier on the session model instead of Sonnet / Opus |

**What happens**

1. **Frame** — scope, reader, languages, and only the questions whose answers change the study.
2. **Inventory** — `scripts/coverage.py init` snapshots the commit, fingerprints every file, lists
   first-party files, and groups vendored / generated / lockfile / binary / ignored files with the
   reason they get no line-level analysis.
3. **Spec** — the session model writes one shared spec (vocabulary, architecture, flows, and
   disjoint file *slices*) so parallel chapters share one mental model.
4. **Analyse** — one Sonnet analyst per slice, all in parallel, each writing a chapter.
5. **Synthesize** — the session model writes the end-to-end flows itself and reconciles the
   chapters; `coverage.py check` must report every first-party file explained.
6. **Verify** — an Opus verifier runs the build and tests in a scratch copy (never the repo),
   samples `path:N` references against the source, fixes the chapters, and writes `VERIFY.md`.
7. **Build** — `scripts/build_handbook.py` renders a self-contained `handbook.html` (light and dark),
   optionally split into volumes (`--split`) and a PDF (`--pdf`, via headless Chrome/Edge or
   weasyprint).

**Evidence rules.** Every technical claim carries a `path:N` reference against the snapshot
commit. Every claim about intent is `[Confirmed]` (a doc, comment, test, or commit message says
so), `[Inferred]` (with the evidence), or `[Unknown]` (with what was searched). Secrets are named,
never quoted, and the check scans the chapters and the built HTML for credential shapes.

**Read-only, enforced.** Anything that writes — installs, builds, tests, formatters — runs in
`<workdir>/verify/repo`, and `coverage.py check` fails if any repo file or `HEAD` changed since init.

**Requirements.** Python 3.11+ (stdlib only). Optional: Chrome, Edge, Chromium, or weasyprint for
the PDF. Fonts load from Google Fonts when online and fall back to system fonts offline. Install
`orchestrate` too — the skill follows its delegate protocol.

---

### `/ebook-lecture-notes` — turn a book into notes you'll actually read

**What it does.** Compresses a 300-page book into a short layer you'll actually read, sitting on
deeper layers you only open when you need more. The bet: *"don't keep everything in
the notes, keep everything reachable from the notes."* At that compression ratio, losses are
unavoidable; the skill's job is to make them recoverable, not to pretend they didn't happen. It's
written in the voice of a senior lecturer, not a summarizer — aiming for the sentence that lodges,
not the one that reads as furniture.

**How to invoke**

```
/ebook-lecture-notes C:\Users\me\Books\some-book.pdf
/ebook-lecture-notes C:\Users\me\Books\
```

Point it at a folder and you get one notes set per book. It confirms the list with you once —
including which books, if any, get a full sequential read — then works through every book without
stopping. Plain language works too — *"summarize this book, I don't have time to read it"* or
*"make notes from these ebooks"* both fire it.

**Supported formats**

`.pdf .epub .docx .txt .md .markdown .rst .html .htm .rtf .mobi .azw .azw3` — MOBI/AZW/AZW3 need
Calibre installed for the conversion step.

**What happens**

1. **Extract** — `scripts/extract.py` probes which extractors are installed and picks the best one
   per format, flagging suspicious extractions (garbled text, a PDF with no text layer) rather than
   silently passing garbage downstream.
2. **Find the structure** — `scripts/outline.py` runs several chapter-detection strategies,
   including reconstruction of vertically-set CJK titles, and reports a confidence audit so you
   know when to fall back to reading the table of contents page directly.
3. **Classify the book.** This sets the compression ratio, and getting it wrong is the biggest
   failure mode:

   | Type | Compresses to |
   |---|---|
   | Single-thesis | 5–10% |
   | Cumulative | 20–30% |
   | Reference | 30–40% |
   | Narrative | not compressed |

4. **Read strategically**, and report honestly what fraction it actually read — a reader who
   assumes the whole book was read will over-trust chapter ratings that are really extrapolations.
5. **Write `NOTES.md`** in six layers: a one-page map, named mental models, an evidence layer of
   tables and numbers, a chapter index with ★ ratings for the chapters that carry the book, a
   critical layer that argues against the book (who wrote this, and what do they gain if you
   believe it), and what was cut and where to find it. Closes with a 5–7 question self-test.
6. **Build `charts.html`** — every chart carries a "catch" box stating its weakness, because a
   chart makes a claim more persuasive than the evidence underneath it actually warrants.

**What you get.** Per book: a folder with `NOTES.md`, `charts.html`, and `_source/full_text.txt`.
Point it at a folder of books and you also get `_batch-log.md` — cross-book themes, where the
books contradict each other, and which books would gain most from a full sequential read.

**Requirements.** Python 3. Per-format extras are printed by `python3 scripts/extract.py --check`
— typically `pypdf`/poppler for PDF, `ebooklib` + `beautifulsoup4` for EPUB, `python-docx` for
DOCX, `striprtf` for RTF, and Calibre for MOBI/AZW.

**Worth knowing.** `charts.html` loads Chart.js and its fonts from CDNs, so it needs internet the
first time it's opened. Scanned PDFs have no text layer — pages get rasterized and read visually
instead of extracted. Tables and charts that exist only as images are rendered at 300 dpi and
cropped before their numbers go into the notes. Notes on copyrighted books are personal study
material, not something to republish.

---

### `/rnd` — research anything before building it

**What it does.** Turns a one-line topic into a decision-ready report answering *"should I pursue
this, and what exactly would I do next?"*

**How to invoke**

```
/rnd vector databases for a personal RAG project
/rnd self-hosted monitoring for a home lab
/rnd improve my CI pipeline, builds take 20 minutes
```

Typing "R&D `<topic>`" in plain language works too.

**What happens**

1. **Sharpen the target.** If your prompt is already specific, it states its interpretation and
   proceeds. If it's broad, it asks **one batch of 2–4 questions** — never a drip-feed — about your
   goal (learn broadly vs pick one vs prepare to build), context, constraints, and how deep you
   want the deliverable. Then it restates the brief so you can correct it cheaply before any work
   happens.
2. **Scope.** Breaks the brief into 4–6 sub-questions before searching.
3. **Gather.** Hits four source classes deliberately: web search for the landscape, GitHub for
   reference implementations and maturity signals, community threads (Reddit / HN / Stack Exchange)
   for the reality check, and official docs for real limits and pricing. Typically 5–10 searches
   plus full-page fetches. Cross-checks load-bearing claims across two independent sources and
   records disagreements rather than silently picking a side.
4. **Report.** Fixed 8-section structure so every run is comparable: refined brief, landscape,
   approaches & trade-offs, reference implementations, requirements, risks & gotchas,
   recommendation, next step.

**What you get.** `rnd-<topic-slug>-<YYYY-MM-DD>.md`, plus a 3–5 sentence verdict in chat so you
get the conclusion without opening the file.

Every report ends with a **ready-to-paste Claude Code handoff prompt** containing the chosen
direction, constraints, and first milestone — deliberately free of code-level prescriptions, since
Claude Code inspects your actual codebase when it plans.

**Improve mode.** *"Improve my X"* is a valid topic. It diagnoses before it researches: it wants
the current state and the **symptoms** (slow, flaky, costly, noisy, hard to maintain) first, then
researches targeted fixes for the diagnosed causes rather than producing a generic best-practices
listicle. The report reshapes into current state & diagnosis → prioritised candidates, each with a
hypothesis and a way to test it.

**Update mode.**

```
/rnd update vector databases
```

Reads the old report and runs a delta investigation — what changed since its date, what's new,
what died, whether the old verdict still holds — leading with a "What changed" section. Turns your
reports into a living library instead of a pile of snapshots.

**What it won't do.** Guarantee outcomes. Conclusions are framed as "what the evidence supports
testing first". If genuine coverage would take 20+ searches, it says so up front and offers a
usefully scoped version rather than silently under-delivering.

---

### `/orchestrate` — plan expensive, execute cheap

**What it does.** Keeps the costly reasoning on your session's strong model (Opus/Fable) and pushes
the routine execution out to parallel Sonnet subagents. You save tokens and independent work runs
concurrently.

**How to invoke**

```
/orchestrate add rate limiting across all four API services and write tests for each
```

Switch to Opus or Fable first — the whole point is that the planning step is worth the expensive
model.

**What happens**

1. **Plan (strong model).** Thinks hard *before* dispatching anything: files and systems involved,
   sequence of changes, edge cases, trade-offs. If something is genuinely ambiguous in a way only
   you can resolve, it asks now — rather than letting a subagent hit it three levels down. Then it
   splits the plan into work items and judges each one: needs ongoing architectural judgment (stays
   here), is small enough to finish in a handful of tool calls (also stays here), or is a sizeable,
   independent, well-specified track a competent engineer could do from the spec alone (delegated).
2. **Delegate (Sonnet).** Dispatches with `model: "sonnet"` set explicitly, batching everything
   independent into a single message so it runs concurrently — normally 3–4 agents at most, with
   related items sharing one agent. Each subagent gets a self-contained prompt — the task, the file
   paths and line numbers already known from the plan, and what "done" looks like. Sequences only
   real dependencies.
3. **Synthesize (strong model).** Reads each subagent's **actual diff**, not its summary — a
   summary describes intent, not necessarily what happened — resolves conflicts between agents, and
   runs the tests/build/lint itself rather than trusting self-reports.

**When it skips itself.** Trivial single-file changes, or a tight change that has to happen in one
place in one order. Spinning up subagents costs more than it saves there, and it will just do the
work directly rather than force a fake parallel split.

---

### `/system-builder` — build a whole system in five gated phases

**What it does.** Runs a new project through five ordered stages and never lets you skip one:
**Kickoff Interview → R&D → Plan → Execute → Review**.

**How to invoke**

```
/system-builder
```

Or just say *"let's build a personal finance tracker"*.

**The `docs/` folder is the project's memory.** Each phase reads what earlier phases wrote and
writes its own document, so **any phase can resume in a fresh session** without you re-explaining
anything. Run `/system-builder` again in a project that already has `docs/` and it reads the files,
tells you which phase is done and what's next, confirms, and continues — it never restarts Phase 0
unless `docs/` is missing or you ask.

**Two questions at kickoff** (asked every time, never assumed):

| Question | Options |
|---|---|
| **Gate mode** | **Manual** — hard stop after Phase 1 and Phase 2, you approve before continuing (3→4 then flow automatically). **Full auto** — an Approver subagent checks each phase against a checklist and sends it back for revision if it fails; you get a one-line status note at each gate as the next phase starts, and it keeps going until an Approver escalation, a blocker only you can resolve, or the end of Phase 4. |
| **Phase 3 execution style** | Parallel subagents (capped at ~3 concurrent so results stay reviewable) or one-by-one sequential. |

**The phases**

| Phase | Output | What it does |
|---|---|---|
| **0 — Kickoff & Interview** | `docs/00-BRIEF.md` | Interviews you in batched, numbered rounds until it has honest **≥90% understanding**: goal, users, must-have vs nice-to-have, constraints, success criteria, and — if there's a UI — its visual direction. Hard and uncomfortable questions are explicitly welcome. It restates its understanding and waits for "yes, that's it". The brief becomes the contract every later phase is checked against. |
| **1 — R&D** | `docs/01-RND.md` | Derives 4–8 research missions and dispatches them **all in parallel** as Sonnet subagents with character roles ("open-source scout", "community listener", "competitor analyst"). Typical missions: existing solutions, GitHub repos and libraries, Reddit/forums for real pain points, best-practice architectures, API/pricing/licensing constraints, failure stories. Findings are synthesized, conflicts resolved, and surprising claims spot-checked. |
| **2 — Plan** | `docs/02-PLAN.md` | Architecture, tech stack justified by **specific Phase 1 findings**, then milestones broken into **vertical slices** — each cutting through data + logic + interface to produce something runnable. Every slice gets tasks sized for one subagent, acceptance criteria, and **its own test gate**. |
| **3 — Execute** | `docs/03-EXECUTION-LOG.md` | One slice per subagent, with its acceptance criteria and test gate attached. Subagents must report **actual test output** as evidence; the commander then reads the real diff and re-runs the tests itself. Every dispatch and result is logged as it happens, which is how a fresh session resumes mid-execution. A slice that fails twice the same way stops looping — it gets taken over directly or re-scoped. |
| **4 — Review & Demo** | `docs/04-REVIEW.md` | Fresh reviewer subagents hunt bugs, security issues, dead code, and divergence from the plan. Full test suite, plus **scenario walkthrough tests** demoing the system end to end — happy path, edge cases, failure modes. Fix and re-run until green. Phase 4 always ends with you, even in full-auto mode. |

**Approver checklist (full-auto mode).** A phase document passes only if it fully serves the brief
with no blocking unanswered question, claims are sourced / decisions justified / evidence attached,
the logic has no contradictions or missing steps, and **a stranger could execute the next phase
from this document alone**. The plan is also checked for gaps, wrong slice ordering, hidden
dependencies between slices, and unstated assumptions; in manual mode, your approval is that
review. Max two revision loops per gate, then it escalates to you.

**Install `orchestrate` alongside it.** system-builder delegates its research and coding fan-out
through orchestrate's protocol. Claude Code plugins have no dependency field, so this isn't
declared in the manifest — it degrades to general-purpose subagents when orchestrate is absent, but
that's the fallback, not the intent.

---

### `/trading-system-review` — a senior trader's verdict on an existing system

**What it does.** Rates one of your trading-system repos with fresh eyes, the way a prop-desk head
would. It answers:

- Is there an edge?
- Is it real or overfitted?
- Is it still in line with today's market?
- What's outdated, and what's worth adding?
- Deploy, incubate, revamp or retire?

It ends in an offline HTML report with charts.

**How to invoke**, ideally in a clean session started from a folder with no `CLAUDE.md`:

```powershell
$env:CLAUDE_CODE_DISABLE_AUTO_MEMORY = "1"; claude --model best
```
```
/trading-system-review C:\path\to\your-trading-repo
```

**Why the clean session.** "Fresh eyes" means it must not lean on old conclusions. Skill
instructions can't unload auto-memory, so the skill checks its own context first and tells you if
it's contaminated. It also tells every subagent to skip prior research, plans, audits and stored
reports.

**What happens**

| Phase | Output in `trading-reviews/<system>-<date>/` | What it does |
|---|---|---|
| **0 — Independence gate** | — | Confirms the target, states the model, its knowledge cutoff and today's date, and runs the contamination check. |
| **1 — System map** | `system-map.md` | A subagent maps the rules, parameters, data coverage, backtest command and forward logs. |
| **2 — Senior-trader plan** | `review-plan.md` | The strongest model (`model: best`) sets the edge thesis, top risks, the backtest and parameter-grid plan, filled search queries, and which model handles each work item. |
| **3 — Execute** | `code-audit.md`, `metrics.json`, `market-research.md`, `techniques-research.md` | Run in parallel through `orchestrate`: code-integrity audit (Opus); fresh backtest + `review.py stats` (Sonnet); today's market and venue/prop-rule changes (Sonnet); new techniques, evidence vs hype (Sonnet). |
| **4 — Score** | `scorecard.json` | Verifies the claims, scores 10 dimensions (two hard gates: code integrity and overfitting control), and writes the verdict and revamp plan. |
| **5 — Report** | `report.html` | `review.py render` builds the report and opens it. |

**Numbers come from code, not the model.** The bundled `scripts/review.py` computes:

- trade stats with confidence intervals
- PSR, Deflated Sharpe and MinTRL (Bailey & López de Prado)
- PBO via CSCV when parameter variants exist
- Monte Carlo drawdown percentiles against your prop-firm limit
- year, session and regime breakdowns
- recent vs earlier performance
- live-vs-backtest decay tests
- curve-fit tripwires

The renderer recomputes the weighted score itself and flags a verdict that contradicts the rubric.

**Web research** uses the session's search tool. Bot-blocked pages are fetched with
[CloakBrowser](https://github.com/CloakHQ/CloakBrowser) (`pip install cloakbrowser`), not the
Chrome extension.

**Needs:** Python with numpy, pandas, scipy and matplotlib. Install `orchestrate` too, since
delegation goes through it. This is research, not financial advice. The target repo stays
read-only, apart from files its own backtest writes, and those are listed in `backtest-notes.md`.

---

### `/skill-scout` — check for an existing skill before a big task

**What it does.** At the start of a substantial task in a specialized domain, pulls keywords from
your request, checks the skills you already have, then searches skills.sh, GitHub, well-known
collections, and your added marketplaces. Each candidate gets a security review (network calls,
credential reads, elevated shells, hidden instructions…) before you see a shortlist of up to
five. Only the skills you pick are installed, then it carries on with your original request.

**How to invoke.** It fires on its own for tasks like *"build an integration for Shopify"*, or
explicitly with `/skill-scout:skill-scout <task>`. Say *"skip skill search"* to bypass it. It also
stays quiet when no one can answer its questions: in subagents, scheduled or non-interactive runs,
or when you've asked Claude to work without check-ins.

**Requirements.** Node.js 18+ (no npm dependencies). Optional: a logged-in `gh` CLI for GitHub code
search. Full details, including how to disable it: [`plugins/skill-scout/README.md`](plugins/skill-scout/README.md).

---

### `/smart-money-concepts` — a two-book SMC knowledge base

**What it does.** A reference skill built from two Smart Money Concepts ebooks (Frank Miller,
2024, and the anonymous *E-book Smart Money SMC*): market structure, BOS/CHoCH, inducement,
liquidity sweeps, order blocks, FVG/imbalance, POI, premium/discount, entry models, and risk
management. It ships testable algorithmic definitions for coding indicators, screeners, and
backtests, plus a book comparison of where the two authors disagree.

**How to invoke**

```
/smart-money-concepts
/smart-money-concepts order blocks
/smart-money-concepts fm-ch04
```

No argument uses the core frameworks; a topic, rule name, or chapter id (`fm-ch04`, `se-ch09`)
pulls the matching chapter. It also fires when you analyse a chart or write trading code with SMC
terms. Study material, not financial advice.

---

## ebook-lecture-notes changes from upstream

The skill arrived as a third-party `.skill` archive with no recorded author or license. These
defects were found in review — static analysis plus live runs on synthetic books — before import.

1. **English/European chapter detection found nothing.** The normalizer stripped all whitespace
   from a line, but the `Chapter N` / `Part N` / `Capítulo N` patterns required whitespace, so
   `Chapter 5` arrived as `Chapter5` and could never match. Verified live: 0 of 10 headings found
   on a synthetic book, and page-break clustering — the documented "noisy last resort" — silently
   became the default strategy. Patterns now tolerate the stripped form.

2. **On Windows, `outline.py` crashed with `UnicodeEncodeError` the moment it printed a CJK
   chapter title.** Legacy console code pages; it happened even with output redirected to a file.
   Verified: 0-byte JSON output, exit 1. Both scripts now force UTF-8 stdout/stderr.

3. **Re-running a batch re-ingested the tool's own `notes/` output**, and every re-ingested
   `full_text.txt` collided on one slug, silently overwriting each other. Verified: 3 of 4 books'
   text lost. The output directory is now excluded from collection, and same-run slug collisions
   get a numeric suffix.

4. **EPUB chapter markers (`@@CHAPTER@@`) were inserted on their own line**, so the outline
   script's pattern never saw the title. The marker now carries the heading text.

5. **`Chapter 5: The Meeting` was rejected as prose** because colons were treated as prose
   punctuation. Colons no longer disqualify a heading.

6. **A chapter heading within 3 lines of a `PART` heading was deduplicated away**, and so was any
   heading exactly 3 lines after the previous one (short chapters, dense DOCX exports). Dedupe is
   now per-level and only collapses cross-strategy duplicates of one physical heading — same-kind
   headings close together are kept, and the confidence audit already flags suspicious density.

7. **MOBI conversion wrote to a hardcoded `/tmp`**, which fails on Windows. It now uses the
   platform temp directory and cleans up after itself.

8. **Smaller:** `pdftotext`/`pdfinfo` pipes now decode as UTF-8 (Windows' ANSI code page mangled
   CJK); HTML is parsed from bytes so the declared charset (GBK/Big5) is honored; EPUB3 nav/TOC
   pages are no longer swept in as fake chapter sources; localized Word heading styles
   (Überschrift, Titre) are recognized; CJK chapter numbers ≥ 100 (一百二十三) parse; bare
   three-character vertical headings (第五章) are detected; and the docs were synced with actual
   script behavior.

### v1.1.0 — refinements from a field test on real books

The skill was then run end to end on real PDFs (a Chinese single-thesis polemic, a Chinese
narrative memoir, a short English strategy document, plus a scanned book that correctly refused
extraction). The pipeline and the note quality held up; every fix below closes a gap where the
*instructions* left the executor guessing:

1. **Output-language rule.** The skill never said which language to write notes in, so Chinese
   books silently produced English notes. Now: the book's primary language unless the user asks
   otherwise; translated editions may use either, stating the choice at the top of NOTES.md.
2. **Compression ratio vs. the six layers.** A strict 5–10% is arithmetically incompatible with
   the mandated layers on a short book. Clarified: the ratio governs the read-through layers (map
   + mental models); evidence, index, and critique are lookup material outside it. Reading time
   collapses, not necessarily file size.
3. **The Narrative case is now specified**, not just named — a new PEDAGOGY.md section defines
   "map, not summary" concretely (arc-shaped Layer 1, models still harvested, no scene-level
   paraphrase, sequential reading, usually 0–1 charts).
4. **Two undocumented extraction failure modes**, both hit in the field test: evidence that exists
   only as an image (the tell is dangling prose — "the table below shows…" with nothing following;
   render the page rather than silently under-reporting), and ToCs that survive as plain text in
   the front matter (read them there before rasterizing; supports bare-numeral headings via a
   content-matched, explicitly-inferred index).
5. **New [Since] provenance tag** for post-publication facts checked against cited external
   sources — the critical layer's age test kept producing facts that fit neither [Book], [Added],
   nor [Verify]. Template gets the matching `tag-since` class; [Verify] now strictly means
   "not yet confirmed."
6. **Chart count subordinated to the chart bar** in both CHARTS.md and SKILL.md ("aim for 4–8"
   padded thin books with decoration), plus reading-budget buckets clarified as ceilings on
   obligation, not permission to under-read short books. Template now opens with `<!doctype html>`
   so pages render in standards mode.

---

## Repo layout

```
.claude-plugin/marketplace.json     # marketplace manifest — lists all plugins
plugins/<name>/
  .claude-plugin/plugin.json        # name, description, version, author
  skills/<name>/
    SKILL.md                        # the skill itself (frontmatter: name + description)
    references/                     # templates and context, read on demand (codebase-teacher: reference/)
    scripts/                        # executable helpers (codebase-teacher, ebook-lecture-notes,
                                    #   skill-scout, trading-system-review)
    assets/                         # chart template (ebook-lecture-notes only)
  theme/tokens.css                  # handbook theme (codebase-teacher only)
docs/superpowers/                   # design spec + implementation plan for trading-system-review
```

**Adding a plugin:** create `plugins/<name>/` with the two files above, add an entry to
`.claude-plugin/marketplace.json` pointing at `./plugins/<name>`, commit, push, then
`/plugin marketplace update claude-skills`.

The `description` in `SKILL.md`'s frontmatter is what decides whether Claude reaches for the skill
unprompted, so it should name concrete trigger phrases rather than describe the skill abstractly.
Keep `plugin.json` and `marketplace.json` descriptions in sync, and bump `version` in
`plugin.json` when you change behaviour — installed copies only update when the version changes.

---

## Attribution

`system-builder` and `ebook-lecture-notes` originated as third-party `.skill` archives; neither
recorded an author or a license. `ebook-lecture-notes` was patched at import — see
[ebook-lecture-notes changes from upstream](#ebook-lecture-notes-changes-from-upstream);
`system-builder` was imported unmodified and has since been edited here. `orchestrate`, `rnd`,
`trading-system-review`, and `smart-money-concepts` are personal. `skill-scout` and
`codebase-teacher` come from Snapdec Sdn Bhd; `codebase-teacher` was adapted on import to run
standalone (bundled theme, Windows fixes).

`smart-money-concepts` is study notes on two copyrighted ebooks.

No license is asserted, because the upstream skills shipped without one. This repository is
public; confirm the original terms of the third-party skills and the source books before
redistributing them.

---

## Line endings

`.gitattributes` forces LF. Git for Windows defaults to `core.autocrlf=true`, which would rewrite
scripts to CRLF on clone; a shell script then fails with `$'\r': command not found`, which is
awkward to diagnose because the files look correct in an editor.
