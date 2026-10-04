# Quiz design

How to write, run, and grade the multiple-choice quiz.

## Contents

1. Size and mix
2. Writing a good question
3. What goes in ANSWERS.md
4. Running the quiz interactively
5. Grading a quiz taken on their own

## 1. Size and mix

Default to 10 questions: 5 for a single file, up to 15 for a whole large project. Any number the user asks for wins.

| Category | Tests | Share | Example stem |
|---|---|---|---|
| Navigate | Knowing where things live | ~20% | "Where is the check that stops a user deleting someone else's post?" |
| Trace | Order of execution and data flow | ~30% | "After the user clicks *Place order*, which file runs first on the server?" |
| Reason | Why it's built this way | ~30% | "Why is the Stripe secret key read in `lib/stripe.ts` and not in the checkout page?" |
| Apply | Predicting the effect of a change | ~20% | "You add a `phone` column to `User`. Besides the schema, which file must change for the signup form to save it?" |

For learners new to coding, shift weight toward Navigate and Trace; for experienced learners, toward Reason and Apply. Order questions from easiest to hardest.

## 2. Writing a good question

- **Ground it in this codebase.** A question someone could answer without having seen the code is trivia, not a check of understanding.
- **One correct answer**, confirmed against the code before you write it down.
- **Four options, A–D**, similar in length and grammar, so the longest or most detailed option isn't a giveaway.
- **Wrong options are real misconceptions:** the right idea in the wrong file, a server/client mix-up, a plausible but wrong order of steps, a reason that sounds right in general but isn't true here.
- Skip "all of the above" and "none of the above". Avoid negative stems; if one is unavoidable, bold the **not**.
- Spread correct letters roughly evenly across the quiz.
- A short code snippet (up to about 8 lines) in the stem is fine when the question is about reading code.

## 3. What goes in ANSWERS.md

For each question: the correct letter and option text; why it's right, with `path:line`; one line per wrong option saying what it gets wrong; and the lesson section to revisit.

The wrong-option lines do the most teaching. A learner who picked C needs to know what C got wrong, not only that B was right.

## 4. Running the quiz interactively

With AskUserQuestion:

- Up to 4 questions per call, each with its four options in A–D order.
- `header` (12 characters max): `Q3 · Trace`.
- `question`: the full stem. If it needs a code snippet, show the snippet in your message just before the call, since the question field is plain text.
- Option `label`: the letter and a short form, e.g. `B. middleware.ts`. Option `description`: the full option text.
- The tool adds an "Other" choice automatically. Treat a typed answer as "unsure": mark it wrong, but respond to what they wrote.

After each batch, say which they got right and give each miss its short why and code pointer, then ask the next batch. At the end, append an attempt to "Your attempts" in `ANSWERS.md`: date, score, a table of their picks, and a revisit list linking each miss to its lesson section. Retakes add a new attempt below the earlier ones.

## 5. Grading a quiz taken on their own

- **In `QUIZ.md`:** read the `[x]` box under each question.
- **In the viewer:** they paste lines like `Q1: B` from the "Copy my answers" button.

Grade against `ANSWERS.md`, explain each miss as in §4, and record the attempt the same way.
