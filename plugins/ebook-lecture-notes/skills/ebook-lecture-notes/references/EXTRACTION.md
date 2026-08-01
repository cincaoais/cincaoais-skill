# Extraction and structure detection

## Contents
1. Format → tool table
2. Diagnose before extracting
3. Failure modes that produce silent garbage
4. Structure detection strategies
5. Reading budget

---

## 1. Format → tool table

`scripts/extract.py` tries these in order and falls back automatically. Run `python3 scripts/extract.py --check` to see what's installed.

| Format | Preferred | Fallbacks | Install |
|---|---|---|---|
| PDF (prose) | `pdftotext` | `pypdf`, `pdfminer.six` | `apt install poppler-utils` |
| PDF (tables, code, formulas) | `docling` | as above | `pip install docling` |
| EPUB | `ebooklib` + `beautifulsoup4` | stdlib `zipfile` | `pip install ebooklib beautifulsoup4` |
| DOCX | `python-docx` | stdlib ZIP/XML | `pip install python-docx` |
| HTML | `beautifulsoup4` | stdlib `html.parser` | `pip install beautifulsoup4` |
| RTF | `striprtf` | regex | `pip install striprtf` |
| MOBI/AZW/AZW3 | Calibre `ebook-convert` | — | calibre-ebook.com |
| TXT / MD | built-in | — | — |

Poppler's install command is Linux-flavored: on macOS it's `brew install poppler`; on Windows there's no easy poppler package, so `pip install pypdf` covers PDFs without it.

**PDF choice matters.** `pdftotext` is instant and fine for prose. `docling` preserves tables and code blocks as markdown but runs ~1.5s/page — 4 minutes for a 160-page book. Use it only when the book's value is in its tables, code, or formulas. For most trade non-fiction, `pdftotext` is correct.

---

## 2. Diagnose before extracting

```bash
pdfinfo book.pdf      # pages, size, producer
pdffonts book.pdf     # is there a text layer at all?
pdftotext -f 1 -l 3 book.pdf - | head -40   # sample it
```

Read the sample. This takes ten seconds and prevents the worst outcome in this whole pipeline.

**Empty `pdffonts` output → the PDF is scanned.** `pdftotext` returns nothing. Rasterize and read visually, or OCR:

```bash
pdftoppm -jpeg -r 150 -f 10 -l 10 book.pdf /tmp/page
```

---

## 3. Failure modes that produce silent garbage

These matter more than the happy path, because each one produces output that *looks* fine and is wrong.

**Mojibake from custom encodings.** Fonts with `Custom` or `Identity-H` encoding and no CIDToGID map extract as wrong characters. Symptom: plausible-looking text that is subtly nonsense, or runs of `\uf000`-range glyphs. Fix: rasterize and read visually.

**Decorative typesetting scrambling word order.** Drop caps, vertical CJK titles, and sidebars extract in visual order, not reading order. A vertically-set 「第五章 威鲸闯天关」 becomes fifteen one-character lines, interleaved with adjacent text. This is not corruption — the characters are all there — but any regex looking for `第N章` will find nothing.

**Ligature loss.** Some PDFs drop `fi`/`fl`. Search the extraction for `nd`, `rst`, `nal` — if present, note it and don't trust exact word matching.

**Multi-column merging.** Two-column academic PDFs interleave lines without `-layout`. Always use `pdftotext -layout` for anything that might be columnar.

**EPUB extracted via stdlib zipfile** loses chapter boundaries entirely — you get one continuous blob. If chapter detection fails on an EPUB, check whether `ebooklib` was actually available before concluding the book has no chapters.

**Rule: sample the output every time.** A confident pipeline over garbage input produces confident garbage output, and nothing downstream will catch it.

---

## 4. Structure detection strategies

`scripts/outline.py` runs strategies A, B, and C automatically, in that order, falling back as confidence drops. Strategy D is not run by the script — it's the manual fallback the script's own low-confidence output should send you to. Understand all four, because when the automated ones fail you need to know which one to reach for.

**Strategy A — explicit headings.** Line-initial `Chapter N`, `第N章`, `Capítulo N`, `제N장`, Roman numerals, `Part N`. Works on most Western trade non-fiction. It also matches the `@@CHAPTER@@` markers that extract.py's EPUB and DOCX parsers insert at real heading boundaries.

**Strategy B — vertical CJK reconstruction.** Detects runs of 4+ consecutive single-character lines and concatenates them. This is how Chinese and Japanese ebooks typeset chapter titles, and Strategy A never finds them.

Note that the reconstruction is often *scrambled* — the characters are all present but interleaved with the chapter number, so 「第5章 威鲸闯天关」 may reconstruct as `第威5章鲸闯天关`. That's fine. You're locating the boundary, not reading the title. Get the line number, then read the surrounding text to learn what the chapter is actually called.

**Strategy C — page-break clustering.** Form feeds (`\f`) followed by short lines and a large blank gap. Noisy; use as a last resort.

**Strategy D — read the ToC page directly.** Rasterize the table of contents page and read it visually. Slower but always works, and worth it for a book you're going to rely on.

**When everything fails:** say so in the notes. Structure the notes by argument rather than by chapter, and note that chapter references are approximate. Do not fabricate a chapter list — a reader who goes looking for "chapter 7" on your say-so and finds something unrelated will stop trusting everything else in the document.

---

## 5. Reading budget

After extraction, estimate: `characters ÷ 3.5` ≈ tokens for CJK, `÷ 4` for Latin scripts.

| Book size | Strategy |
|---|---|
| < 30K tokens | Read it all. Sampling saves nothing worth having. |
| 30–80K | Read the summary layer fully, sample evidence chapters |
| 80–200K | Strategic read per SKILL.md Step 4. Track coverage. |
| > 200K | Strategic read, and tell the user what fraction you covered |

**Always report coverage.** "Read approximately 13% — introduction, all part-transition passages, the payoff chapter, and samples from six evidence chapters" is honest and lets the reader calibrate. Silence implies you read everything, and that implication will be believed.
