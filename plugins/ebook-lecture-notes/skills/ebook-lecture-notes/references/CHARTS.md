# Charts

## The bar

**A chart earns its place only when prose fails.** That's a high bar and most candidate charts don't clear it.

Prose fails in exactly four situations:

| Prose fails at | Because | Chart |
|---|---|---|
| **Magnitudes across orders** | "0.0000001%" is a number readers skim past | Line or log scale |
| **Shape over time** | Flat-then-vertical is a *shape*, not a value | Line |
| **Comparison across many items** | 4+ things on 2+ dimensions won't hold in a sentence | Grouped bar |
| **Ratio between two quantities** | 37× is abstract; two bars of wildly different length is not | Horizontal bar |

**Cut it if:** the numbers are already legible in a sentence (three values → write the sentence), the chart restates its own caption, or you're making it because the section felt text-heavy. That last one is the most common and the least defensible.

Aim for 4–8 charts in a book's notes. More than that and each one stops being an event.

## Every chart gets a catch box

Non-negotiable.

A chart makes a claim *more persuasive* than the underlying evidence warrants. Axes imply precision. Smooth lines imply mechanism. That's an acceptable trade for an author arguing a case; it's a disservice to a student trying to evaluate one.

So every chart carries a box stating its weakness — what it omits, where the data is soft, what a critic would say.

> **Example.** Chart: gold's purchasing power vs. a $20 bill over 90 years, measured in bespoke suits. Visually devastating.
>
> **Catch:** Ninety years of dividends, rent, and interest are missing. A $20 bill left in a drawer was never the alternative — the alternative was $20 *invested*, which over the same window substantially outperformed the ounce. The comparison is honest about inflation and silent about opportunity cost.

The catch box is often the most valuable text on the page.

## Provenance tags

Every chart caption carries one or more:

- **[Book]** — figures from the text
- **[Added]** — your framing, indexing, or comparison
- **[Verify]** — load-bearing and should be independently confirmed

If you indexed two series to a common baseline to show a relationship the author asserted but never plotted, that's **[Book]** data with **[Added]** presentation. Say both.

In `template.html` these map to the CSS classes `tag-book`, `tag-mine`, and `tag-check` respectively — the class names don't match the tag vocabulary, so don't assume you can rename one without updating the other.

## Building it

Use `assets/template.html`. One file, no build step — everything except Chart.js (cdnjs) and fonts (Google Fonts) is inline, so it needs internet the first time it's opened; charts render blank offline.

The template supplies a ledger-paper palette — pale cool ground, tabular monospace figures, brass and oxide accents. It's built for long-form reading rather than dashboard scanning. Replace the palette if the book's subject suggests something better; keep the structure.

**Structural rules:**
- One chart per section, with its explanation attached — never a gallery of charts followed by a wall of text
- Lead each section with the puzzle or the claim, then the chart, then the reading, then the catch
- Numbers in monospace with tabular figures, so columns align
- Forecasts and projections must be visually distinct from observations — dashed border, reduced opacity. A prediction rendered identically to a measurement is a lie of formatting.

**Signature-number treatment.** When a book turns on a single number — `$42.22`, a threshold, a date — set it large in monospace as a standalone element *before* charting it. Two numbers side by side at 46px land harder than any bar chart. Let the chart follow once the pair has registered.

## Chart type selection

| You want to show | Use | Not |
|---|---|---|
| Growth shape over time | Line | Bar (hides the shape) |
| A few discrete magnitudes | Vertical bar | Line (implies continuity) |
| One dominant ratio | Horizontal bar | Pie (impossible to compare) |
| Two series with different units | Dual line, log scale, indexed | Dual y-axes (arbitrary and misleading) |
| Composition | Stacked bar | Pie |
| Distribution | Histogram | Anything else |

**Never pie charts.** Humans compare angles badly. There is always a better option.

**Log scale when spanning orders of magnitude** — and label it as log on the axis title, since an unlabelled log scale flattens exponential growth into something reassuring, which inverts the point you were making.

## Accessibility floor

- Never rely on color alone — pair with dash pattern, position, or direct labels
- Legible at mobile width; the template handles this
- Real `<table>` markup for tabular data, not a chart of six numbers
