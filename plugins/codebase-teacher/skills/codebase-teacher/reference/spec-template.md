# Analysis spec — {REPO_NAME}

The primary model writes this file to `<workdir>/spec.md` before any
analyst runs, and every analyst reads it first. It is what makes
parallel chapters share one mental model, one vocabulary, and one
evidence format. Fill every section; delete none.

---

## 1. Snapshot and rules

| | |
|---|---|
| Repository | `{REPO_PATH}` — **read-only** |
| Commit / branch | `{COMMIT}` on `{BRANCH}` · working tree {clean / N uncommitted paths: list} |
| Scope | {whole repository / `path/`} |
| Depth | {default / --deep / --exhaustive `path`} |
| Reader | {capable junior new to this system and framework / as stated by the user} |
| Workdir | `{WORKDIR}` — the only place anything is written |
| Scratch copy for commands | `{WORKDIR}/verify/repo` |

All references are repo-relative paths with line numbers against the
commit above. Writing conventions and entry shapes:
`{SKILL_DIR}/reference/handbook-template.md` — follow it literally.

## 2. Toolchain

| | Command | Writes files? |
|---|---|---|
| Install | | |
| Build | | |
| Test | | |
| Type check / lint | | |
| Start (safe, local) | | |

Any command that may write runs only in the scratch copy.

## 3. The system in one paragraph

{What it is, who uses it, what the 5–7 components are. Analysts frame
their chapters inside this; they do not redefine it.}

## 4. Vocabulary

| Term | Meaning in this system | Code name(s) | First defined in |
|---|---|---|---|
| | | | |

Analysts use these words exactly. A new term an analyst needs goes in
its output's "Proposed vocabulary" list, not silently into prose.

## 5. Architecture

```diagram Components and boundaries
{the diagram chapter 5 will carry}
```

| Component | Responsibility | Main paths | Talks to |
|---|---|---|---|

## 6. Flows (owned by the primary model)

| Flow | Trigger | Entry point | Components crossed |
|---|---|---|---|

Analysts document their subsystem's part of these flows inside their
chapter and add a "Flow hand-offs" list (what enters, what leaves, at
which `path:N`); the primary model writes the end-to-end traces.

## 7. Slices

Disjoint sets of files, one analyst each. Every first-party file in
`inventory.json` belongs to exactly one slice (or to the primary
model's chapters).

| Slice | Chapter file(s) | Owns paths | Introduces terms | May assume |
|---|---|---|---|---|
| A | `chapters/20-billing.md` | `src/billing/**` | invoice, ledger entry | vocabulary §4 |

## 8. Known evidence sources

{ADRs, docs/, READMEs, design comments, notable commit ranges, issue
links found during framing — so analysts look there first.}

## 9. Open questions so far

{Anything the framing could not settle; analysts may answer these with
evidence, and must label what they cannot.}
