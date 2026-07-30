# Review Report Template — docs/04-REVIEW.md

Use this exact structure. Every claim of "working" needs attached evidence (real command output), never assertions.

# Review & Test Report: [Project Name]

## Verdict
One paragraph: ready / ready with known issues / not ready, and why.

## Review findings
Table: # | finding | severity (critical/major/minor) | where | status (fixed/open).

## Fixes applied
Short list: what was changed and which finding it closes.

## Test results
Full-suite summary (totals, pass/fail) plus the actual test runner output (trimmed to the relevant parts) as evidence.

## Scenario walkthroughs
For each scenario (happy path, edge cases, failure modes):
- Scenario: [name]
- Steps taken
- Expected vs actual
- Result: pass/fail, with output/screenshot evidence

## Plan conformance
Definition-of-done checklist from 02-PLAN.md, item by item, checked off or explained.

## Known issues & limitations
Honest list of what is still imperfect.

## Suggested next steps
Improvements or v2 ideas surfaced during review.
