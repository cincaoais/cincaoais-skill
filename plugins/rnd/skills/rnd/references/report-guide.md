# Report guide

The report exists to support a decision. It is not a literature review and not a link dump. Write it
for a solo engineer who has to choose what to learn, adopt or build next — and who would rather reuse a
proven framework than start from zero.

## Required elements

Each of these earns its place. If one is empty, say so briefly rather than padding it.

- **Bottom line and confidence.** One short section: the answer, the confidence (high / medium / low),
  and the reason for that confidence. A reader should be able to stop here.
- **Options and honest trade-offs.** What each credible option offers and what it costs — money,
  complexity, maintenance, lock-in, learning time. Make it decisive when the goal was to pick one;
  "it depends" is only useful when followed by what it depends on.
- **Reference repos and frameworks.** The reusable things the user should learn from or build on,
  assessed in the table below. This is the heart of the report, not an appendix.
- **Evidence with links, dates and tier.** Every load-bearing claim is attributable. Date the source
  when recency matters, and mark the tier (see below).
- **Disagreements.** Where credible sources conflict, say so and give the likely reason. Do not average
  them into a false consensus.
- **What would change the verdict.** The one or two findings, measurements or events to verify or watch
  before committing. This is the calibration, not a hedge.
- **Coverage gaps.** Sources that were skipped, blocked, unavailable or too thin, and what they might
  have added.
- **Next step and handoff.** The smallest concrete first step, with a measurable definition of success,
  followed by the ready-to-paste Claude Code prompt.

## Reference-repo table

Use these columns. A missing value is written as "unknown", not guessed.

| Repo | What to take from it | Stars | Last push | Licence | Maturity | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| `owner/name` | The pattern, module or idea worth reusing | 12.4k | 2026-09-14 | MIT | production | link to repo or release |
| `owner/other` | A narrower utility, reference implementation | 830 | 2025-03-02 | Apache-2.0 | usable | link to issue or README |

Maturity is a judgment: **production** (used by others, tests, releases, responsive maintainers),
**usable** (works, thinner maintenance or docs), **experimental** (promising, unfinished),
**abandoned** (no meaningful activity, unresolved issues). Say which part of a repo is worth
copying — the architecture, a specific module, the test harness, or just its issue threads.

## Evidence tiers

- **Official / primary** — the project's docs, source code, release notes, licence, pricing page,
  paper. Best for capabilities, limits and API reality.
- **Practitioner** — a detailed write-up, an issue with a reproduction, a post-mortem, a benchmark
  someone ran. Best for how it behaves in production and what breaks.
- **Anecdotal** — short posts, comments, videos, second-hand claims. Useful leads and colour, but they
  never settle a verdict alone.

Aim for two independent sources on anything load-bearing. When the only evidence is anecdotal, say so
and lower the confidence.

## Example skeleton (an option, not a mandate)

Merge, rename or drop sections to fit the question. For improve mode, replace the landscape and options
sections with current state, diagnosis and prioritized candidates. For update mode, open with "What
changed".

```markdown
# R&D: <topic>
Date: <YYYY-MM-DD> · Verdict: <Pursue / Park / Skip — one line> · Confidence: <high / medium / low>

## Bottom line
The recommendation, the confidence and the main reason.

## What already exists
The reusable landscape in two or three paragraphs: the established approaches, who uses them, and
where the field is moving.

## Options and trade-offs
The shortlist, each with what it offers and what it costs. Decisive when a choice is expected.

## Reference repos and frameworks
The table above, with a sentence on what each contributes.

## Evidence
The load-bearing claims with links, dates and tiers. Keep it readable; put the long tail in Sources.

## Disagreements and uncertainty
What credible sources disagree about, and what would resolve it.

## Coverage gaps
What could not be reached or answered, and what it would have added.

## Next step
The smallest experiment or prototype, its success criterion, and the handoff prompt.

## Sources
Every load-bearing link, with its date if recency matters.
```

## The handoff prompt

End with a fenced block the user can paste into Claude Code. It contains a compact context paragraph,
the chosen direction and why, the hard constraints, and the first milestone with its success test. It
does **not** prescribe file layout, libraries or code-level steps — Claude Code inspects the real
environment and plans that itself. Keep it free of credentials and of claims the report did not
support.

## Length and style

A focused question fits in one or two screens. A landscape question legitimately needs more. Length
follows the number of real options and the amount of evidence, never a word target: cut padding
sections, repeated context and long link lists before cutting trade-offs or the next step. Use prose
for reasoning and tables for comparisons; a report that is only bullets usually hides the judgment the
user needs.