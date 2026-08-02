---
name: ebook-lecture-notes
description: Turn ebooks (PDF, EPUB, DOCX, MOBI, TXT, HTML) into layered study notes written in the voice of a senior lecturer — with named mental models, charts that carry real data, a critical layer that argues against the book, and a self-test. Handles single books or a whole directory in batch. Use this skill whenever the user wants to read, digest, summarize, condense, extract, study, or take notes from a book, ebook, PDF book, paper collection, or documentation set — including phrasings like "summarize this book", "I don't have time to read this", "make notes from these ebooks", "analyze all the ebooks in this folder", "turn this into study material", or "help me understand this book fast". Also use it when the user points at a directory of books and asks for separate notes per book.
---

# Ebook → Lecture Notes

Turn a book someone doesn't have time to read into notes they will actually read, and actually remember.

## The core bet

A 300-page book compressed to 15 pages **has** lost information. That's unavoidable. The trick is to make the loss *recoverable* rather than *permanent*:

> Don't keep everything **in** the notes. Keep everything **reachable from** the notes.

So the output is layered — a short layer people read, sitting on top of longer layers they only open when needed, sitting on top of the untouched source. Total material grows. Reading time collapses.

## Voice: senior lecturer, not summarizer

This is the single most important thing in this skill, and the thing that most easily degrades into slop.

A summarizer writes *"The author discusses the relationship between debt and monetary policy."* Nobody remembers that sentence. Nobody was ever going to.

A good lecturer opens with: *"One bacterium in a glass at 11pm, doubling every minute. Full at midnight. When is it half full?"* — then makes you sit with your wrong answer before explaining why you got it wrong.

Same content. One is furniture; the other lodges.

**Read `references/PEDAGOGY.md` before writing a single line of notes.** It defines the voice concretely, with before/after pairs. Skipping it produces competent, forgettable summaries — the exact failure this skill exists to prevent.

## Workflow

### Step 0 — Scope and triage

If pointed at a directory, list every supported file first and confirm the batch with the user before starting — 12 books is a long run and they should know the shape of it.

Supported: `.pdf .epub .docx .txt .md .markdown .rst .html .htm .rtf .mobi .azw .azw3`

**One output directory per book**, named from the book's slug. Never merge books into one set of notes unless explicitly asked. A failed book gets logged and skipped; it never halts the batch.

```
notes/
├── the-great-devaluation/
│   ├── NOTES.md
│   ├── charts.html
│   └── _source/
│       ├── full_text.txt
│       └── metadata.json
├── thinking-fast-and-slow/
├── _extraction.json        # written by extract.py — machine-readable per-run log
└── _batch-log.md           # written by Claude in Step 8
```

### Step 1 — Extract

```bash
python3 scripts/extract.py --check       # see which extractors are installed
python3 scripts/extract.py <path-or-directory> --out ./notes
```

Writes `full_text.txt` and `metadata.json` per book. It probes for available extractors and tells you what to install if something's missing. For books whose value is in tables, code, or formulas, add `--mode technical` (uses docling, ~1.5s/page). See `references/EXTRACTION.md` for format-specific tools and failure modes.

**Check the extraction before trusting it.** Sample a few hundred characters. Garbled output means a font-encoding problem — rasterize pages and read them visually instead. Silent garbage extraction is the most common way this whole pipeline produces confident nonsense.

### Step 2 — Find the structure

```bash
python3 scripts/outline.py ./notes/<slug>/_source/full_text.txt
```

Get the skeleton before reading any content. It tells you how to spend your reading budget.

**This step fails more often than you'd expect.** Decorative chapter headings — especially vertically-set CJK titles, which extract as one character per line, interleaved and out of order — defeat naive detection completely. The script handles several strategies automatically, including page-break heuristics as a noisy last resort. When they all fail, check whether the table of contents survived extraction as plain text in the front matter — it often does, and reading it there is free. Only rasterize the ToC page when the text version didn't survive. Either way, say so in the notes rather than pretending you have a clean outline.

### Step 3 — Classify the book. This sets everything downstream.

Compression ratio is not a preference. It's a property of the book.

| Type | Tell | Compresses to | Reading strategy |
|---|---|---|---|
| **Single-thesis** | Every chapter argues the same claim from a new angle | **5–10%** | Read the summary layer fully, sample the evidence layer |
| **Cumulative** | Chapter 12 depends on chapter 11 | **20–30%** | Read sequentially; you cannot skip |
| **Reference** | Chapters are independent entries | **30–40%** | Read all headings, sample within each |
| **Narrative** | Sequence *is* the content | **do not compress** | Say so. Offer a map, not a summary |

Getting this wrong is the biggest failure mode. Compressing a textbook at 5% silently deletes whole ideas. Compressing a polemic at 30% produces a long document restating one point.

**What the ratio governs:** the layers a reader reads straight through — the map and the mental models. The lookup layers (evidence, chapter index, what-was-cut) and the critical layer sit outside it; they're consulted, not read. So the notes file for a short book may total more than the ratio suggests, and that's fine — what must collapse is reading time, not file size. Never gut a mandated layer to hit the percentage.

**How to tell fast:** read the introduction and the part-transition passages. Argumentative non-fiction summarizes itself constantly — intro states the thesis, each part restates it, the conclusion restates it. If the same claim appears three times in the first 10% of the book, it's single-thesis.

### Step 4 — Read strategically, and be honest about it

Read in this order, because it front-loads the highest-value text:

1. **Introduction / preface** — the thesis, stated plainly before the author starts defending it
2. **Part-transition passages** — the book summarizing itself. Highest value-per-word in the entire book
3. **The payoff chapter** — where the argument lands. Usually late, sometimes signposted in the intro
4. **Samples from the evidence chapters** — for the concrete numbers, examples, and metaphors

This order is built for argumentative non-fiction. A book classified **Narrative** reads sequentially or not at all — see the narrative note in `references/PEDAGOGY.md`.

**Track what you read and what you didn't.** If you sampled, say so in the notes. A reader who thinks you read 100% will trust chapter ratings that are actually extrapolations. That trust is unearned and will eventually cost them.

The reading-budget buckets in `references/EXTRACTION.md` license sampling; they never forbid reading more. At the low end of a bucket, sampling saves almost nothing — read the whole thing and say so.

For a book that matters, offer a full sequential pass as the more expensive alternative. Let the user choose.

### Step 5 — Write NOTES.md

**Language first.** Write the notes in the book's primary language unless the user asks otherwise. For a translated edition, either the edition's language or the user's working language is defensible — state the choice in one line at the top of NOTES.md, and keep author-coined names bilingual where the original wording is the searchable handle.

Six layers, in this order. `references/PEDAGOGY.md` has the full spec and worked examples for each.

**Layer 1 — The one-page map.** The whole book on one page. The thesis, the argument in 5–7 numbered steps, the single sentence worth remembering, and who is telling you this. If someone reads only this page, they should be able to hold a conversation about the book.

**Layer 2 — Mental models.** 4–8 *named*, portable frameworks. Each gets: the name (keep the author's if they gave one), the model in a form you could redraw on a napkin, a concrete example, and a **"Use it when"** line generalizing it beyond the book. This layer is what's still useful in five years. Prioritize it.

**Layer 3 — The evidence.** Numbers, tables, dates, claims. Tables beat prose here. This is what people come back for.

**Layer 4 — Chapter index.** One line per chapter. Mark the chapters that carry the book (★) versus restatements. State plainly which ratings are verified and which are inferred. End with a verdict: *"chapters 2, 5, 8, 14, 17, 23 ≈ 85% of the value."*

**Layer 5 — The critical layer.** Content the notes **add**. Non-negotiable:
- **Who is telling you this, and what do they gain if you believe it?** A gold dealer's book arguing you should buy gold. A consultant's book arguing you need consultants. Check the author's affiliations. This single question changes how a reader weighs everything else.
- What the book doesn't argue against itself
- Where evidence is thin relative to rhetorical confidence — flag the *most quotable* claims especially, since memorability and rigor are uncorrelated
- Age: what has happened since publication that tests the book's claims — facts you check externally for this get the **[Since]** tag with an inline source
- What's conspicuously absent — including content the document itself advertises as missing (paywalled chapters, "full version only" sections). The shape of the omission is evidence about the author's business, not just a gap

Without this layer you haven't compressed the book, you've absorbed it — including its blind spots.

**Layer 6 — What was cut, and where to find it.** The loss-protection contract. List what you deliberately didn't summarize, and give search terms for the source text.

**Close with a self-test.** 5–7 questions answerable from the notes alone. Tell the reader: whatever you can't answer in a week is where the notes cut too deep — patch that section, don't inflate everything.

### Step 6 — Charts

Read `references/CHARTS.md`, then build `charts.html` from `assets/template.html`. The generated file loads Chart.js and its fonts from CDNs, so it needs internet the first time it's opened.

**The bar: a chart earns its place only when prose fails.** "0.0000001% at 11:30" is a number readers skim past; a line that stays flat across the whole chart then goes vertical is the argument itself. That's a chart. A bar chart of three numbers already legible in a sentence is decoration — cut it.

Aim for 4–8 charts in a typical argumentative book — but the bar overrides the count. A narrative book or a thin document may support one chart, or none; build fewer and say why in the notes. **Every chart gets a "catch" box** stating its weakness, limitation, or what it omits. A chart makes a claim more persuasive than the underlying evidence warrants; that's fine for the author and dangerous for the student. Charting a weak claim without its counterargument is the most harmful thing this skill can do.

### Step 7 — Verify before delivering

- Every number traced to text you actually read — never to memory or inference
- Provenance tagged: **[Book]** / **[Added]** / **[Since]** / **[Verify]** — see `references/CHARTS.md` for the definitions
- Dangling evidence chased down: if the text says "the table below shows…" and no table follows, the table is an image — render that page and read it (see `references/EXTRACTION.md`), don't silently under-report the book's evidence
- Every chart has its catch box
- The critical layer names the author's interest
- Nothing quoted at length — see below
- Self-test questions are all answerable from the notes

### Step 8 — Batch reporting

Write `_batch-log.md`: per book, the type classification, compression achieved, what fraction was read, and any extraction problems. For batches over ~5 books, add a cross-book section — recurring themes, where books contradict each other. Contradictions between sources are among the most valuable things a reader gets from reading several books, and they're invisible when notes live in separate files.

## Copyright

Generated notes are synthesis, not reproduction — treat them like handwritten study notes.

- **Never reproduce passages.** Every idea restated in your own words. No mirroring of sentence structure.
- Factual data — numbers, dates, table values — is not protectable expression; carrying it into notes and charts (that's what the **[Book]** tag marks) is fine. The ban is on reproducing prose expression, not facts.
- **Quotes under 15 words, one per source, only where exact wording carries meaning** a paraphrase would lose. Default to paraphrase.
- **Never reproduce poems, lyrics, or complete short works** in any form.
- Don't reconstruct the book through dense paraphrase packed with its specifics — that's reproduction with extra steps.
- Notes on copyrighted books are for personal use. Don't publish or redistribute them.

## Reference files

- `references/PEDAGOGY.md` — **read before writing.** The lecturer voice, before/after pairs, layer specs
- `references/EXTRACTION.md` — format tools, encoding failures, structure detection strategies
- `references/CHARTS.md` — when a chart earns its place, chart selection, template usage
- `assets/template.html` — the chart document shell
- `scripts/extract.py`, `scripts/outline.py` — extraction and structure detection
