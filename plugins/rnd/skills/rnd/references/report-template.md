# Report Template — General R&D

Use this exact structure so reports stay comparable across the user's research library.
Write clear prose within sections; use short lists only where they genuinely help
(e.g., option rundowns). Link every load-bearing source. Typical length: 600–1500
words, scaled to the deliverable depth the user chose — long enough to decide from,
short enough to actually get read.

```markdown
# R&D: <Topic>
Date: <YYYY-MM-DD> · Verdict: <Pursue / Park for later / Skip — one line why> · Confidence: <high/medium/low>

## 1. Refined brief
The sharpened target from Phase 1: what is being investigated, for what goal, under
what constraints. Two or three sentences.

## 2. Landscape
What this area is, how it works at the level the user needs, and where it currently
stands (mature/emerging, active development, notable recent shifts).

## 3. Approaches & options
The main ways to do this, compared honestly. For each: what it offers, what it costs
(money, complexity, maintenance burden), and who it suits. If the user's goal was to
pick one, make the comparison decisive rather than diplomatic.

## 4. Reference implementations & tools
3–5 assessed options: link, activity/maturity signals, strengths, gaps, and whether
each is usable as a base, adoptable as-is, or reading material only.

## 5. Requirements
What pursuing this actually needs: infrastructure, services, data, prerequisite
knowledge, and realistic costs of anything not free.

## 6. Risks & gotchas
What practitioners report going wrong — production pain, migration regrets, edge
cases, lock-in. Prefer reported experience over theoretical concerns.

## 7. Recommendation
The verdict with rationale, tied back to the brief's goal and constraints. If the
honest answer is "depends on X", say what X is and how to resolve it cheaply. End
with the one or two findings that would most change this verdict — what to verify
or watch before committing.

## 8. Next step & Claude Code handoff
The single smallest concrete step to start (an experiment, a prototype scope, a
spike), with a measurable definition of success. Then a ready-to-paste handoff
prompt for Claude Code, fenced as a quote block, containing: one-paragraph context,
the chosen direction, hard constraints, and the first milestone. Do not prescribe
code-level details — Claude Code inspects the real environment and plans that itself.

## Sources
Linked list of everything load-bearing.
```
