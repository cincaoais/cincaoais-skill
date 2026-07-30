# Report Templates

Use the template matching the topic type from Phase 1. Keep section headers exactly as
written so reports stay comparable across the user's research library. Write in clear
prose within sections; use short lists only where they genuinely help (e.g., repo
rundowns). Link every source you rely on. Typical report length: 800–2000 words —
long enough to be decision-ready, short enough to actually get read.

---

## Template A — Strategy investigation

```markdown
# R&D: <Topic>
Date: <YYYY-MM-DD> · Type: Strategy · Verdict: <Build & test / Park for later / Skip — one line why> · Confidence: <high/medium/low>

## 1. What it is
Plain-language explanation of the strategy, the market inefficiency or behavior it
tries to exploit, and the core signal/entry/exit logic in pseudocode-level detail.

## 2. Why would the edge exist (and persist)?
The honest section. What is the hypothesis for why this makes money, who is on the
other side of the trade, and why hasn't it been arbitraged away? If the answer is
weak, say so plainly — this section decides the verdict more than any other.

## 3. Evidence from the field
What implementations, papers, and practitioner threads report. Backtest results seen
in the wild vs any live results people share. Explicitly separate marketing claims
from practitioner experience. Note disagreements between sources.

## 4. Reference implementations
3–5 assessed GitHub repos: link, stars/activity, language, what it does well, what's
missing, whether it's usable as a base or only as reading material.

## 5. Requirements
Data (granularity, fields, history depth), execution needs (frequency, order types,
latency tolerance), and any libraries/infrastructure involved. Include realistic
costs of anything not free.

## 6. Failure modes & risks
How this loses money: overfitting risk, regime dependence, transaction costs and
slippage sensitivity, crowding, drawdown profile. Include gotchas practitioners
actually reported, not just theoretical ones.

## 7. Fit with my system
Line up section 5 against references/my-system.md: what's already covered, what's
missing, estimated implementation effort in my stack, and any account-level
constraints (e.g., PDT) that bite. Flag assumptions where my-system.md was blank.

## 8. If I build this — starter plan & Claude Code handoff
Concrete first steps: the minimal version to implement, the first backtest to run
(universe, period, baseline to beat), success criteria to advance to paper trading,
and the criteria that would kill the idea. Small enough to start this week. End with
a ready-to-paste Claude Code handoff prompt (fenced as a quote block): one-paragraph
context, the chosen approach, hard requirements, and the first milestone — no
code-level prescriptions, since Claude Code inspects the real codebase itself.

## Sources
Linked list of everything load-bearing.
```

---

---

## Template B — Feature investigation

```markdown
# R&D: <Topic>
Date: <YYYY-MM-DD> · Type: Feature · Verdict: <Build / Park / Skip — one line why> · Confidence: <high/medium/low>

## 1. What it is & why I'd want it
The capability in plain language and the problem it solves for my system.

## 2. How people build this
Common architectures and approaches found in the wild, with trade-offs between them.
Which approach fits a solo-maintained system best (favor boring, low-maintenance
solutions over impressive ones).

## 3. Reference implementations & tools
3–5 assessed options: open-source repos, libraries, or services. Link, activity,
language/stack match, build-vs-adopt assessment for each.

## 4. Requirements & costs
Data, infrastructure, third-party services, and their real costs (money and ongoing
maintenance burden).

## 5. Risks & gotchas
What practitioners report going wrong: reliability issues, edge cases, ways this
could break existing behavior in my system.

## 6. Fit with my system
Against references/my-system.md: integration points, what's new vs modified, rough
effort estimate, simplest viable version.

## 7. If I build this — starter plan & Claude Code handoff
The minimal first slice, how to test it safely alongside the live system, and a
measurable definition of done. End with a ready-to-paste Claude Code handoff prompt
(fenced as a quote block): context, chosen approach, hard requirements, first
milestone — no code-level prescriptions, since Claude Code inspects the codebase.

## Sources
Linked list of everything load-bearing.
```

---

## Template C — Improvement investigation

```markdown
# R&D: Improve <Strategy/Feature>
Date: <YYYY-MM-DD> · Type: Improve · Verdict: <top recommendation in one line> · Confidence: <high/medium/low>

## 1. Current state
The existing implementation as understood — rules, universe, cadence, sizing — and
which sources this understanding came from (user's summary, past reports,
my-system.md). Flag gaps in the picture explicitly rather than papering over them.

## 2. Symptoms & diagnosis
What's underperforming and the most likely causes, mapped symptom → candidate cause.
Distinguish confirmed causes (from the user's own data or reports) from suspected
ones.

## 3. Improvement candidates (prioritized)
3–5 candidates ordered by expected impact vs effort. For each: the change, the
hypothesis ("adding a volatility regime filter should reduce whipsaw losses in
ranging markets"), evidence from research that it helps this strategy class, and
what it costs (complexity, extra data, higher turnover).

## 4. Test plan
For each candidate worth testing: the exact comparison backtest (baseline vs
variant, universe, period, metrics), the success criterion to adopt it, and the
kill criterion that discards it. Test one variable at a time, and warn about the
overfitting risk of iterating many variants against the same history.

## 5. Risks
Ways an "improvement" makes things worse: curve-fitting to recent regimes, added
complexity and fragility, turnover costs outgrowing the gain, degraded behavior in
market conditions absent from the test window.

## 6. Claude Code handoff
Ready-to-paste prompt (fenced as a quote block): context, the top 1–2 candidates,
the comparison tests to implement, hard constraints — no code-level prescriptions,
since Claude Code inspects the real codebase itself.

## Sources
Linked list of everything load-bearing.
```

---

For **general tech** topics, use Template B and replace section 6's frame with "fit
with my skills and stack" (what I'd learn, prerequisite knowledge, and a learning
path), dropping trading-specific concerns.
