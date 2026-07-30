# Plan Template — docs/02-PLAN.md

Use this exact structure. The plan must be executable by subagents who have read nothing else except the brief and this file.

# Implementation Plan: [Project Name]

## Goal recap
2–3 sentences restating the brief's goal and success criteria.

## Architecture overview
Components and how they talk to each other. A text/ASCII diagram is enough.

## Tech stack & justification
Each choice must cite the RND finding that supports it (e.g., "chosen because 01-RND.md §Existing solutions showed X and Y both hit scaling problems with Z").

## Milestones & vertical slices
Milestone N: [name]
For each slice inside it:
- **Slice N.M — [name]**
  - What it delivers (must be runnable/testable on its own, cutting across data + logic + interface)
  - Tasks (sized for one subagent each)
  - Acceptance criteria
  - Test gate: the specific tests that must pass before this slice is done
  - Depends on: [slices]
  - Parallelizable with: [slices] (no shared files)

## File / module layout
The intended directory tree so subagents don't invent conflicting structures.

## Execution order & suggested subagent assignment
Ordered list or simple graph: which slices run when, which can run together under the chosen execution style.

## Risks & rollback
What could go wrong per milestone and how to back out.

## Definition of done
The checklist Phase 4 will verify against.
