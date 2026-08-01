#!/usr/bin/env python3
"""
Extract text from ebooks. Single file, directory, or glob.

  python3 extract.py book.pdf --out ./notes
  python3 extract.py ./books/ --out ./notes
  python3 extract.py ./books/ --out ./notes --mode technical
  python3 extract.py --check

Writes per book:  <out>/<slug>/_source/full_text.txt
                  <out>/<slug>/_source/metadata.json

One bad file is logged and skipped; the batch continues.
"""

import argparse, glob, json, os, re, shutil, subprocess, sys, tempfile, unicodedata
from pathlib import Path

# Windows consoles and pipes often default to a legacy code page (cp1252,
# cp936); printing a CJK slug or warning would then crash the script.
for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        _stream.reconfigure(encoding="utf-8", errors="replace")

EXTS = {".pdf", ".epub", ".docx", ".txt", ".md", ".markdown",
        ".html", ".htm", ".rtf", ".mobi", ".azw", ".azw3", ".rst"}


# ---------- helpers ----------

def have_cmd(name):
    return shutil.which(name) is not None


def have_mod(name):
    try:
        __import__(name)
        return True
    except ImportError:
        return False


def slugify(text, fallback="book"):
    text = unicodedata.normalize("NFKC", text).strip()
    # keep CJK and word chars, collapse everything else to hyphens
    text = re.sub(r"[^\w\u4e00-\u9fff\u3040-\u30ff\uac00-\ud7af]+", "-", text)
    text = re.sub(r"-{2,}", "-", text).strip("-").lower()
    return text[:60] or fallback


# ---------- format parsers ----------

def from_pdf(path, mode="text"):
    if mode == "technical" and have_mod("docling"):
        try:
            from docling.document_converter import DocumentConverter
            return DocumentConverter().convert(str(path)).document.export_to_markdown(), "docling"
        except Exception as e:
            print(f"    docling failed ({e}); falling back", file=sys.stderr)

    if have_cmd("pdftotext"):
        # pdftotext emits UTF-8; without explicit encoding, Windows decodes
        # the pipe with the ANSI code page and mangles CJK/accented text
        r = subprocess.run(["pdftotext", "-layout", str(path), "-"],
                           capture_output=True, text=True,
                           encoding="utf-8", errors="replace")
        if r.returncode == 0 and r.stdout.strip():
            return r.stdout, "pdftotext"

    if have_mod("pypdf"):
        from pypdf import PdfReader
        pages = [p.extract_text() or "" for p in PdfReader(str(path)).pages]
        out = "\n".join(pages)
        if out.strip():
            return out, "pypdf"

    if have_mod("pdfminer"):
        from pdfminer.high_level import extract_text
        out = extract_text(str(path))
        if out.strip():
            return out, "pdfminer"

    raise RuntimeError("no PDF extractor produced text — "
                       "install poppler-utils or pypdf, or the PDF may be scanned")


def from_epub(path):
    if have_mod("ebooklib") and have_mod("bs4"):
        import ebooklib
        from ebooklib import epub
        from bs4 import BeautifulSoup
        book = epub.read_epub(str(path))
        parts = []
        for item in book.get_items():
            if item.get_type() == ebooklib.ITEM_DOCUMENT:
                # skip EPUB3 nav/TOC documents — their heading lists would
                # otherwise be ingested as fake chapters
                props = getattr(item, "properties", None) or []
                name = Path(item.get_name()).name.lower()
                if "nav" in props or name in ("nav.xhtml", "toc.xhtml", "toc.html"):
                    continue
                soup = BeautifulSoup(item.get_content(), "html.parser")
                # keep heading boundaries — they carry the chapter structure.
                # The title must ride on the SAME line as the marker:
                # get_text("\n") emits inserted strings as separate lines, so
                # a bare marker would never reach outline.py with its title.
                for h in soup.find_all(re.compile(r"^h[1-3]$")):
                    title = h.get_text(" ", strip=True)
                    h.insert_before(f"\n\n@@CHAPTER@@ {title}\n")
                parts.append(soup.get_text("\n"))
        return "\n\n".join(parts), "ebooklib"

    # stdlib fallback: loses chapter boundaries
    import zipfile
    from html.parser import HTMLParser

    class Strip(HTMLParser):
        def __init__(self):
            super().__init__()
            self.buf = []

        def handle_data(self, d):
            self.buf.append(d)

    parts = []
    with zipfile.ZipFile(path) as z:
        for name in sorted(z.namelist()):
            if name.lower().endswith((".xhtml", ".html", ".htm")):
                p = Strip()
                p.feed(z.read(name).decode("utf-8", "ignore"))
                parts.append("".join(p.buf))
    return "\n\n".join(parts), "zipfile(degraded)"


def from_docx(path):
    if have_mod("docx"):
        import docx
        d = docx.Document(str(path))
        lines = []
        for p in d.paragraphs:
            # style_id is locale-independent ("Heading1" even when the
            # display name is "Überschrift 1" or "Titre 1")
            name = p.style.name or ""
            sid = getattr(p.style, "style_id", "") or ""
            if name.startswith("Heading") or sid.startswith("Heading"):
                lines.append("\n@@CHAPTER@@ " + p.text)
            else:
                lines.append(p.text)
        return "\n".join(lines), "python-docx"

    import zipfile
    from xml.etree import ElementTree as ET
    with zipfile.ZipFile(path) as z:
        xml = z.read("word/document.xml").decode("utf-8", "ignore")
    ns = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
    root = ET.fromstring(xml)
    return "\n".join("".join(t.text or "" for t in p.iter(ns + "t"))
                     for p in root.iter(ns + "p")), "stdlib-xml"


def from_html(path):
    if have_mod("bs4"):
        from bs4 import BeautifulSoup
        # parse from bytes so bs4 sniffs the declared charset — a GBK/Big5
        # page force-decoded as UTF-8 is silent garbage
        soup = BeautifulSoup(Path(path).read_bytes(), "html.parser")
        for t in soup(["script", "style"]):
            t.decompose()
        return soup.get_text("\n"), "beautifulsoup4"
    raw = Path(path).read_text("utf-8", errors="ignore")
    return re.sub(r"<[^>]+>", " ", raw), "regex(degraded)"


def from_rtf(path):
    raw = Path(path).read_text("utf-8", errors="ignore")
    if have_mod("striprtf"):
        from striprtf.striprtf import rtf_to_text
        return rtf_to_text(raw), "striprtf"
    return re.sub(r"\\[a-z]+-?\d* ?|[{}]", "", raw), "regex(degraded)"


def from_mobi(path):
    if not have_cmd("ebook-convert"):
        raise RuntimeError("MOBI needs Calibre — install from calibre-ebook.com")
    tmp = Path(tempfile.gettempdir()) / (Path(path).stem + ".txt")
    subprocess.run(["ebook-convert", str(path), str(tmp)],
                   capture_output=True, check=True)
    text = tmp.read_text("utf-8", errors="ignore")
    tmp.unlink(missing_ok=True)
    return text, "calibre"


def extract_one(path, mode="text"):
    ext = Path(path).suffix.lower()
    if ext == ".pdf":
        return from_pdf(path, mode)
    if ext == ".epub":
        return from_epub(path)
    if ext == ".docx":
        return from_docx(path)
    if ext in (".html", ".htm"):
        return from_html(path)
    if ext == ".rtf":
        return from_rtf(path)
    if ext in (".mobi", ".azw", ".azw3"):
        return from_mobi(path)
    return Path(path).read_text("utf-8", errors="ignore"), "builtin"


# ---------- quality check ----------

def sanity(text):
    """Flag extractions that look broken. Silent garbage is the worst outcome."""
    warn = []
    if len(text.strip()) < 500:
        warn.append("almost no text — likely a scanned PDF; rasterize and read visually")
    pua = sum(1 for c in text[:60000] if "\ue000" <= c <= "\uf8ff")
    if pua > len(text[:60000]) * 0.01:
        warn.append("many private-use glyphs — font encoding is broken; rasterize instead")
    if re.search(r"\b(nd|rst|nal|rm)\b", text[:40000]) and text.count("fi") < 5:
        warn.append("possible ligature loss (fi/fl dropped) — exact word matching unreliable")
    return warn


def count_pdf_pages(path):
    if not have_cmd("pdfinfo"):
        return None
    r = subprocess.run(["pdfinfo", str(path)], capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    m = re.search(r"Pages:\s+(\d+)", r.stdout)
    return int(m.group(1)) if m else None


# ---------- driver ----------

def collect(target, exclude=None):
    p = Path(target)
    if p.is_file():
        files = [p]
    elif p.is_dir():
        files = sorted(f for f in p.rglob("*") if f.suffix.lower() in EXTS)
    else:
        files = sorted(Path(f) for f in glob.glob(target)
                       if Path(f).suffix.lower() in EXTS)
    if exclude:
        # never re-ingest our own previous output — a rerun with --out inside
        # the target would sweep up every full_text.txt as a "new book"
        ex = Path(exclude).resolve()
        files = [f for f in files if ex not in f.resolve().parents]
    return files


def check():
    rows = [
        ("PDF   pdftotext", have_cmd("pdftotext"), "apt install poppler-utils"),
        ("PDF   pypdf", have_mod("pypdf"), "pip install pypdf"),
        ("PDF   pdfminer.six", have_mod("pdfminer"), "pip install pdfminer.six"),
        ("PDF   docling", have_mod("docling"), "pip install docling"),
        ("EPUB  ebooklib", have_mod("ebooklib"), "pip install ebooklib"),
        ("HTML  beautifulsoup4", have_mod("bs4"), "pip install beautifulsoup4"),
        ("DOCX  python-docx", have_mod("docx"), "pip install python-docx"),
        ("RTF   striprtf", have_mod("striprtf"), "pip install striprtf"),
        ("MOBI  calibre", have_cmd("ebook-convert"), "calibre-ebook.com"),
    ]
    print("\nExtractor availability\n" + "-" * 52)
    for name, ok, how in rows:
        print(f"  {'OK ' if ok else '-- '} {name:<24} {'' if ok else how}")
    print("\nTXT / MD / RST need nothing.\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("target", nargs="?", help="file, directory, or glob")
    ap.add_argument("--out", default="./notes")
    ap.add_argument("--mode", choices=["text", "technical"], default="text",
                    help="technical uses docling for PDFs: keeps tables and code, ~1.5s/page")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()

    if a.check or not a.target:
        check()
        return

    files = collect(a.target, exclude=a.out)
    if not files:
        print(f"No supported files found in {a.target}", file=sys.stderr)
        sys.exit(1)

    out_root = Path(a.out)
    out_root.mkdir(parents=True, exist_ok=True)
    results = []
    used_slugs = set()

    print(f"\nFound {len(files)} file(s)\n" + "=" * 52)
    for i, f in enumerate(files, 1):
        print(f"[{i}/{len(files)}] {f.name}")
        try:
            text, tool = extract_one(f, a.mode)
        except Exception as e:
            print(f"    SKIPPED — {e}\n")
            results.append({"file": str(f), "status": "failed", "error": str(e)})
            continue

        slug = slugify(f.stem)
        if slug in used_slugs:  # same stem twice — don't silently overwrite
            base, k = slug, 2
            while f"{base}-{k}" in used_slugs:
                k += 1
            slug = f"{base}-{k}"
            print(f"    NOTE: slug taken — writing as {slug}")
        used_slugs.add(slug)
        src = out_root / slug / "_source"
        src.mkdir(parents=True, exist_ok=True)
        (src / "full_text.txt").write_text(text, encoding="utf-8")

        chars = len(text)
        # CJK runs ~3.5 chars/token, Latin ~4
        cjk = sum(1 for c in text[:20000] if "\u4e00" <= c <= "\u9fff")
        divisor = 3.5 if cjk > 2000 else 4.0

        meta = {
            "source_file": str(f),
            "slug": slug,
            "extractor": tool,
            "characters": chars,
            "est_tokens": int(chars / divisor),
            "pages": count_pdf_pages(f) if f.suffix.lower() == ".pdf" else None,
            "primarily_cjk": cjk > 2000,
            "warnings": sanity(text),
        }
        (src / "metadata.json").write_text(
            json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8")

        print(f"    {tool} · {chars:,} chars · ~{meta['est_tokens']:,} tokens"
              + (f" · {meta['pages']}pp" if meta["pages"] else ""))
        for w in meta["warnings"]:
            print(f"    WARNING: {w}")
        print(f"    -> {src}/full_text.txt\n")
        results.append({"file": str(f), "status": "ok", "slug": slug, **meta})

    ok = sum(1 for r in results if r["status"] == "ok")
    print("=" * 52)
    print(f"Extracted {ok}/{len(files)}")
    (out_root / "_extraction.json").write_text(
        json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")


if __name__ == "__main__":
    main()
