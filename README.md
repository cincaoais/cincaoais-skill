# claude-skills

A personal [Claude Code](https://claude.com/claude-code) plugin marketplace. Skills live in git,
so adding the marketplace once on each machine or account keeps them updated from a single source
of truth.

- **Repo:** [`cincaoais/cincaoais-skill`](https://github.com/cincaoais/cincaoais-skill) (public)
- **Marketplace name (used in install commands):** `claude-skills`

---

## Contents

- [Install](#install)
- [The five plugins at a glance](#the-five-plugins-at-a-glance)
- [Which one do I use?](#which-one-do-i-use)
- [User guide](#user-guide)
  - [`/rnd`](#rnd--research-anything-before-building-it)
  - [`/orchestrate`](#orchestrate--plan-expensive-execute-cheap)
  - [`/orca-coordinator`](#orca-coordinator--claude-plans-orca-workers-do-the-work)
  - [`/trading-system-review`](#trading-system-review--a-senior-traders-verdict-on-an-existing-system)
  - [`/skill-scout`](#skill-scout--check-for-an-existing-skill-before-a-big-task)
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
/plugin install rnd@claude-skills
/plugin install orchestrate@claude-skills
/plugin install orca-coordinator@claude-skills
/plugin install trading-system-review@claude-skills
/plugin install skill-scout@claude-skills
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

**Plugins dropped from this marketplace** (`find-skills`, `video-analysis`, `web-pentest`) stay
installed on machines that already have them until you uninstall them:
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

## The five plugins at a glance

| Plugin | Command | Version | What it does |
|---|---|---|---|
| `rnd` | `/rnd` | 2.0.0 | Reuse-first research across web, GitHub, Reddit / X and Chinese platforms → decision-ready report + Claude Code handoff prompt |
| `orchestrate` | `/orchestrate` | 1.0.1 | Plans with the expensive model, fans execution out to parallel Sonnet subagents |
| `orca-coordinator` | `/orca-coordinator` | 1.0.0 | Claude Code coordinates; Orca dispatched workers (Antigravity first, pi fallback) do the work, sized as micro-tasks |
| `trading-system-review` | `/trading-system-review` | 1.1.0 | Fresh-eyes senior-trader review of an existing trading system, or vetting of someone else's repo: fresh backtest, deflated Sharpe / PBO / Monte Carlo stats, today's-market research, gated rubric → offline HTML report with a deploy / incubate / revamp / retire verdict |
| `skill-scout` | `/skill-scout:skill-scout` | 0.1.1 | Before a substantial task, finds existing agent skills that fit it, security-reviews them, and installs only the ones you approve |

All five are **skills**, so you don't strictly need the slash command. Describing the task in
plain language triggers them too. The slash command is just the explicit way to ask.

---

## Which one do I use?

| You want to… | Use |
|---|---|
| Learn a new area / compare options / find repos and frameworks to reuse (trading topics included) | `/rnd` |
| Improve something that already exists (a service, a pipeline, a strategy) | `/rnd` — it has an "improve" mode |
| Do one big multi-part task faster and cheaper | `/orchestrate` |
| Keep Claude's quota for thinking and hand the work to Orca workers (Antigravity, pi) | `/orca-coordinator` |
| Find out if an existing trading system still works, is overfitted, or is outdated | `/trading-system-review` |
| Vet someone else's GitHub trading repo or framework before learning from or building on it | `/trading-system-review` — reference mode |
| Check for an installable skill before building a capability by hand | `/skill-scout:skill-scout` |

---

## User guide

### `/rnd` — research anything before building it

**What it does.** Starts from reuse: it finds the frameworks, reference repos, tools, papers and
practitioner experience that already answer the question, then turns a one-line topic into a
decision-ready report answering *"what should I learn from or build on, and what do I do next?"*

**How to invoke**

```
/rnd vector databases for a personal RAG project
/rnd self-hosted monitoring for a home lab
/rnd improve my CI pipeline, builds take 20 minutes
```

Typing "R&D `<topic>`" in plain language works too.

**How it searches**

1. **Frame the question.** If the prompt is already specific, it states its interpretation and
   starts. If it's broad, it asks **one batch** of questions — never a drip-feed — and only when the
   answers would change where it searches or what it recommends.
2. **Build a keyword map.** Before the first search, it writes down the vocabulary the field
   actually uses, from several angles at once: your own words, how people with the problem describe
   it, expert jargon and acronyms, named tools / repos / papers / people, comparisons and
   alternatives, failures and critiques, GitHub vocabulary, Chinese-language terms, and adjacent
   fields. It also imagines a beginner, a maintainer, a skeptic and a domain expert, each searching
   differently, then snowballs new terms from every good source.
3. **Search widely, then read deeply.** Web search covers the landscape. GitHub (`gh search
   repos|code|issues`, topic pages, awesome-lists) supplies reference implementations and maturity
   signals — stars, last push, releases, issues, licence, tests. Community threads on Reddit,
   Hacker News, Stack Overflow and X provide the reality check. Chinese platforms — Douyin,
   Bilibili, Zhihu, Xiaohongshu, CSDN and Juejin — cover fields active there. Official docs and
   papers confirm capabilities, limits and pricing. It sweeps cheaply first, then reads the
   load-bearing pages, READMEs, source and issues in full; dates its sources, weights recent
   material, and cross-checks load-bearing claims in two independent sources.
4. **Write a reuse-first report.** The heart of it is a reference-repo table: what to take from
   each project, stars, last push, licence and maturity. Around it sit the bottom line and
   confidence, options and honest trade-offs, dated evidence with tiers, disagreements, what would
   change the verdict, coverage gaps, and the next step.

**What you get.** `rnd-<topic-slug>-<YYYY-MM-DD>.md`, plus a 3–5 sentence summary in chat so you
get the conclusion without opening the file. Every report ends with a **ready-to-paste Claude Code
handoff prompt** containing the chosen direction, constraints, and first milestone — deliberately
free of code-level prescriptions, since Claude Code inspects your actual codebase when it plans.

**CloakBrowser and bot walls.** Some of the best practitioner discussion sits behind bot walls.
The skill escalates in order: normal fetch, the bundled `scripts/stealth_fetch.py`
([CloakBrowser](https://github.com/CloakHQ/CloakBrowser)), a logged-in persistent profile, then
skip and record the gap. It runs the readiness check only when the plan needs a walled source,
and the login flow only when a site asks for one:

```
uv run "<skill-dir>/scripts/stealth_fetch.py" --check
uv run "<skill-dir>/scripts/stealth_fetch.py" --login <url>
```

If CloakBrowser is not ready, it asks once whether to install it now (about 200 MB of Chromium) or
skip Reddit, X and Douyin for this run. Install with `pip install cloakbrowser` followed by
`python -m cloakbrowser install`, or let `uv run` install the script's declared dependencies. The
one-time `--login <url>` opens a visible browser on the persistent profile so you sign in yourself,
and later fetches reuse that profile. Browsing is read-only.

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

**What it won't do.** Guarantee outcomes. Conclusions are framed as "what the evidence
supports testing first".

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

### `/orca-coordinator` — Claude plans, Orca workers do the work

**What it does.** Turns Claude Code into the coordinator of an Orca
orchestration run and applies standing rules you would otherwise repeat in every prompt. Claude
spends its tokens on ideas, R&D directions, specs and review; Orca dispatched workers do the
reading, coding, testing, cloning and web research. Built for a quota-limited Claude plan.

**How to invoke**

```
/orca-coordinator R&D order-flow strategies for gold; my notes are in ./orderflow
/orca-coordinator fix the findings in report.md by priority
```

**What it applies**

- **Roles.** Claude makes small targeted reads only; bigger reading goes to a scout worker
  whose report Claude reads. Your own research is treated as input to check, not as truth.
- **Worker choice.** Antigravity first, then another Antigravity model on a quota error, then pi.
  Your latest word on quota in the conversation wins.
- **Micro-tasks for pi.** About 100 KB of reading per pi worker, one output file written one
  section per tool call, map-reduce for big syntheses, many small workers in waves.
- **Spec recipe.** Target, change, constraints, ownership (disjoint files), acceptance, and a
  fixed worker-rules line.
- **Plan gate.** A short task table, then dispatch, unless you ask to review first or the work
  touches risk/execution code, live accounts, secrets or anything outward-facing.
- **Verification.** Runs each acceptance check itself, re-dispatches anything suspicious, uses
  an independent second worker for critical numbers, tests both options when torn.
- **Timed starts.** "Start at midnight" becomes a one-time scheduled job, in Malaysia time
  (UTC+8) unless you say otherwise.
- **Close-out.** Releases workers, closes leftover tabs and worktrees, and reports outcome,
  evidence, open items and anything done that you did not ask for.

`references/pi-recovery.md` holds fixes for known pi failures: an unsent prompt, stalls by context
%, provider 400 errors, `consumer_fenced` after a new session, and jobs killed on release.

**Needs:** Orca with its `orchestration` skill (this skill loads Orca's version-matched guide for
the actual commands), plus the worker CLIs you use (Antigravity `agy`, pi).

---

### `/trading-system-review` — a senior trader's verdict on an existing system

**What it does.** Rates a trading repo with fresh eyes, the way a prop-desk head would — either
your own system or someone else's repo you are thinking of adopting. It answers:

- Is there an edge?
- Is it real or overfitted?
- Is it still in line with today's market?
- What's outdated, and what's worth adding?
- Deploy, incubate, revamp or retire?

It ends in an offline HTML report with charts.

**Two modes.** *Own* mode (the default) reviews a system you already run or built. *Reference*
mode vets a third-party repo or framework before you learn from or build on it: it clones the repo,
records the commit SHA, checks the licence and maintenance, treats every README performance claim
as a claim to reproduce, and adds an adoption verdict — **ADOPT-AS-BASE**, **LEARN-FROM** or
**AVOID** — to the report. Reference reviews land in
`trading-reviews/ref-<owner>-<repo>-<date>/`. It also works on local paths; a GitHub or GitLab URL
selects reference mode, and unclear wording gets one question.

**How to invoke**, ideally in a clean session started from a folder with no `CLAUDE.md`:

```powershell
$env:CLAUDE_CODE_DISABLE_AUTO_MEMORY = "1"; claude --model best
```
```
/trading-system-review C:\path\to\your-trading-repo
/trading-system-review https://github.com/owner/trading-repo
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

In reference mode the same phases run, with the clone under `OUT/src`, the README's claims added
to the plan, and an `adoption` block in `scorecard.json`. The ten-dimension score and the existing
verdict still judge the strategy as-is; the adoption verdict says what to do with the codebase.

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

**Web research** uses the session's search tool. Bot-blocked pages are fetched with the same
bundled `scripts/stealth_fetch.py` ([CloakBrowser](https://github.com/CloakHQ/CloakBrowser)), not
the Chrome extension. If CloakBrowser is not ready, the skill asks once whether to install it or
skip those sources; `--login <url>` handles sign-in walls once on a persistent profile. Skipped
sources are listed under the review's limitations.

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

## Repo layout

```
.claude-plugin/marketplace.json     # marketplace manifest — lists all plugins
plugins/
  orchestrate/
    .claude-plugin/plugin.json      # name, description, version, author
    skills/orchestrate/SKILL.md     # the skill itself (frontmatter: name + description)
  orca-coordinator/
    .claude-plugin/plugin.json
    skills/orca-coordinator/
      SKILL.md
      references/                   # pi-recovery
  rnd/
    .claude-plugin/plugin.json
    skills/rnd/
      SKILL.md
      references/                   # search-angles, source-access, report-guide
      scripts/                      # stealth_fetch.py, plus its tests
  trading-system-review/
    .claude-plugin/plugin.json
    skills/trading-system-review/
      SKILL.md
      references/                   # rubric, search-playbook
      scripts/                      # review.py, stealth_fetch.py, plus their tests
  skill-scout/
    .claude-plugin/plugin.json
    skills/skill-scout/
      SKILL.md
      references/                   # security, sources, vetting
      scripts/                      # scout.js and lib/
    README.md                       # plugin-specific README (skill-scout)
docs/superpowers/
  specs/                            # design specs, incl. 2026-11-01 rnd revamp + TSR reference mode
  plans/                            # implementation plans
  notes/                            # probe notes, incl. the 2026-11-01 CloakBrowser probe
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

`orchestrate`, `orca-coordinator`, `rnd`, and `trading-system-review` are personal. `skill-scout` comes from
Snapdec Sdn Bhd.

`skill-scout` is MIT, as declared in its `plugin.json`. The personal skills have no separate
license file. This repository is public; confirm the terms of any third-party skill before
redistributing it.

---

## Line endings

`.gitattributes` forces LF. Git for Windows defaults to `core.autocrlf=true`, which would rewrite
scripts to CRLF on clone; a shell script then fails with `$'\r': command not found`, which is
awkward to diagnose because the files look correct in an editor.
