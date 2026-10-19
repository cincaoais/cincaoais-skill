# Handbook template

The authoritative shape of the handbook: volumes, chapters, the entry
shapes inside them, and the Markdown every author writes. The primary
model copies the relevant parts into the analysis spec; analysts follow
it literally so that independently drafted chapters assemble into one
document.

---

## Workdir layout

Everything lives in the session scratch directory, never in the repo:

```
<scratch>/codebase-teacher/<repo-name>/
  snapshot.json inventory.json fingerprint.json   # coverage.py init
  spec.md                                          # the shared analysis spec
  chapters/NN-<slug>.md                            # one file per chapter, NN = reading order
  chapters/90-coverage.md                          # coverage.py check --index (generated)
  handbook.json                                    # build manifest
  out/handbook.html [index.html vol-N.html handbook.pdf]
  verify/repo/                                     # scratch copy for build/test runs
  VERIFY.md                                        # verifier report
  check.json                                       # coverage.py check result
```

## Volume plan

One volume when the scope is under roughly 150 first-party files and
20k lines; otherwise these five, in this order (the master index explains
the order — overview before flows, flows before files):

| Volume | Chapters | Reader goal |
|---|---|---|
| 1 · System overview and architecture | front matter, system in five minutes, vocabulary, architecture map, dependency map, runtime topology, setup and startup | explain what the system is and how it is shaped |
| 2 · Runtime and data flows | end-to-end flows, data model and persistence, authN/authZ, external integrations, background work and events, configuration and environment | trace any request, job, or event |
| 3 · Subsystems and files | one chapter per subsystem with its file and symbol entries, imports and dependencies | find and understand any file |
| 4 · Operations, testing, debugging | testing strategy, build and deployment, failure modes, debugging guide | run, test, debug, and change it safely |
| 5 · Decisions, coverage, verification | confirmed / inferred / unknown decisions, open questions, file-coverage index, verification evidence, teach-another-junior summary, comprehension questions | defend the explanations and teach them on |

A single-volume handbook keeps the same chapter order.

## Required chapters

Every handbook contains each of these as a `#` chapter (merge two only
when the system genuinely has nothing to say for one; say so in a line):

| # | Chapter | Written by | Must contain |
|---|---|---|---|
| 1 | Repository snapshot and scope | primary | commit, branch, working-tree state, scope, depth mode, what was excluded and why |
| 2 | How to use this handbook | primary | reading order, evidence labels, reference notation, how collapsible entries work |
| 3 | The system in five minutes | primary | the problem, the users, the 5–7 components, one diagram, one representative flow in prose |
| 4 | Product and domain vocabulary | primary | every domain and framework term the handbook relies on, defined once, linked from first use |
| 5 | Architecture map | primary | component diagram, responsibilities, boundaries |
| 6 | Dependency map | primary + analysts | internal module dependencies (diagram) and external packages grouped by the capability they provide |
| 7 | Runtime topology | primary | processes, containers, queues, databases, schedulers, and what talks to what |
| 8 | Setup and startup sequence | primary | from the start command to "ready", including config loading, DI/wiring, migrations, and shutdown |
| 9 | End-to-end execution flows | primary (reconciles) | the flow traces (shape below), success and failure |
| 10 | Data model and persistence | analyst | entities, relationships diagram, lifecycles, transactions, migrations |
| 11 | Authentication and authorization | analyst | identity source, session/token lifetime, where permission checks live, what is unprotected |
| 12 | External integrations | analyst | each service: purpose, client code, auth, timeouts, retries, failure handling, what is unverified |
| 13 | Background work and event processing | analyst | producers, consumers, schedules, retries, idempotency, ordering |
| 14 | Configuration and environment | analyst | each setting: source, default, who reads it, effect; values never quoted when secret |
| 15+ | One chapter per subsystem | analysts | subsystem shape below |
| — | Imports and dependency explanations | analysts | per subsystem inside its chapter; cross-cutting packages in the dependency map |
| — | Testing strategy and how to read the tests | analyst | test layout, fixtures/factories, what is and is not tested, how to run one test |
| — | Build and deployment | analyst | build steps, artefacts, environments, CI, release |
| — | Failure modes | primary | what breaks, symptoms, where it is handled, what is not handled |
| — | Debugging guide | primary | entry points, logs, breakpoints, toggles, "if you see X, look at Y" table |
| — | Architectural decisions | primary | three sections: Confirmed, Inferred, Unknown (shape below) |
| — | Open questions and unresolved dependencies | primary | everything the study could not establish, and who could answer it |
| — | Complete file-coverage index | `coverage.py --index` | generated; never hand-written |
| — | Verification evidence | primary from VERIFY.md | commands run, verbatim results, claims corrected |
| — | Teach this to another junior | primary | one page: the story you would tell at a whiteboard, in order |
| — | Comprehension and teach-back questions | primary | 10–20 questions, each with the chapter that answers it |

---

## Writing conventions (every author)

- **Markdown subset**: exactly what `scripts/build_handbook.py`
  documents in its docstring. Anything else renders as literal text.
- **Headings**: `#` chapter, `##` section, `###` file entry, `####`
  symbol or sub-point. Chapters and sections appear in the TOC.
- **File entries** start with the backticked repo-relative path:
  `` ### `src/billing/invoice.py` — invoice lifecycle ``. That heading is
  what the coverage check counts and what the coverage index links to.
  Long entries for minor files go in `:::details` with the same summary
  shape.
- **Grouped coverage**: a set of repetitive files explained together
  (migrations, icon components, generated clients) carries a marker in
  the section that explains them: `<!-- covers: src/icons/*.tsx -->`.
  Use it only when the section really explains the set as a set.
- **References**: `` `path:42` `` or `` `path:42-58` ``, repo-relative,
  against the snapshot commit. Every technical claim has one.
- **Excerpts**: quote real code with ```` ```python src/app.py:40-55 ````
  — the body must equal those lines exactly (the check compares them).
  Elide by quoting two excerpts, never by editing one.
- **Evidence labels** on every claim about *why*: `[Confirmed]`,
  `[Inferred]`, `[Unknown]` (rules below). Claims about *what the code
  does* need a reference, not a label.
- **Diagrams**: ```` ```diagram Caption ```` with box-drawing or ASCII,
  ≤ 88 columns so they never scroll. One diagram per idea; name boxes
  with the vocabulary chapter's terms.
- **Cross-references**: `[Request lifecycle](#request-lifecycle)` —
  the anchor is the heading text lowercased with other characters
  collapsed to `-`; file entries are `#f-` + the path slugged the same
  way (`#f-src-billing-invoice-py`). Never write "see Part B" or
  "another agent covers".
- **Secrets**: never quote a credential, token, key, or secret config
  value. Name the setting and where it is read; write `<redacted>` or an
  obviously fake value (`sk_test_xxx`) when shape matters.
- **Register**: a patient senior engineer. Mental model before detail;
  define a term before using it; explain framework conventions and hidden
  runtime behaviour (decorators, DI, middleware order, ORM lazy loading,
  reflection, codegen) where they first matter; explain common syntax
  once, never again; no "simply", "just", "obviously".
- **Length**: match each chapter and entry to what the system needs:
  cover the substance, but do not pad with filler sections, redundant
  summaries, or boilerplate. The subsystem Summary and "You should now
  be able to explain" blocks stay, kept tight. A required chapter with
  little to say gets a short paragraph.

## Evidence rules

| Label | Use when | Required with it |
|---|---|---|
| `[Confirmed]` | a document, comment, test, issue, config, or commit message states it | the reference: `` `docs/adr/0003-queue.md:12` ``, or commit `a1b2c3d` and its subject |
| `[Inferred]` | the code and its surroundings strongly suggest it | the evidence that suggests it, in the same sentence |
| `[Unknown]` | nothing reliable explains it | what was searched, and the plausible readings if any, marked as such |

Shapes:

> [Confirmed] Invoices are immutable once issued — the docstring at
> `src/billing/invoice.py:14` says so, and `tests/test_invoice.py:88`
> asserts that `issue()` twice raises.

> [Inferred] The retry wrapper exists because the payment gateway
> times out under load: every call site at `src/pay/client.py:30-44`
> wraps it, and the timeout is 2s while other clients use 30s. No
> document says so.

> [Unknown] Why `orders` and `order_lines` live in separate databases.
> Searched: docs/, ADRs, commit messages touching `db_router.py`, blame
> of `settings/base.py:120`. Plausible readings: an old scaling
> decision, or a migration in progress.

Never write a historical narrative ("the team decided…") without a
`[Confirmed]` source. Git blame and log show *when* and *who changed*;
they show *why* only when the message says so.

---

## Subsystem chapter

```
# <Subsystem name>

<Two-paragraph mental model: what it is for, where it sits in the
architecture diagram, what the reader should picture.>

```diagram <Subsystem> inside the system
...
```

## Responsibilities and boundaries
## How it works            <main execution flow, referenced>
## Files                   <file entries, most important first>
## Tests                   <what they prove, how to read them>
## Common mistakes and debugging

## Summary
- **Owns:** …
- **Deliberately does not own:** …   (and who does)
- **Inputs → outputs:** …
- **Depends on / depended on by:** …
- **Main flow:** one sentence, with references
- **Most important files:** 3–5 links
- **Main failure modes:** …

> **You should now be able to explain:** 3–5 concrete things, phrased
> as statements the reader could say to a colleague.
```

## File entry

Default depth (every first-party file gets at least the first three lines):

```
### `path/to/file.ext` — <one-line role>

**Responsibility.** What it owns and why it exists [label if the why is a claim].
**Used by.** Who imports or calls it (`caller.py:12`). **Uses.** What it needs and why.

**Imports that matter.**
| Import | Capability it provides here |
|---|---|
| `from sqlalchemy.orm import Session` | the unit-of-work: every query in this file runs in the caller's transaction, so nothing here commits |

**Module-level state.** For each constant/variable that matters:
what it holds, where its value comes from, its lifetime (import-time /
per-request / per-process), who reads it, whether it can change, why the
flow needs it.

**Public surface.** Each function/class/type: contract in one or two
sentences, with `path:N`.

**Control and data flow.** What happens before and after the important
operations; framework behaviour the reader cannot see.

**Configuration, errors, concurrency.** Only what applies.

**Tests.** `tests/...:N` and what they pin down.

**Watch out.** Common mistakes; where to put a breakpoint.
```

Bad import note: "imports `Session` from SQLAlchemy". Bad variable
note: "`MAX_RETRIES` is the maximum number of retries". Good notes say
what the dependency *guarantees* and what the value *does to the flow*.

Trivial files (re-export barrels, empty `__init__.py`, one-line
config) get one sentence in a `:::details` entry or a `covers` group.

`--deep` adds, per function: purpose, parameters (meaning, not type
repetition), return value, important locals, each branch and why it
exists, error paths, async/concurrency/reflection behaviour.

## `--exhaustive <path>` entry

Quote the file in excerpts of ≤ 40 lines, in order, each followed by a
line-by-line list:

```
```python src/billing/invoice.py:1-12
...exact lines...
```

- **L1–3** — imports: `Decimal` because money never touches floats here; …
- **L5** — `TAX_RATE` is read once at import from settings; changing the
  env var needs a restart.
- **L8–12** — `class Invoice`: …connects to the flow in [Issuing an invoice](#issuing-an-invoice).
```

Every import, declaration, meaningful variable, branch, and call is
explained and tied back to the wider system. Files over ~400 lines, or
selections over ~1,500, split into ordered chapters (`Invoice lifecycle,
part 1 of 3`). Literal line-by-line for a whole large repository only
when the user asked for exactly that, as extra volumes.

## Flow trace

```
## <Flow name> (e.g. "Customer pays an invoice")

**Starts when:** … **Entry point:** `path:N`

```diagram <Flow name>
Browser ──POST /pay──▶ router ──▶ PaymentService.pay ──▶ Gateway
   ◀── 302 ──────────── view ◀──── Payment row ◀──────────┘
```

1. **<Step>** — what happens, `path:N`. Validation/authorization here.
   Data shape in → out. Database access. External call. Side effects.
2. …

**Succeeds with:** … **Fails when:** each failure, where it is caught
(`path:N`), what the user sees, retry/recovery. **Tests:** `path:N`.
```

Pick flows that together exercise every major component: at least one
read, one write, one background/event flow if any exist, one auth
failure, and one external-integration failure.

## Decisions chapter

Three sections, `## Confirmed decisions`, `## Inferred decisions`,
`## Unknown or unresolved`, each a list of entries in the evidence
shapes above, each linking back to the chapter where the decision bites.

## Teach-back

- **Teach this to another junior**: the whiteboard story in 10–15
  numbered steps, each pointing to the chapter that backs it.
- **Comprehension questions**: 10–20, mixing "what happens when…",
  "where would you change…", "why does…" ; each ends with
  `→ [Chapter](#anchor)`. No answers inline; the chapter is the answer.
