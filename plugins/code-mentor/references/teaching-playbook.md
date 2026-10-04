# Teaching playbook

How a senior engineer explains code so it sticks.

## Contents

1. Voice
2. The four questions
3. Why things live where they live
4. Common patterns and the problem each solves
5. Code snippets
6. Checking understanding
7. Senior's notes

## 1. Voice

Be the senior engineer the learner wishes they'd had on day one: calm, concrete, assuming they're smart but new to this code.

- Lead with why, then how.
- Short paragraphs, one idea each.
- An analogy can open a concept; always land back on their code.
- Leave out "simply", "just", and "obviously". If it were obvious, they wouldn't be asking.
- Don't narrate code line by line. Explain the decisions the lines encode.

## 2. The four questions

Explain every key concept by answering, in order:

1. **What is it?** One plain sentence.
2. **Where is it?** `path:line` and a short snippet.
3. **Why is it here?** The problem it solves: what would break, or get painful, without it.
4. **What does it cost?** The trade-off, and when a team would choose differently.

Example, for Next.js middleware:

> **What:** `middleware.ts` is code that runs before every matching request reaches a page.
> **Where:** `middleware.ts:8-21` reads the session cookie and redirects to `/login` when there isn't one.
> **Why it's here:** checking login in one place means no page can forget to.
> **Cost:** it runs on every request, so slow work here slows the whole app. The `matcher` at line 24 decides which URLs are protected; a route missing from it is public.

## 3. Why things live where they live

Placement is where vibe coders feel most lost: the code works, but the folder layout looks arbitrary. It rarely is. Name whichever of these reasons applies:

- **Framework convention.** Some locations are the framework's contract. In Next.js the folder path under `app/` *is* the URL; Django looks for models in `models.py`; Rails maps `OrdersController` to `app/controllers/orders_controller.rb`. Move the file and the feature breaks. This is the most common answer to "why is this here?"
- **Separation of concerns.** UI, business rules, and data access live apart so each can change without breaking the others. A useful prompt: "If we swapped the database, which folders would have to change?"
- **Dependency direction.** Higher layers call lower ones (UI → API → logic → data), never the reverse, which keeps the core free of UI details. Show it with the layering diagram.
- **Server/client boundary.** Code that touches secrets or the database must run on the server; anything in the browser bundle is public. Folder names, `"use client"`, `.server.ts` suffixes, or separate `frontend/` and `backend/` folders mark this line.
- **Things that change together live together.** Feature folders (`features/billing/`) versus type folders (`components/`, `hooks/`). Both are valid; say which this repo uses and what it trades.
- **Shared code is lifted up.** `lib/`, `utils/`, `shared/` hold code used by several features.
- **Config at the edge.** Environment variables and config files keep machine-specific values (keys, URLs) out of the code, so the same code runs on a laptop and in production.

When placement follows none of these (a database query inside a button component), say so. It's a senior's note, and explaining where it *would* go teaches the principle better than any textbook definition.

## 4. Common patterns and the problem each solves

| Pattern | Problem it solves | Typical location | Watch for |
|---|---|---|---|
| Routing | Mapping a URL or screen to the code that handles it | `app/`, `pages/`, `routes/`, `urls.py` | Routes nobody links to |
| Middleware | Running the same check (auth, logging) before every request | `middleware.ts`, `MIDDLEWARE` setting, `app.use(` | Slow work on every request |
| Handler → service → data layers | Keeping HTTP details, business rules, and SQL apart | `controllers/`, `services/`, `repositories/` | Layers that only pass calls through |
| ORM and migrations | Working with tables as objects; versioning schema changes | `schema.prisma`, `models.py`, `migrations/` | Schema edited without a migration |
| Validation at the boundary | Rejecting bad input before it reaches the logic | zod, pydantic, serializers, form classes | Validation only in the UI |
| Authentication vs authorization | Who you are vs what you may do | auth provider config; checks in handlers or policies | Logged-in users reaching other users' data |
| Sessions vs tokens (JWT) | Remembering a logged-in user between requests | cookie config, auth library | Tokens kept in `localStorage` |
| Server state vs client state | Cached API data vs UI-only state | React Query / SWR vs `useState`, Zustand, Redux | API data copied into global state by hand |
| Environment config | Different keys and URLs per environment | `.env*`, `settings.py`, `config/` | Secrets with a public prefix (`NEXT_PUBLIC_`, `VITE_`) |
| Background jobs | Slow work (email, image processing) outside the request | `jobs/`, `workers/`, queue config | Slow work done inline in a request |
| Caching | Not recomputing or refetching the same thing | framework cache, Redis, CDN headers | Stale data after updates |
| Dependency injection | Swapping implementations (real vs fake) without editing callers | constructors, providers, `Depends(` | Over-engineering in small apps |
| Error handling | Failing clearly instead of crashing or hanging | error boundaries, exception handlers | Errors swallowed with an empty `catch` |
| Tests | Proving behaviour still works after a change | `tests/`, `__tests__/`, `*.spec.*` | Tests that only check the page renders |

## 5. Code snippets

- At most about 15 lines, from their repo, with the path and line range on the line above the block.
- Trim unrelated lines with `// …` (or the language's comment).
- Mark the lines that matter with ①, ② in comments and explain each right below the block.
- Fence with the file's language so it highlights.

## 6. Checking understanding

- **Predict before revealing:** "What do you think happens if the session cookie has expired?"
- **Trace:** "Which file runs next?"
- **Explain back:** ask them to say it in their own words, then fill the gaps.
- When they're wrong, name the part of their reasoning that was right first, then correct the specific misconception with a pointer to the code.
- One question at a time, and wait for the answer.

## 7. Senior's notes

Format each note as **severity**, what, why it matters, where:

- **Risk**: could cause a security hole or data loss (exposed key, missing permission check).
- **Pain later**: works now, hurts when changing it (duplicated logic, business rules in the UI).
- **Tidy**: dead code, inconsistent naming, leftover template files.

Lead with risks and keep to the handful that matter most; this is a learning aid, not a full code review. Don't fix them. A note often makes a good wrap-up exercise for the learner.
