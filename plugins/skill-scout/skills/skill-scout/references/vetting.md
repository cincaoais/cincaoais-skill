# Vetting candidates

Rank by **relevance first**, then by trust. A popular skill that is only near the topic loses to a niche skill that fits exactly.

## Relevance

The `score` in the search output counts how many keywords appear in the candidate's name, path, and description. It is a starting point only; skills.sh results often score 1 because only their name is known. Judge relevance yourself:

1. **Exact fit.** Covers this platform or format and this task type. Example: a skill for the exact API or file format being used.
2. **Domain fit.** Same platform, different task, or same task on a closely related platform.
3. **Generic.** A general practice such as "testing" or "API design". Include it only if nothing better exists.

Drop candidates that only share a common word (for example "strategy" matching marketing skills on a trading task). Skills that cover everyday work (git, general coding) don't help a domain search either.

## Trust signals

| Signal | Where it comes from | How to read it |
|---|---|---|
| Publisher | The repo owner | Official vendor orgs (`anthropics`, the platform's own org such as `expo` or `shopify`) and well-known collections rank higher |
| Installs | skills.sh | Over 1K is established. Under 100 is "low adoption" |
| Stars | GitHub, shown by `inspect` | Over 100 is established. Under 20 is "low adoption" |
| Last updated | `inspect` (last commit that touched the skill folder) | More than 12 months old: mark it "stale" and prefer a fresher option |
| Archived | `inspect` | Archived repos aren't maintained. Mention it and rank them lower |
| License | `inspect` | No license means unclear reuse terms. Mention it, but don't drop the candidate for that |

Don't discard a relevant skill for low popularity. Keep it and label it "low adoption" in the Popularity column so the user can decide.

## Shortlist rules

- Show at most 5 candidates. Prefer variety: don't fill the list with five siblings from one repo when one or two cover the need.
- If one repo offers several relevant skills, list the best one or two and mention the rest in its row.
- Already installed and relevant: don't list it. Say it's already installed and use it.
- Marketplace plugins can bundle several skills, MCP servers, or hooks. Say so in "What it does".
- Popularity column format: `12K installs`, `★ 340`, `low adoption (35 installs)`, or `—` when unknown.
