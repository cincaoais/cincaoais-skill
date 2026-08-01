#!/usr/bin/env python3
"""
Find chapter boundaries in extracted text. Run before reading anything.

  python3 outline.py notes/<slug>/_source/full_text.txt
  python3 outline.py notes/<slug>/_source/full_text.txt --context 4
  python3 outline.py notes/<slug>/_source/full_text.txt --json

Four strategies, tried in order. Reports which worked and how confident,
because a wrong outline is worse than no outline: a reader who looks up
"chapter 7" on your say-so and finds something else stops trusting the
whole document.
"""

import argparse, json, re, sys
from pathlib import Path

# Windows consoles and pipes often default to a legacy code page (cp1252,
# cp936); the first CJK chapter title printed would then crash the script
# with UnicodeEncodeError — even with stdout redirected to a file.
for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        _stream.reconfigure(encoding="utf-8", errors="replace")

# Strategy A — explicit headings. norm() strips ALL whitespace from a line
# before matching, so no pattern may require whitespace (\s+) — "Chapter 5"
# arrives here as "Chapter5".
HEADING_PATTERNS = [
    (r"^(?:CHAPTER|Chapter)\s*([0-9#]+|[IVXLC]+)\b", "en-chapter", "chapter"),
    (r"^(?:PART|Part)\s*([0-9]+|[IVXLC]+|One|Two|Three|Four|Five|Six)\b", "en-part", "part"),
    (r"^第\s*([0-9〇零一二三四五六七八九十百#]+)\s*[章回節节]", "cjk-chapter", "chapter"),
    (r"^第\s*([0-9〇零一二三四五六七八九十#]+)\s*部分?", "cjk-part", "part"),
    (r"^제\s*([0-9]+)\s*장", "ko-chapter", "chapter"),
    (r"^(?:Capítulo|Capitolo|Kapitel|Chapitre)\s*([0-9]+|[IVXLC]+)\b", "eu-chapter", "chapter"),
    (r"^@@CHAPTER@@\s*(.*)$", "structural", "chapter"),
]

# prose punctuation — a real heading almost never contains these.
# Colons are deliberately absent: "Chapter 5: The Meeting" is a heading.
PROSE_MARKS = "。，、；！？.,;!?"

CJK_NUM = {"〇": 0, "零": 0, "一": 1, "二": 2, "三": 3, "四": 4, "五": 5,
           "六": 6, "七": 7, "八": 8, "九": 9, "十": 10}
ROMAN = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100}


BMP_PUA = re.compile(r"[\ue000-\uf8ff]")


def depua(s):
    """
    Recover characters hidden in Private Use Areas.

    Subsetted fonts frequently remap glyphs into a PUA. The supplementary
    areas (plane 15 and 16) are usually a straight ASCII offset — a digit '1'
    becomes U+F0031, whose low byte is still 0x31. Those decode exactly, which
    means chapter NUMBERS are recoverable, not merely locatable.

    The BMP PUA (U+E000-U+F8FF) carries no such guarantee, so mask it with '#'
    to keep the heading matchable without inventing a number.
    """
    out = []
    for c in s:
        o = ord(c)
        if 0xF0000 <= o <= 0x10FFFD:
            low = o & 0xFF
            out.append(chr(low) if 0x20 <= low <= 0x7E else "#")
        else:
            out.append(c)
    return BMP_PUA.sub("#", "".join(out))


def norm(line):
    """
    Collapse internal whitespace and neutralize private-use glyphs.

    Two extraction artifacts break naive matching, and both are common:

    1. `pdftotext -layout` renders a vertically typeset CJK title as
       `第       一       部       分` on one line; without -layout the same
       title becomes one character per line. Collapsing whitespace makes the
       first case matchable; Strategy B handles the second.

    2. Books embedding subsetted fonts often encode DIGITS as private-use
       characters, so a chapter heading extracts as `第<PUA>章` and no digit
       pattern will ever match it. Mapping PUA to '#' lets the heading be
       found even though the number itself is unrecoverable from the text
       layer. The boundary is what matters; read the number from the page.
    """
    return depua(re.sub(r"\s+", "", line)).strip()


def looks_like_prose(raw, normalized):
    """Reject sentence fragments that merely mention a chapter number."""
    if len(normalized) > 40:
        return True
    if any(c in raw for c in PROSE_MARKS):
        return True
    # a heading rarely runs to the width of a text column
    if len(raw.rstrip()) > 70:
        return True
    return False


def _cjk_small(s):
    """0–99 in CJK numerals."""
    if s == "十":
        return 10
    if len(s) == 1:
        return CJK_NUM.get(s)
    if s.startswith("十"):
        return 10 + CJK_NUM.get(s[1], 0)
    if "十" in s:
        a, _, b = s.partition("十")
        if a not in CJK_NUM:
            return None
        return CJK_NUM[a] * 10 + (CJK_NUM.get(b, 0) if b else 0)
    return None


def parse_num(s):
    s = s.strip()
    if s.isdigit():
        return int(s)
    if s and all(c in CJK_NUM or c == "百" for c in s):
        if "百" in s:  # 一百二十三, 一百零三, 二百
            a, _, b = s.partition("百")
            if a and a not in CJK_NUM:
                return None
            total = (CJK_NUM[a] if a else 1) * 100
            b = b.lstrip("零〇")
            if b:
                rest = _cjk_small(b)
                if rest is None:
                    return None
                total += rest
            return total
        return _cjk_small(s)
    if s and all(c in ROMAN for c in s.upper()):
        vals = [ROMAN[c] for c in s.upper()]
        total = 0
        for i, v in enumerate(vals):
            total += -v if i + 1 < len(vals) and v < vals[i + 1] else v
        return total
    return None


def strategy_a(lines):
    """Explicit headings on whitespace-normalized lines."""
    hits = []
    for i, raw in enumerate(lines):
        if not raw.strip():
            continue
        n = norm(raw)
        if not n or looks_like_prose(raw, n):
            continue
        for pat, kind, level in HEADING_PATTERNS:
            m = re.match(pat, n)
            if m:
                hits.append({"line": i, "title": n[:80], "kind": kind,
                             "level": level, "num": parse_num(m.group(1))})
                break
    return hits


def strategy_b(lines):
    """
    Vertical CJK typeset one character per line (extraction without -layout).
    Collapse runs of >=4 single-char lines into a candidate title.

    Reconstruction is usually SCRAMBLED — the chapter number interleaves with
    the title characters, so 第5章 威鲸闯天关 may come back as 第威5章鲸闯天关.
    That is fine. This locates the boundary; it does not read the title.
    """
    hits, i, n = [], 0, len(lines)
    while i < n:
        if len(lines[i].strip()) == 1:
            j, chars = i, []
            while j < n and len(lines[j].strip()) <= 1:
                if lines[j].strip():
                    chars.append(lines[j].strip())
                j += 1
            if len(chars) >= 3:  # 第五章 alone is exactly 3 characters
                joined = depua("".join(chars))
                level = ("part" if re.search(r"部分", joined)
                         else "chapter" if re.search(r"[章回節节]", joined) else None)
                if level:
                    hits.append({"line": i, "title": joined[:80], "kind": "vertical-cjk",
                                 "level": level, "num": None, "scrambled": True})
            i = j
        else:
            i += 1
    return hits


def strategy_c(lines):
    """Page-break clustering. Noisy — last resort."""
    hits = []
    for i, line in enumerate(lines):
        if "\f" not in line:
            continue
        for k in range(i, min(i + 6, len(lines))):
            s = norm(lines[k].lstrip("\f"))
            if 2 <= len(s) <= 40 and not any(c in s for c in PROSE_MARKS):
                blanks = sum(1 for m in range(k + 1, min(k + 5, len(lines)))
                             if not lines[m].strip())
                if blanks >= 2:
                    hits.append({"line": k, "title": s[:80], "kind": "page-break",
                                 "level": "chapter", "num": None})
                break
    return hits


def dedupe(hits, window=3):
    """Collapse cross-strategy duplicates of the same physical heading.

    One heading can be detected twice — a @@CHAPTER@@ marker line and the
    raw title line just below it — always within a couple of lines and
    always with different kinds. Same-kind hits are kept even when close:
    consecutive short chapters are real, and audit() already flags
    boundaries that are suspiciously dense. Tracked per level so a PART
    heading never swallows the chapter right after it.
    """
    out, last = [], {}
    for h in sorted(hits, key=lambda x: x["line"]):
        lv = h.get("level")
        prev = last.get(lv)
        if prev and h["line"] - prev["line"] <= window and h["kind"] != prev["kind"]:
            continue
        out.append(h)
        last[lv] = h
    return out


def audit(hits, total_lines):
    """Return (confidence, notes[]). Err toward doubt."""
    notes = []
    chapters = [h for h in hits if h.get("level") == "chapter"]
    parts = [h for h in hits if h.get("level") == "part"]
    n = len(chapters)

    if n == 0 and parts:
        return "low", [f"found {len(parts)} part markers but no chapters — "
                       "chapter headings are typeset in a way these patterns miss"]
    if n < 3:
        return "none", ["too few boundaries to be a chapter list"]
    if n > 120:
        return "low", [f"{n} candidates — over-detecting"]

    # numbering should ascend without gaps
    nums = [h["num"] for h in chapters if h.get("num") is not None]
    if len(nums) >= 3:
        if nums != sorted(nums):
            notes.append("chapter numbers are out of order — likely false positives")
        if max(nums) > 500:  # a garbled capture would make range() explode
            notes.append(f"implausible chapter number {max(nums)} — "
                         "number parsing is suspect")
        else:
            missing = [k for k in range(1, max(nums) + 1) if k not in nums]
            if missing:
                notes.append(f"missing chapter numbers: {missing[:12]}"
                             f"{'…' if len(missing) > 12 else ''}")
            if max(nums) > n * 1.4:
                notes.append(f"highest number is {max(nums)} but only {n} found — "
                             "detection is incomplete")

    gaps = [chapters[i + 1]["line"] - chapters[i]["line"] for i in range(n - 1)]
    mean = sum(gaps) / len(gaps) if gaps else 0
    if mean and mean < 15:
        return "low", notes + ["boundaries too close to be chapters"]
    cv = ((sum((g - mean) ** 2 for g in gaps) / len(gaps)) ** 0.5 / mean) if mean else 99
    if cv > 1.2:
        notes.append(f"very uneven spacing (cv={cv:.1f})")

    coverage = (chapters[-1]["line"] - chapters[0]["line"]) / total_lines if total_lines else 0
    if coverage < 0.5:
        notes.append(f"boundaries span only {coverage:.0%} of the text — "
                     "later chapters are probably undetected")

    if notes:
        return "medium", notes
    return "high", [f"{n} chapters, evenly spaced, numbering consistent"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--context", type=int, default=0,
                    help="print N following lines, to read the real titles")
    a = ap.parse_args()

    lines = Path(a.path).read_text("utf-8", errors="ignore").split("\n")

    attempts = []
    for name, fn in [("A: explicit headings", strategy_a),
                     ("B: vertical CJK", strategy_b),
                     ("C: page breaks", strategy_c)]:
        hits = dedupe(fn(lines))
        conf, notes = audit(hits, len(lines))
        attempts.append({"name": name, "hits": hits, "conf": conf, "notes": notes})

    rank = {"high": 3, "medium": 2, "low": 1, "none": 0}
    # Strategy C is a last resort: it produces false positives on any book with
    # page-break decoration. Only consider it when A and B together fail.
    ab = [t for t in attempts if not t["name"].startswith("C")]
    ab_chapters = sum(1 for t in ab for h in t["hits"] if h.get("level") == "chapter")
    pool = ab if ab_chapters >= 5 else attempts
    best = max(pool, key=lambda t: (rank[t["conf"]], len(t["hits"])))

    # A and B can be complementary: A finds parts, B finds chapters
    merged = best["hits"]
    strategy_name = best["name"]
    other = [t for t in pool if t is not best and t["hits"]
             and not t["name"].startswith("C")]
    for o in other:
        b_levels = {h.get("level") for h in best["hits"]}
        o_levels = {h.get("level") for h in o["hits"]}
        if o_levels - b_levels:
            merged = dedupe(merged + o["hits"])
            strategy_name = f"{best['name']} + {o['name']}"

    conf, notes = audit(merged, len(lines))
    result = {
        "file": a.path, "total_lines": len(lines), "strategy": strategy_name,
        "confidence": conf, "notes": notes, "boundaries": merged,
        "counts": {t["name"]: len(t["hits"]) for t in attempts},
    }

    if a.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return

    print(f"\n{Path(a.path).name} — {len(lines):,} lines")
    print(f"Strategy: {strategy_name}")
    print(f"Confidence: {conf.upper()}")
    for nt in notes:
        print(f"  · {nt}")
    print(f"Counts by strategy: {result['counts']}")
    print("-" * 70)
    for h in merged:
        tag = "PART " if h.get("level") == "part" else "ch   "
        flag = "  [scrambled]" if h.get("scrambled") else ""
        print(f"  {tag} line {h['line']:>6}  {h['title']}{flag}")
        if a.context:
            shown = 0
            for k in range(h["line"] + 1, min(h["line"] + 40, len(lines))):
                if lines[k].strip():
                    print(f"                     | {norm(lines[k])[:64]}")
                    shown += 1
                    if shown >= a.context:
                        break
    print("-" * 70)

    if conf in ("none", "low"):
        print("\nDetection unreliable. Options:")
        print("  1. Rasterize the contents page and read it visually:")
        print("     pdftoppm -jpeg -r 150 -f 3 -l 5 book.pdf /tmp/toc")
        print("  2. Structure the notes by argument rather than by chapter")
        print("  3. Re-run with --context 4 to inspect candidates manually")
        print("  Do NOT invent a chapter list.")
    elif conf == "medium":
        print("\nPartially reliable — verify against the contents page before")
        print("citing chapter numbers in the notes.")
    else:
        print("\nRe-run with --context 4 to read the real titles.")
    print()


if __name__ == "__main__":
    main()
