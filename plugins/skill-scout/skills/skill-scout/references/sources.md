# Sources

`scout.js search` queries every source at once and caps the run at 8 network requests, each with an 8-second timeout. A source that fails is reported as skipped; the rest still return.

| Source | What it searches | Requests | Fallback when it fails |
|---|---|---|---|
| skills.sh | The open skills directory's search API (`skills.sh/api/search`) with all keywords together, then with the top two | 2 | `npx --no-install skills find`. This runs only if the `skills` CLI is already cached locally; the script never downloads it |
| GitHub | Code search for `SKILL.md` files that contain each of the top two keywords | 2 | Without `gh auth login`, GitHub refuses code search, so the script searches repositories instead (name, description, README) |
| Collections | `anthropics/skills` (folder names) plus the READMEs of `ComposioHQ/awesome-claude-skills` and `VoltAgent/awesome-agent-skills` | 3 | Each collection is skipped on its own if it fails |
| Marketplaces | The `marketplace.json` of every marketplace in `~/.claude/plugins/known_marketplaces.json`, excluding plugins already installed | 0 (local files) | None needed |

`scout.js local` reads only local files: `~/.claude/skills` (including claude.ai synced skills), the project's `.claude/skills`, `~/.agents/skills` (the `skills` CLI store), and the `skills/` folder of every installed plugin.

## Adding a collection

Edit `COLLECTIONS` at the top of `scripts/lib/remote.js`. Use `kind: 'tree'` for a repository of skill folders, or `kind: 'list'` for an awesome list whose README links to GitHub skill folders. Each added collection costs one request per search, so raise the budget in `scripts/scout.js` (`buildClient({ budget: 8 })`) to match.

## GitHub rate limits

| Access | Core API | Search API | Code search |
|---|---|---|---|
| Anonymous | 60 per hour per IP | 10 per minute | Not allowed |
| Logged in with `gh auth login` | 5,000 per hour | 30 per minute | Allowed |

The scripts never read tokens themselves. When `gh` is installed and logged in, they call `gh api`, which uses the user's own login. Otherwise they make anonymous HTTPS requests. Each `inspect` costs 3 core requests, and each `install` costs 1. An HTTP 403 that mentions a rate limit means waiting or running `gh auth login`.

## Cache

Every search is stored in `search-cache.json` in the plugin's data folder (`${CLAUDE_PLUGIN_DATA}`, which is removed when the plugin is uninstalled). Outside a plugin, the cache lives in `~/.claude/skill-scout/`. Entries expire after 7 days, and the file holds at most 50.

A later search reuses an entry when:

- its keywords match exactly, in any session, or
- it ran in the same session and at least half its keywords overlap.

Pass `--fresh` to search again anyway.
