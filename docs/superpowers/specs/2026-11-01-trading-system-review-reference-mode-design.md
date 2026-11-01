# trading-system-review: reference mode and refresh (design)

Date: 2026-11-01. Author: Opus (coordinator). Builder: a pi worker via Orca orchestration.

## Why

The user no longer builds trading systems from scratch. They learn established frameworks
(e.g. freqtrade, NautilusTrader, QuantConnect Lean, vectorbt, Jesse, hummingbot, MT5 EAs) and take
GitHub repos as references.

The skill already audits *any* repo, but every word assumes "your system". Most public trading
repos carry look-ahead bias, overfit parameters or unrealistic costs. That is exactly what this
skill tests for, so it becomes more useful in a "learn from other people's repos" workflow, not
less.

## Hard constraints

- **Do not modify `scripts/review.py` or `scripts/test_review.py`.** `review.py` hard-fails unless
  `verdict` is one of `DEPLOY, DEPLOY-REDUCED, INCUBATE, REVAMP, RETIRE`. It also warns unless
  `dimensions` match the 10 rubric names and weights exactly. Reference mode must live inside
  those rules.
- Keep own-system mode working exactly as today: same phases, evidence rules, outputs and
  scorecard schema. Additions only, apart from the refresh items below.

## Changes

### 1. Two modes (SKILL.md)

- **own** (today's behaviour): "rate my system", "is my system still working".
- **reference** (new): "is this repo, framework or strategy worth learning from or building on?",
  "vet this GitHub trading bot".
  - Selected when the argument is a GitHub/GitLab URL, or the user's wording is about adopting or
    learning from someone else's code.
  - If unclear, ask once.

Add a short "Modes" section near the top. Then, in each phase, add a clearly marked
**Reference mode:** paragraph for the differences. Don't fork the whole document.

### 2. Reference-mode differences per phase

- **Phase 0:**
  - Clone with `git clone --depth 1 <url> OUT/src`, or use the given local path.
  - Record the URL and commit SHA (`git -C OUT/src rev-parse HEAD`).
  - Set `OUT = ./trading-reviews/ref-<owner>-<repo>-<YYYY-MM-DD>/`.
  - Never run live or paper trading. Install only the dependencies the backtest needs, inside a venv
    in OUT.
  - The contamination check still applies, but it is usually clean for a third-party repo.
- **Phase 1 (system-map) adds:**
  - Framework and version.
  - Licence (SPDX) and whether it allows private use and modification.
  - Repo health via `gh api repos/<o>/<r>`: stars, forks, `pushed_at`, `archived`, open issues,
    latest releases, contributor count.
  - **Every performance claim in the README, listed as a CLAIM to test, not as evidence.**
- **Phase 2:**
  - The edge thesis may be "none stated".
  - The backtest plan tries to **reproduce the README's claims** on the same period, then extends
    to the latest data.
  - The search plan adds playbook group F (below).
- **Phase 3:**
  - W2 reports "claimed vs reproduced" per claim.
  - W3 also runs group F.
- **Phase 4:**
  - Score the same 10 dimensions. `verdict` uses the existing enum and judges the strategy as-is.
  - **Add** an `adoption` block to `scorecard.json`:
    ```json
    "adoption": {
      "verdict": "ADOPT-AS-BASE | LEARN-FROM | AVOID",
      "why": "2-3 sentences",
      "license": "SPDX id", "license_ok_for_private_use": true,
      "maintenance": "active | slowing | abandoned, with pushed_at date",
      "claims": [{"claim": "...", "reproduced": "yes | no | partly | not testable", "evidence": "metric path or file"}],
      "what_to_take": ["ideas, modules, patterns worth reusing"],
      "what_to_avoid": ["bugs, biases, bad patterns found"]
    }
    ```
  - **Start `summary` with `Adoption: <VERDICT>, <one-line why>.`** `review.py` renders `summary`
    but not `adoption`, so this is how the adoption verdict reaches `report.html`.
- **Phase 5 (reference mode):**
  - The chat summary leads with the adoption verdict, then the claims reproduced vs not, then what
    to take and what to avoid.

### 3. Rubric: new "Reference adoption" section (references/rubric.md)

Append it. Do not change the 10 dimensions or their weights.

- **AVOID:**
  - the `data_code_integrity` gate fails with look-ahead or survivorship that isn't a small fix;
  - or the licence forbids the intended use;
  - or the repo is archived or abandoned and its backtest doesn't run.
- **LEARN-FROM:**
  - the code or ideas are useful, but the edge is unproven or overfit (`overfitting_control` ≤ 2),
    or claims don't reproduce;
  - or maintenance is weak.
- **ADOPT-AS-BASE** needs all four:
  - the integrity gate passes;
  - the licence allows the use;
  - there was a push within ~12 months, or it's a stable, widely used framework;
  - the core claims reproduce within tolerance (state the tolerance used).

### 4. Search playbook refresh (references/search-playbook.md)

- **Make it instrument-agnostic.** Keep the gold, prop-firm and MT5 queries, but present them as
  examples for those markets, not defaults. Placeholders already exist; make the wording neutral.
- **Add group F, "Reference repo reputation"** (W3, reference mode only), with at least these
  queries:
  - `"<owner>/<repo>" reddit`
  - `<repo> backtest results real OR live`
  - `<repo> look-ahead OR repainting OR "doesn't work"`
  - `site:github.com <repo> issues lookahead`
  - Forks that fixed bugs: `gh api repos/<o>/<r>/forks?sort=stargazers`.
- **Tools section:**
  - Replace the inline `python -c "from cloakbrowser import launch ..."` one-liner with the bundled
    helper `python "<skill-dir>/scripts/stealth_fetch.py" --url URL --format md`. W5 copies the
    script from the rnd plugin.
  - Interface: `--check` (exit 3 if not installed), `--url` (repeatable), `--headed`, `--profile`,
    `--login URL`, `--max-chars`, `--format json|md`. Output fields include `blocked` and
    `block_reason`.
  - Replace "Don't install packages yourself" with: if `--check` says not ready, ask the user once
    to install CloakBrowser now or skip the bot-walled sites. Record skipped sources under
    `limitations`.
  - Keep "never use Claude-in-Chrome for this research" (the independence rationale still holds).

### 5. Small refresh items

- **Frontmatter `description`:**
  - Add reference-mode triggers ("vet this trading repo", "is this GitHub bot any good", "should I
    build on <framework/repo>").
  - Replace "Not for researching a new strategy idea (rnd) or building a new system
    (system-builder)" with "Not for open-ended research on a new idea or framework (use rnd)".
    `system-builder` has been removed.
- **`argument-hint`:** `"<path-to-trading-repo | github-url>"`.
- Remove every other mention of `system-builder` and `trading-rnd` anywhere in this plugin.
- **`plugin.json`:** version → `1.1.0`, and the description mentions reference mode.

## Acceptance

- `grep -rn -i "system-builder\|trading-rnd" plugins/trading-system-review` returns nothing.
- `git diff --stat` shows no change to `scripts/review.py` or `scripts/test_review.py`.
- `python -m pytest plugins/trading-system-review/skills/trading-system-review/scripts -q` passes
  (run by W5).
- The SKILL.md own-mode text is unchanged except the description, argument-hint, Modes section,
  the marked Reference-mode paragraphs and the search-tool wording.
