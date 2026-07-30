# claude-skills

A personal [Claude Code](https://claude.com/claude-code) plugin marketplace. Skills live in git,
so adding the marketplace once on each machine or account keeps them updated from a single source
of truth.

This repository is **private**. The install commands below use the SSH remote, which is what works
for a private repo.

- **Repo:** `git@github.com:cincaoais/claude-skill-marketplace.git`
- **Marketplace name (used in install commands):** `claude-skills`

---

## Contents

- [Install](#install)
- [The five plugins at a glance](#the-five-plugins-at-a-glance)
- [Which one do I use?](#which-one-do-i-use)
- [User guide](#user-guide)
  - [`/video-analysis`](#video-analysis--turn-a-video-into-notes)
  - [`/rnd`](#rnd--research-anything-before-building-it)
  - [`/trading-rnd`](#trading-rnd--research-for-the-us-stocks-auto-trading-system)
  - [`/orchestrate`](#orchestrate--plan-expensive-execute-cheap)
  - [`/system-builder`](#system-builder--build-a-whole-system-in-five-gated-phases)
- [video-analysis setup & troubleshooting](#video-analysis-setup--troubleshooting)
- [video-analysis changes from upstream](#video-analysis-changes-from-upstream-v110)
- [Repo layout](#repo-layout)
- [Attribution](#attribution)
- [Line endings](#line-endings)

---

## Install

### 1. Add the marketplace — once per machine or account

```
/plugin marketplace add git@github.com:cincaoais/claude-skill-marketplace.git
```

This registers the marketplace under the name **`claude-skills`** (taken from
`.claude-plugin/marketplace.json`), which is the name every later command uses.

> **Why the SSH URL and not `cincaoais/claude-skill-marketplace`?** The `owner/repo` shorthand
> resolves through GitHub's public API, so it won't reach a private repo unless you have GitHub
> auth wired up. The SSH URL uses your existing SSH key. If you ever make the repo public, the
> shorthand is `cincaoais/claude-skill-marketplace` — note it is **`claude-skill`**, singular,
> even though the local folder is `claude-skills-marketplace`.

Requires an SSH key registered with GitHub. Check with:

```bash
ssh -T git@github.com
```

### 2. Install the plugins you want

```
/plugin install video-analysis@claude-skills
/plugin install rnd@claude-skills
/plugin install trading-rnd@claude-skills
/plugin install orchestrate@claude-skills
/plugin install system-builder@claude-skills
```

Or run `/plugin` with no arguments for the interactive browser.

### 3. Restart Claude Code

Skills are loaded at session start. Restart before expecting the new commands to appear.

### Updating

```
/plugin marketplace update claude-skills
```

Then reinstall or update the individual plugins if a version bumped.

### Removing

```
/plugin uninstall video-analysis@claude-skills
/plugin marketplace remove claude-skills
```

### ⚠️ Watch for duplicate copies in `~/.claude/skills/`

If you previously dropped these skills straight into `~/.claude/skills/`, those loose copies stay
active after you install the plugin versions, and you end up with two of each. Check with:

```bash
ls ~/.claude/skills
```

If you see `orchestrate`, `rnd`, `trading-rnd`, `system-builder`, or `video-analysis` in there
**and** you've installed them from this marketplace, delete the loose directories and let the
marketplace be the single source of truth.

---

## The five plugins at a glance

| Plugin | Command | Version | What it does |
|---|---|---|---|
| `video-analysis` | `/video-analysis` | 1.1.0 | Turns a video URL or local file into structured, timestamped knowledge notes |
| `rnd` | `/rnd` | 1.0.0 | Researches any topic → decision-ready report + Claude Code handoff prompt |
| `trading-rnd` | `/trading-rnd` | 1.0.0 | Same, specialised for US-stocks auto-trading, with a fit check against your system |
| `orchestrate` | `/orchestrate` | 1.0.0 | Plans with the expensive model, fans execution out to parallel Sonnet subagents |
| `system-builder` | `/system-builder` | 1.0.0 | Phase-gated build workflow: interview → R&D → plan → execute → review |

All five are **skills**, so you don't strictly need the slash command. Describing the task in plain
language triggers them too — pasting a YouTube link fires `video-analysis`, saying "let's build a
habit tracker app" fires `system-builder`. The slash command is just the explicit way to ask.

---

## Which one do I use?

| You want to… | Use |
|---|---|
| Understand what's in a video without watching it | `/video-analysis` |
| Learn a new area / compare options / decide whether to adopt something | `/rnd` |
| Research a trading strategy, indicator, broker, or data source | `/trading-rnd` |
| Improve something that already exists (a service, a pipeline, a strategy) | `/rnd` or `/trading-rnd` — both have an "improve" mode |
| Do one big multi-part task faster and cheaper | `/orchestrate` |
| Build a whole new system from a vague idea | `/system-builder` |

**`rnd` vs `trading-rnd`** — they overlap on purpose. `trading-rnd` is the specialised path: it
loads your trading system's context and grades every finding against it. `rnd` handles everything
else and steps aside for `trading-rnd` on trading topics when that one is installed.

**`orchestrate` vs `system-builder`** — `orchestrate` is a *tactic* for one task. `system-builder`
is a *project workflow* covering the whole arc, and it uses orchestrate's delegate protocol
internally for its research and coding fan-out. Install both; system-builder falls back to
general-purpose subagents if orchestrate is missing, but that's the degraded path.

---

## User guide

### `/video-analysis` — turn a video into notes

**What it does.** Claude can't watch video. This skill converts one into things Claude *can* read —
extracted frames plus a transcript — then writes timestamped notes from both.

**How to invoke**

```
/video-analysis https://www.youtube.com/watch?v=...
/video-analysis C:\Users\me\Videos\lecture.mp4
```

Or just paste the link with a question: *"what does this video actually claim about X?"*

**Supported input**

- Any site yt-dlp supports — YouTube, TikTok, Douyin 抖音, RedNote/Xiaohongshu 小红书, Bilibili
- Local files: `.mp4`, `.mov`, `.mkv`, `.webm`, `.avi`

**What happens**

1. **Fetch** — downloads the video, and its captions if the platform offers them (which skips
   transcription entirely).
2. **Probe** — reads duration/resolution/fps and picks an extraction tier:

   | Tier | Duration | Frame strategy |
   |---|---|---|
   | short | < 4 min | a frame every 2–3 s, read individually |
   | medium | 4–20 min | scene-change keyframes + 1 frame/10 s, read as 3×3 grids |
   | long | > 20 min | scene-change keyframes only + 1 frame/30 s, read as 3×3 grids |

   The tier is what controls token cost. Ask for finer detail on a specific range and it will
   re-extract just that range.
3. **Extract** — frames *and* transcript, always. On-screen text, charts, demos, and UI
   walkthroughs routinely carry information the audio never mentions.
4. **Analyse** — reads the transcript in full, views the frames, and explicitly reconciles the two:
   what was said but not shown, and shown but not said.
5. **Write** — saves a `.md` notes file named after the video and hands you the file.

**What you get.** A notes file with: summary, key takeaways, a timestamped breakdown in `[mm:ss]`,
a visual-only section, extracted knowledge, notable quotes, caveats, and a **Prompt-Ready
Distillation** — a self-contained block with no references to "the video", so you can paste it
straight into a system prompt.

**Notes are written in the video's primary language.** A Chinese video produces Chinese notes
(中文视频输出中文笔记) unless you ask otherwise.

**Useful things to ask for**

- *"Zoom in on 12:00–15:00, there's a chart there"* → re-extracts that range densely
- *"Keep the transcript"* → saved next to the notes (it asks before deleting the scratch dir anyway)
- Multiple URLs at once → one notes file each, processed sequentially, plus a comparison note if
  you ask for synthesis

**Requirements.** Needs `ffmpeg` and `yt-dlp` installed — see
[setup & troubleshooting](#video-analysis-setup--troubleshooting) below.

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

### `/trading-rnd` — research for the US-stocks auto trading system

**What it does.** Same pipeline as `/rnd`, but every finding is graded against *your* trading
system, and it ends by answering **"should I build this, and if so, how?"**

#### ⚙️ Set this up first

Fill in `plugins/trading-rnd/skills/trading-rnd/references/my-system.md`. It's a placeholder file,
and anything left unfilled gets treated as unknown and flagged as an assumption in every report.
It covers:

| Section | What goes in it |
|---|---|
| Broker & execution | Broker + API, order types, trading frequency, account constraints (PDT, cash vs margin) |
| Data | Sources, granularity, universe, and **what you don't have** (options chains, fundamentals, level-2) |
| Validation process | How you validate before going live; whether paper trading is available |
| Current features & strategies | What the system does today, what's live, short rule summaries per strategy |
| Preferences & constraints | Risk appetite, position sizing, monthly budget for data/tools, things already ruled out |

Code-level details are deliberately excluded — Claude Code discovers those from the real codebase.
This file only holds the domain facts research needs. A 5-minute edit here sharpens every future
report.

**How to invoke**

```
/trading-rnd mean reversion on US equities
/trading-rnd real-time risk monitoring dashboard
/trading-rnd improve my momentum strategy, drawdowns are too deep
```

**What happens**

1. **Load context** from `my-system.md`.
2. **Classify** the topic, because each type needs different sub-questions and a different report
   template:
   - **Strategy** — a trading approach (mean reversion, pairs trading, options wheel) → Template A
   - **Feature** — a system capability (risk dashboard, execution improvement, alerting) → Template B
   - **General tech** — self-learning not tied to the system → Template B minus trading sections
   - **Improve** — upgrading something that already exists → Template C
3. **Gather** across web, GitHub, r/algotrading, r/quant, HN, Quantitative Finance Stack Exchange,
   and official broker/vendor docs. Recency discipline applies hard here — broker offerings and
   data pricing change fast, so key sources get date-stamped.
4. **Evaluate fit** against your system on four axes: data you'd need vs data you have, execution
   model compatibility, implementation effort (concept-level sizing only), and risk.
5. **Report** using the matching template.

**What you get.** `rnd-<topic-slug>-<YYYY-MM-DD>.md` plus a chat verdict, ending in a starter plan
— first thing to build, first backtest to run, a measurable success criterion — and a Claude Code
handoff prompt.

**Improve mode specifics.** It cannot see your codebase. If the actual rules (entry/exit logic,
universe, holding period, sizing) aren't in your prompt, an uploaded file, a past report, or
`my-system.md`, it asks you to paste a short summary rather than guessing from the strategy's name.
It asks for symptoms in the same batch — backtest-vs-live gap, deep drawdowns, whipsaws, cost drag,
missed fills — then maps symptoms to candidate causes and researches those specifically. Each
improvement candidate comes with a hypothesis, an exact comparison test, and a **kill criterion**.

**Built-in skepticism.** Every strategy report must honestly answer *"why would this edge still
exist?"* Public strategies are mostly decayed alpha — if it's free on GitHub with thousands of
stars, the easy edge is assumed gone. Found strategies are treated as learning material and
building blocks, not plug-and-play systems.

**Boundaries.** Research and feasibility analysis, **not financial advice**. Framing is always
"here is what to test", never "this will be profitable". Any simulations it runs use synthetic data
to illustrate mechanics (how costs erode a win-rate profile, how sizing changes drawdown shape) —
they are explicitly not backtests, and real validation stays in your own process.

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
   here) or is well-specified execution a competent engineer could do from the spec alone
   (delegated).
2. **Delegate (Sonnet).** Dispatches with `model: "sonnet"` set explicitly, batching everything
   independent into a single message so it runs concurrently. Each subagent gets a self-contained
   prompt — the task, the file paths and line numbers already known from the plan, and what "done"
   looks like. Sequences only real dependencies.
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
| **Gate mode** | **Manual** — hard stop after Phase 1 and Phase 2, you approve before continuing (3→4 then flow automatically). **Full auto** — an Approver subagent checks each phase against a checklist and sends it back for revision if it fails; you're notified at each gate but not blocked. |
| **Phase 3 execution style** | Parallel subagents (capped at ~3 concurrent so results stay reviewable) or one-by-one sequential. |

**The phases**

| Phase | Output | What it does |
|---|---|---|
| **0 — Kickoff & Interview** | `docs/00-BRIEF.md` | Interviews you in batched, numbered rounds until it has honest **≥90% understanding**: goal, users, must-have vs nice-to-have, constraints, success criteria. Hard and uncomfortable questions are explicitly welcome. It restates its understanding and waits for "yes, that's it". The brief becomes the contract every later phase is checked against. |
| **1 — R&D** | `docs/01-RND.md` | Derives 4–8 research missions and dispatches them **all in parallel** as Sonnet subagents with character roles ("open-source scout", "community listener", "competitor analyst"). Typical missions: existing solutions, GitHub repos and libraries, Reddit/forums for real pain points, best-practice architectures, API/pricing/licensing constraints, failure stories. Findings are synthesized, conflicts resolved, and surprising claims spot-checked. |
| **2 — Plan** | `docs/02-PLAN.md` | Architecture, tech stack justified by **specific Phase 1 findings**, then milestones broken into **vertical slices** — each cutting through data + logic + interface to produce something runnable. Every slice gets tasks sized for one subagent, acceptance criteria, and **its own test gate**. A fresh-eyes reviewer subagent then attacks the plan for gaps, wrong ordering, and hidden dependencies before you see it. |
| **3 — Execute** | `docs/03-EXECUTION-LOG.md` | One slice per subagent, with its acceptance criteria and test gate attached. Subagents must report **actual test output** as evidence; the commander then reads the real diff and re-runs the tests itself. Every dispatch and result is logged as it happens, which is how a fresh session resumes mid-execution. A slice that fails twice the same way stops looping — it gets taken over directly or re-scoped. |
| **4 — Review & Demo** | `docs/04-REVIEW.md` | Fresh reviewer subagents hunt bugs, security issues, dead code, and divergence from the plan. Full test suite, plus **scenario walkthrough tests** demoing the system end to end — happy path, edge cases, failure modes. Fix and re-run until green. Phase 4 always ends with you, even in full-auto mode. |

**Approver checklist (full-auto mode).** A phase document passes only if it fully serves the brief
with no blocking unanswered question, claims are sourced / decisions justified / evidence attached,
the logic has no contradictions or missing steps, and **a stranger could execute the next phase
from this document alone**. Max two revision loops per gate, then it escalates to you.

**Install `orchestrate` alongside it.** system-builder delegates its research and coding fan-out
through orchestrate's protocol. Claude Code plugins have no dependency field, so this isn't
declared in the manifest — it degrades to general-purpose subagents when orchestrate is absent, but
that's the fallback, not the intent.

---

## video-analysis setup & troubleshooting

The scripts check for their own dependencies and print exact install commands on failure. They also
ask before installing anything on your machine.

| Tool | Required for | Install |
|---|---|---|
| `ffmpeg` / `ffprobe` | always | `winget install Gyan.FFmpeg` · `brew install ffmpeg` · `apt install ffmpeg` |
| `yt-dlp` | URLs only | `winget install yt-dlp.yt-dlp` · `pipx install yt-dlp` |
| `faster-whisper` | videos without captions | `pip install faster-whisper` — **`pip`, not `pipx`** (see [below](#video-analysis-changes-from-upstream-v110)) |

Alternatives to `faster-whisper`: `openai-whisper`, `whisper.cpp` (`whisper-cli`), or
`mlx-whisper` on Apple Silicon. Whichever is installed gets used.

Transcription is skipped entirely when the platform provides captions, so `ffmpeg` + `yt-dlp` alone
covers a lot of YouTube.

### Environment variables

| Variable | Default | Purpose |
|---|---|---|
| `WHISPER_MODEL` | `small` | Model size. `base` is 4–5× faster; `medium` when accuracy suffers. |
| `WHISPER_LANG` | auto-detect | Force a language, e.g. `zh`, when intro music causes misdetection. |
| `WHISPER_CPP_MODEL` | `~/.cache/whisper.cpp/ggml-small.bin` | ggml model path for the whisper.cpp route. |

### When a download fails

**Douyin and RedNote links often fail on the first try — this is expected, not a dead end.**
`references/sources.md` holds the per-platform fallback ladder: cookies, share-link expansion, and
finally manual download → hand it the local file instead. The skill reads that file before telling
you something can't be done, and reports the specific failing step and exact error rather than
silently degrading to guessing content from the title.

### Running the scripts by hand

```bash
bash scripts/fetch_video.sh "<url-or-local-path>" <workdir>
bash scripts/probe.sh <video-file>
bash scripts/extract_frames.sh <video-file> <workdir>/frames <short|medium|long>
bash scripts/extract_frames.sh <video-file> <outdir> zoom <start-s> <end-s>
bash scripts/get_transcript.sh <video-file> <workdir>
```

Frames are timestamp-named (`t0042.5.jpg` = 42.5 s). Medium/long tiers also produce montage grids
(`grid_001.jpg`) plus a `grid_index.txt` mapping each cell back to its timestamp.

---

## video-analysis changes from upstream (v1.1.0)

Three bugs, each reproduced and verified against a synthetic 300s clip with hard cuts and a real
50-minute Douyin video.

1. **Scene detection failed on Windows.** `extract_frames.sh` passed a path to
   `metadata=print:file=` *inside* the ffmpeg filtergraph, where `:` is an option separator and
   MSYS/Git-Bash does not rewrite `/c/Users/...` to `C:/Users/...`. Result: zero keyframes and
   `Error initializing filters`. Now uses `showinfo`, which reports `pts_time` on stderr and
   needs no path.

2. **Montage grids were scrambled on every platform.** `make_grids` sorted with
   `sort -t t -k2 -g`, which splits the *entire path* on the letter `t`. Any `t` in a parent
   directory (`/tmp/...`, `.../scratchpad/...`) shifted the sort key and silently degraded the
   order to lexicographic: `0, 10, 100, 110, ..., 190, 20, 200, ...`. The grid index still looked
   plausible, so the corruption was easy to miss. Now sorts numerically on the basename.

3. **`faster-whisper` was never detected.** The PyPI package ships **no console script**
   (verified on 1.2.1 — its `entry_points` list is empty), so `command -v faster-whisper` never
   matched and the script reported "no transcription tool found" while a working library sat
   installed. This is also why the old hint `pipx install faster-whisper` was wrong: pipx installs
   console scripts and this package has none. A new branch drives the library through Python,
   with `WHISPER_MODEL` / `WHISPER_LANG` overrides.

Also fixed: scene keyframes rounding to 0.1s could collide on rapid cuts and silently overwrite
each other (310 frames in, 286 out). Collisions now get a numeric suffix.

---

## Repo layout

```
.claude-plugin/marketplace.json     # marketplace manifest — lists all plugins
plugins/<name>/
  .claude-plugin/plugin.json        # name, description, version, author
  skills/<name>/
    SKILL.md                        # the skill itself (frontmatter: name + description)
    references/                     # templates and context files, read on demand
    scripts/                        # executable helpers (video-analysis only)
```

**Adding a plugin:** create `plugins/<name>/` with the two files above, add an entry to
`.claude-plugin/marketplace.json` pointing at `./plugins/<name>`, commit, push, then
`/plugin marketplace update claude-skills`.

The `description` in `SKILL.md`'s frontmatter is what decides whether Claude reaches for the skill
unprompted, so it should name concrete trigger phrases rather than describe the skill abstractly.
Keep `plugin.json` and `marketplace.json` descriptions in sync, and bump `version` in
`plugin.json` when you change behaviour.

---

## Attribution

`video-analysis` and `system-builder` originated as third-party `.skill` archives; neither
recorded an author or a license. The `video-analysis` fixes above are the only modifications to
that skill; `system-builder` is unmodified. `orchestrate`, `rnd`, and `trading-rnd` are personal.

No license is asserted, because the upstream skills shipped without one. Confirm the original
terms before making this repository public or redistributing it.

---

## Line endings

`.gitattributes` forces LF. Git for Windows defaults to `core.autocrlf=true`, which would rewrite
the shell scripts to CRLF on clone; bash then fails with `$'\r': command not found`, which is
awkward to diagnose because the files look correct in an editor.
