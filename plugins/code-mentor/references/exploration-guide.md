# Exploration guide

How to build an accurate map of an unfamiliar codebase quickly. The map is your notes, not the lesson; the lesson is written from it in step 3.

## Contents

1. Reading order
2. Ecosystem and framework signals
3. Finding the golden path
4. What to record
5. Spotting vibe-code artifacts
6. Large repositories and monorepos

## 1. Reading order

Go from broad to narrow; each step tells you where to look next.

1. **List the files**, skipping dependencies and build output:

   ```bash
   if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then git ls-files; \
   else find . -type f -not -path '*/node_modules/*' -not -path '*/.git/*' \
     -not -path '*/.venv/*' -not -path '*/dist/*' -not -path '*/build/*'; fi | head -300
   ```

2. **README and docs**: the intended purpose. They are often out of date; when they disagree with the code, trust the code and mention the gap.
3. **Manifest**: the dependency list names the stack (§2).
4. **Entry points**: where execution starts (§2).
5. **Routes or screens**: the list of things a user can do.
6. **Data model**: what the app remembers.
7. **External services and config**: SDK clients, config files, environment variables.
8. **Tests**: they show what the author thought mattered and are often the clearest usage examples.
9. **Deployment**: `Dockerfile`, `docker-compose.yml`, `vercel.json`, CI workflows. How it runs outside the laptop.

List environment variable names without their values:

```bash
for f in .env.example .env.local.example .env; do [ -f "$f" ] && sed -E 's/=.*//' "$f"; done | sort -u
```

## 2. Ecosystem and framework signals

| Manifest | Ecosystem | Look next at |
|---|---|---|
| `package.json` | JavaScript / TypeScript | `scripts` (how it runs), `dependencies` (which framework) |
| `pyproject.toml`, `requirements.txt` | Python | framework package, `[project.scripts]` |
| `go.mod` | Go | `main.go`, `cmd/*/main.go` |
| `Cargo.toml` | Rust | `src/main.rs`, `src/lib.rs` |
| `pom.xml`, `build.gradle(.kts)` | Java / Kotlin | `src/main/...` |
| `Gemfile` | Ruby | `config/routes.rb` |
| `composer.json` | PHP | `routes/` |
| `*.csproj`, `*.sln` | .NET | `Program.cs` |
| `pubspec.yaml` | Dart / Flutter | `lib/main.dart` |

| Framework (signal) | Entry point | Routes / screens | Data |
|---|---|---|---|
| Next.js (`next`) | `app/layout.tsx` or `pages/_app.tsx` | `app/**/page.tsx` (folder path = URL), `app/**/route.ts` (API); `middleware.ts` runs first | `prisma/schema.prisma`, Drizzle schema, `supabase/migrations/` |
| React SPA on Vite (`vite`, `react`) | `index.html` → `src/main.tsx` | router config, `src/pages/` | usually a remote API |
| SvelteKit (`@sveltejs/kit`) | `src/routes/+layout.svelte` | `+page.svelte`, `+server.ts` | ORM schema |
| Express / Fastify / Hono | file that calls `listen(` | `app.get(`, `router.post(` | `models/`, ORM schema |
| NestJS (`@nestjs/core`) | `src/main.ts` | `*.controller.ts` | `*.entity.ts`, Prisma |
| Django | `manage.py`, `settings.py` | `urls.py` → `views.py` | `models.py`, `migrations/` |
| FastAPI | `main.py` with `FastAPI()` | `@app.get`, `APIRouter` | SQLAlchemy / SQLModel models |
| Flask | `app.py` with `Flask(__name__)` | `@app.route`, blueprints | `models.py` |
| Rails | `config/application.rb` | `config/routes.rb` → `app/controllers/` | `app/models/`, `db/schema.rb` |
| Laravel | `public/index.php` | `routes/web.php`, `routes/api.php` | `app/Models/`, `database/migrations/` |
| Spring Boot | class with `@SpringBootApplication` | `@RestController` | `@Entity` classes |
| Go (`net/http`, Gin, Echo) | `main.go` | `HandleFunc(`, `r.GET(` | structs + `database/sql` or GORM |
| Expo / React Native | `app/_layout.tsx` (expo-router) or `App.tsx` | `app/` folder | AsyncStorage, remote API |
| Supabase / Firebase as backend | file calling `createClient(` / `initializeApp(` | n/a | `supabase/migrations/`, `firestore.rules` |

These are signals, not guarantees. Confirm by opening the file.

## 3. Finding the golden path

Candidates, best first:

- The action the README or landing page leads with.
- The form or button that writes to the database.
- The route with the most code behind it (handler, service, model).

Trace it fully: UI event → client call → route or handler → validation → business logic → data access → response → UI update. Record each hop as `path:line: what happens`. A missing hop (no validation, no error handling) is a senior's note.

## 4. What to record

- Purpose, in one sentence.
- Stack: layer, technology, its job here, where it lives.
- Entry points.
- Each top-level folder and its responsibility.
- Golden path hops with `path:line`.
- Entities and their relationships.
- External services and which files call them.
- Auth: where identity is established, and where it is checked.
- Config: environment variable names and where they're read.
- Senior's-note candidates (§5).
- Common-change map: "to add a page / an API field / a database column, touch …".

## 5. Spotting vibe-code artifacts

Common in AI-generated projects. Each is worth a gentle note, and the first two are worth a firm one:

- **Secrets in client-side code.** Anything shipped to the browser is public.
- **Database access from the client without row-level security** (Supabase, Firebase).
- Missing input validation or error handling on routes.
- Two ways of doing the same thing (`fetch` and `axios`, two date libraries, CSS modules and Tailwind).
- Logic duplicated across files instead of shared.
- Business logic inside UI components.
- Unused files, components, or exports (grep for their imports).
- Commented-out blocks, TODOs, placeholder data, leftover template code.

Search hints. The secret search prints `file:line` only, so values never enter the conversation:

```bash
grep -rnE "TODO|FIXME|HACK" --exclude-dir={node_modules,.git,dist,build,.venv} . | head -20
grep -rnoE "(sk_live_|sk-[A-Za-z0-9]{8}|AKIA[0-9A-Z]{8}|api[_-]?key\s*[:=]\s*['\"])" \
  --exclude-dir={node_modules,.git,dist,build,.venv} . | cut -d: -f1,2
```

## 6. Large repositories and monorepos

- Over a few hundred source files: map the top level first, then ask the user to pick an area or confirm the golden path before going deep.
- Monorepos (`apps/*`, `packages/*`, `pnpm-workspace.yaml`, `turbo.json`, `nx.json`): treat each app as its own system, and show which shared packages they import.
- With subagents available, map areas in parallel; each returns the §4 notes for its area.
