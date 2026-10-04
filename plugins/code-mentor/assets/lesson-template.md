<!--
Template for LESSON.md. Replace every <placeholder> and delete this comment.
Sections move from what (1–2) to how (3–7) to why (8–9) to "now you" (10).
Drop a section only when it has nothing to say for this scope, e.g. §6 when the app stores no data.
-->

# <Project name>: how it works

> Learning session · <YYYY-MM-DD> · Scope: <whole project | feature | folder> · Level: <background>

## 1. The big picture

<One paragraph in plain English: what the system does, for whom, and the main thing a user does with it.>

**In one breath:**

- <Part 1, e.g. "A Next.js website that renders the pages and handles clicks">
- <Part 2>
- <Part 3>

## 2. Tech stack at a glance

| Layer | Technology | Its job in this project | Lives in |
|---|---|---|---|
| <UI> | <React via Next.js> | <renders pages, handles clicks> | `<app/>` |
| <...> | <...> | <...> | `<...>` |

## 3. Architecture

```mermaid
flowchart LR
  %% boxes are real folders or files; arrows say what flows between them
```

**How to read this:** <1–3 sentences: what the arrows and shapes mean.>

<One or two sentences per box: what it does and where it lives.>

## 4. Folder map

```text
<project>/
├── <folder>/        ← <responsibility>
│   └── <file>       ← <why it matters>
└── <file>           ← <responsibility>
```

**Why it's organized this way:** <Name the placement reasons that apply: framework convention, separation of concerns, server/client boundary, and so on.>

## 5. Follow one request: <golden path, e.g. "a user places an order">

```mermaid
sequenceDiagram
  autonumber
```

1. **<Step>**: `<path:line>`. <What happens, and why it happens here.>
2. **<Step>**: `<path:line>`. <...>

<A snippet of the most important hop, with ① ② markers explained below it.>

## 6. The data

```mermaid
erDiagram
```

<One sentence per entity. Relationships in plain words ("one user has many orders"). Where the schema is defined and how it changes, e.g. migrations.>

## 7. Key concepts in this codebase

### 7.1 <Concept>

- **What:** <one sentence>
- **Where:** `<path:line>`

```<language>
// <path>:<start>-<end>
<snippet, about 15 lines at most>
```

- **Why it's here:** <the problem it solves>
- **Trade-off:** <what it costs; when you'd choose differently>

### 7.2 <Concept>

<...>

## 8. Why it's built this way

| Decision | Why it makes sense | What it costs | A common alternative |
|---|---|---|---|
| <e.g. Supabase instead of a custom backend> | <...> | <...> | <...> |

## 9. Senior engineer's notes

<Severity-tagged notes, risks first. If the code is clean, say so; that's worth knowing too.>

- **Risk**: <what>. <Why it matters.> `<path:line>`
- **Pain later**: <...>
- **Tidy**: <...>

## 10. Where to make common changes

| If you want to… | Start in | Then also touch |
|---|---|---|
| <add a new page> | `<app/<name>/page.tsx>` | <the nav link in `components/Nav.tsx`> |

## 11. Glossary

| Term | Meaning in this project |
|---|---|
| <middleware> | <code that runs before every request; here it checks login> |
