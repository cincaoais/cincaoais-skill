#!/usr/bin/env python3
"""
Assemble codebase-teacher Markdown chapters into a self-contained, themed HTML
handbook (and optionally a PDF). Stdlib only.

Usage:
  build_handbook.py handbook.json -o out/ [--split] [--pdf] [--theme tokens.css] [--strict]

handbook.json (paths relative to the manifest):
  {"title": "Acme API Handbook",
   "eyebrow": "Snapdec · acme-api · Codebase handbook",
   "meta": "one line of context under the title, inline HTML allowed",
   "snapshot": "snapshot.json",
   "source_url": "https://github.com/o/r/blob/<sha>/{path}#L{line}-L{end}",
   "volumes": [{"title": "System overview", "summary": "why and when to read it",
                "parts": ["chapters/01-overview.md", "..."]}]}
  `snapshot` is the file `coverage.py init` writes; `source_url` is optional and
  turns file references into links ({path}, {line}, {end} are substituted).

Writes out/handbook.html: every volume in one file, the artifact to publish or
send. --split also writes out/index.html (the master index) plus
out/vol-<n>.html, with cross-volume links resolved. --pdf writes
out/handbook.pdf through headless Chrome/Chromium or weasyprint, details open.

Markdown subset:
  # chapter            h2, TOC entry.  ## section → h3, nested TOC entry.  ### / #### → h4 / h5.
                       Every heading gets id=<slug>: lowercase, runs of other characters → "-",
                       repeats suffixed -2, -3 in document order.
  ### `path` — note    a ###/#### heading whose first backticked token looks like a file path
                       renders as a file chip with id f-<slug(path)>, outside the TOC.
  ```lang path:40-55   source excerpt numbered from line 40, captioned with its reference;
                       coverage.py check verifies the body still equals those lines.
  ```diagram Caption   box-drawing / ASCII diagram in a captioned figure, never numbered.
  ```lang              other code; 4+ lines are numbered unless lang is shell or output.
  :::details summary   collapsible block, closed on screen and open in the PDF; nests;
  :::                  a summary starting with a backticked path gets id f-<slug(path)>.
  [Confirmed] [Inferred] [Unknown]   evidence badges.
  `path:12`  `path:12-30`            file references; links when source_url is set.
  <!-- covers: glob -->              coverage marker read by coverage.py; stripped here.
  - / 1. lists (one level), - [ ] checklists, pipe tables, > callouts, **bold**, *em*,
  `code`, [text](https://…), [text](#anchor), [text](page.html) inline.

Theme: tokens.css, resolved from --theme, then ../../../theme/tokens.css (the
plugin layout), then $CLAUDE_PLUGIN_ROOT/theme.
"""
from __future__ import annotations

import argparse
import html
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from urllib.parse import quote

PATH_EXT = (".cs", ".csproj", ".sln", ".slnx", ".props", ".fs",
            ".py", ".pyi", ".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs", ".vue", ".svelte",
            ".go", ".mod", ".sum", ".rs", ".rb", ".ex", ".exs", ".eex", ".heex", ".erb",
            ".kt", ".kts", ".java", ".gradle", ".swift", ".php", ".dart", ".scala", ".c", ".h",
            ".cpp", ".hpp", ".json", ".xml", ".toml", ".yml", ".yaml", ".ini", ".cfg", ".conf",
            ".env", ".lock", ".md", ".rst", ".txt", ".html", ".css", ".scss", ".sql", ".proto",
            ".graphql", ".sh", ".tf", ".hcl")
PATH_NAMES = {"Dockerfile", "Makefile", "justfile", "Justfile", "Procfile", "Gemfile",
              "Rakefile", "Jenkinsfile", "Vagrantfile", "LICENSE", "Caddyfile"}
NO_NUMBER = {"", "bash", "sh", "zsh", "console", "text", "output", "shell", "powershell", "ps1"}
FENCE_RE = re.compile(r"^```(\w*)(?:\s+(.+?))?\s*$")
REF_RE = re.compile(r"^([^\s`:]+):(\d+)(?:[-–](\d+))?$")
HEADING_PATH_RE = re.compile(r"\s*`([^`\s]+)`")
EVIDENCE_RE = re.compile(r"\[(Confirmed|Inferred|Unknown)\]")
LINK_RE = re.compile(r"\[([^\]]+)\]\(((?:https?://|#|[\w.-]+\.html)[^)\s]*)\)")
FAVICON = "📚"


def is_path_like(text: str) -> bool:
    t = text.strip().strip("`")
    name = t.rsplit("/", 1)[-1]
    return "/" in t or t.endswith(PATH_EXT) or name in PATH_NAMES or (name.startswith(".") and len(name) > 1)


def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", re.sub(r"<.*?>", "", text).lower()).strip("-") or "section"


def get_heading_path(text: str) -> str | None:
    """The repo-relative file a heading or details summary is about, if any."""
    m = HEADING_PATH_RE.match(text)
    if not m:
        return None
    token = m.group(1)
    ref = REF_RE.match(token)
    return ref.group(1) if ref else token


class Renderer:
    """One pass over the handbook; collects anchors and TOC entries as it goes."""

    def __init__(self, source_url: str, is_print: bool) -> None:
        self.source_url = source_url
        self.is_print = is_print
        self.ids: dict[str, int] = {}
        self.toc: list[tuple[int, int, str, str]] = []
        self.volume = 0

    def build_id(self, base: str) -> str:
        anchor, n = base, 2
        while anchor in self.ids:
            anchor, n = f"{base}-{n}", n + 1
        self.ids[anchor] = self.volume
        return anchor

    def build_code(self, token: str) -> str:
        ref = REF_RE.match(token)
        if not (ref and is_path_like(ref.group(1))):
            return f"<code>{html.escape(token)}</code>"
        code = f'<code class="ref">{html.escape(token)}</code>'
        if not self.source_url:
            return code
        path, line = ref.group(1), ref.group(2)
        href = (self.source_url.replace("{path}", quote(path))
                .replace("{line}", line).replace("{end}", ref.group(3) or line))
        return f'<a class="ref" href="{html.escape(href)}">{code}</a>'

    def inline(self, s: str) -> str:
        out = []
        for p in re.split(r"(`[^`]*`)", s):
            if len(p) >= 2 and p.startswith("`") and p.endswith("`"):
                out.append(self.build_code(p[1:-1]))
            else:
                out.append(html.escape(p, quote=False))
        t = "".join(out)
        t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
        t = re.sub(r"(?<![\w*>])\*(?!\s)([^*<]+?)(?<!\s)\*(?![\w*])", r"<em>\1</em>", t)
        t = LINK_RE.sub(lambda m: f'<a href="{m.group(2)}">{m.group(1)}</a>', t)
        return EVIDENCE_RE.sub(lambda m: f'<span class="ev ev-{m.group(1).lower()}">{m.group(1)}</span>', t)

    def build_heading(self, level: int, text: str) -> str:
        tag = f"h{level + 1}"
        path = get_heading_path(text)
        if level >= 3 and path and is_path_like(path):
            anchor = self.build_id("f-" + slugify(path))
            return f'<{tag} id="{anchor}" class="file">{self.inline(text)}</{tag}>'
        anchor = self.build_id(slugify(text))
        if level <= 2:
            self.toc.append((self.volume, level, anchor, re.sub(r"<.*?>", "", self.inline(text))))
        return f'<{tag} id="{anchor}">{self.inline(text)}</{tag}>'

    def build_fence(self, lang: str, info: str, code: list[str]) -> str:
        if lang == "diagram":
            caption = f"<figcaption>{self.inline(info)}</figcaption>" if info else ""
            body = "\n".join(html.escape(c) for c in code)
            return f'<figure class="diagram"><pre><code>{body}</code></pre>{caption}</figure>'
        ref = REF_RE.match(info) if info else None
        numbered = ref is not None or (lang not in NO_NUMBER and len(code) >= 4)
        if numbered:
            body = "".join(f'<span class="l">{html.escape(c)}</span>' for c in code)
        else:
            body = "\n".join(html.escape(c) for c in code)
        start = int(ref.group(2)) if ref else 1
        style = f' style="counter-reset:ln {start - 1}"' if start > 1 else ""
        pre = (f'<pre class="lang-{lang or "text"}{" numbered" if numbered else ""}">'
               f"<code{style}>{body}</code></pre>")
        if ref:
            return f'<div class="excerpt"><div class="kicker">{self.build_code(info)}</div>{pre}</div>'
        return pre

    def build_details(self, summary: str, inner: list[str]) -> str:
        path = get_heading_path(summary)
        attrs = f' id="{self.build_id("f-" + slugify(path))}" class="file"' if path and is_path_like(path) else ""
        is_open = " open" if self.is_print else ""
        return (f"<details{attrs}{is_open}><summary>{self.inline(summary)}</summary>"
                f"{self.convert(inner)}</details>")

    def build_list(self, items: list[str], ordered: bool) -> str:
        if all(re.match(r"^\[[ xX]\]\s", it) for it in items):
            checks = [re.sub(r"^\[[ xX]\]\s", "", it) for it in items]
            return '<ul class="check">' + "".join(f"<li>{self.inline(c)}</li>" for c in checks) + "</ul>"
        tag = "ol" if ordered else "ul"
        return f"<{tag}>" + "".join(f"<li>{self.inline(it)}</li>" for it in items) + f"</{tag}>"

    def convert(self, lines: list[str]) -> str:
        out: list[str] = []
        para: list[str] = []
        i, n = 0, len(lines)

        def flush() -> None:
            if para:
                out.append("<p>" + self.inline(" ".join(x.strip() for x in para)) + "</p>")
                para.clear()

        while i < n:
            line = lines[i]
            m = FENCE_RE.match(line)
            if m:
                flush()
                i += 1
                code: list[str] = []
                while i < n and not lines[i].startswith("```"):
                    code.append(lines[i])
                    i += 1
                i += 1
                out.append(self.build_fence(m.group(1).lower(), (m.group(2) or "").strip(), code))
                continue
            if line.startswith(":::details"):
                flush()
                depth, inner = 1, []
                i += 1
                while i < n:
                    if lines[i].startswith(":::details"):
                        depth += 1
                    elif lines[i].strip() == ":::":
                        depth -= 1
                        if depth == 0:
                            break
                    inner.append(lines[i])
                    i += 1
                i += 1
                out.append(self.build_details(line[len(":::details"):].strip(), inner))
                continue
            m = re.match(r"^(#{1,4})\s+(.*)$", line)
            if m:
                flush()
                out.append(self.build_heading(len(m.group(1)), m.group(2).strip()))
                i += 1
                continue
            if line.strip().startswith("|") and i + 1 < n and re.match(r"^\s*\|?\s*:?-{2,}", lines[i + 1]):
                flush()
                header = [c.strip() for c in line.strip().strip("|").split("|")]
                i += 2
                rows = []
                while i < n and lines[i].strip().startswith("|"):
                    rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                    i += 1
                t = ['<div class="tblwrap"><table><tr>' + "".join(f"<th>{self.inline(h)}</th>" for h in header) + "</tr>"]
                t += ["<tr>" + "".join(f"<td>{self.inline(c)}</td>" for c in r) + "</tr>" for r in rows]
                out.append("".join(t) + "</table></div>")
                continue
            if line.startswith("> "):
                flush()
                q = []
                while i < n and lines[i].startswith("> "):
                    q.append(lines[i][2:])
                    i += 1
                out.append('<div class="note">' + self.inline(" ".join(q)) + "</div>")
                continue
            m = re.match(r"^(\s*)([-*]|\d+\.)\s+(.*)$", line)
            if m:
                flush()
                ordered = m.group(2)[0].isdigit()
                items: list[str] = []
                while i < n:
                    mm = re.match(r"^(\s*)([-*]|\d+\.)\s+(.*)$", lines[i])
                    if not (mm and mm.group(2)[0].isdigit() == ordered):
                        break
                    items.append(mm.group(3))
                    i += 1
                    while i < n and lines[i].strip() and re.match(r"^\s{2,}", lines[i]) \
                            and not re.match(r"^\s*([-*]|\d+\.)\s+", lines[i]):
                        items[-1] += " " + lines[i].strip()
                        i += 1
                out.append(self.build_list(items, ordered))
                continue
            if not line.strip():
                flush()
                i += 1
                continue
            para.append(line)
            i += 1
        flush()
        return "\n".join(out)

    def render_volumes(self, volumes: list[dict], texts: list[list[str]]) -> list[str]:
        bodies = []
        for v, (vol, parts) in enumerate(zip(volumes, texts, strict=True)):
            self.volume = v
            md = re.sub(r"<!--.*?-->", "", "\n\n".join(parts), flags=re.S)
            banner = ""
            if len(volumes) > 1:
                anchor = self.build_id(f"vol-{v + 1}")
                banner = (f'<div class="volbanner" id="{anchor}"><div class="kicker">Volume {v + 1}</div>'
                          f'<div class="voltitle">{html.escape(vol["title"])}</div></div>')
            bodies.append(banner + self.convert(md.splitlines()))
        return bodies


def resolve_theme(override: str | None) -> Path:
    candidates = [Path(override)] if override else []
    candidates.append(Path(__file__).resolve().parents[3] / "theme" / "tokens.css")
    if os.environ.get("CLAUDE_PLUGIN_ROOT"):
        candidates.append(Path(os.environ["CLAUDE_PLUGIN_ROOT"]) / "theme" / "tokens.css")
    for c in candidates:
        if c.is_file():
            return c
    sys.exit("missing theme tokens.css (codebase-teacher plugin theme/); pass --theme <path>")


# Page-specific CSS only; tokens, fonts, base type, tables, .note, .card,
# .eyebrow, .kicker and .meta come from theme/tokens.css.
PAGE_CSS = """
.wrap{max-width:920px;margin:0 auto;padding:36px 24px 96px}
h2{margin:56px 0 10px;padding-top:20px;border-top:1px solid var(--rule)}
h3{margin:30px 0 6px}
h4,h5{margin:22px 0 6px}
h4.file,h5.file{font-family:"IBM Plex Mono",monospace;font-size:13px;font-weight:500;letter-spacing:0;color:var(--accent-ink);background:var(--tint);border-radius:6px;padding:6px 10px;display:inline-block;margin:36px 0 8px;text-wrap:initial}
h4.file code,h5.file code,details.file>summary code:first-of-type{background:none;border:none;padding:0;color:var(--accent-ink)}
p{max-width:72ch}
ul,ol{max-width:76ch}
[hidden]{display:none!important}
pre.numbered code{counter-reset:ln}
pre.numbered code .l{counter-increment:ln;display:block}
pre.numbered code .l::before{content:counter(ln);display:inline-block;width:2.8em;margin-right:1em;text-align:right;color:var(--mute);user-select:none}
.excerpt .kicker{margin:16px 0 -6px}
.excerpt .kicker code{text-transform:none;letter-spacing:0}
code.ref{color:var(--accent-ink)}
a.ref{text-decoration:none}
figure.diagram{margin:18px 0}
figure.diagram pre{background:var(--surface)}
figure.diagram pre code{line-height:1.2}
figcaption{font-size:13px;color:var(--ink2);margin-top:-4px}
.ev{font-family:"IBM Plex Mono",monospace;font-size:10.5px;font-weight:500;letter-spacing:.06em;text-transform:uppercase;border-radius:4px;padding:1px 6px;white-space:nowrap;vertical-align:1px}
.ev-confirmed{background:var(--tint);color:var(--accent-ink)}
.ev-inferred{background:var(--warm);color:var(--warm-ink)}
.ev-unknown{border:1px solid var(--rule);color:var(--mute)}
details{border:1px solid var(--rule);border-radius:8px;background:var(--surface);margin:10px 0;padding:0 14px}
details>summary{cursor:pointer;padding:9px 0;font-weight:500}
details[open]>summary{border-bottom:1px solid var(--rule);margin-bottom:8px}
details details{background:var(--bg)}
.snap,.toc,.reading{margin:22px 0}
.snap table{font-size:13px}
.toc>strong,.reading>strong{font-family:"IBM Plex Mono",monospace;font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:var(--mute)}
.tocbar{display:flex;gap:10px;align-items:center;margin:10px 0 4px}
.tocbar input{flex:1;font:inherit;font-size:14px;color:var(--ink);background:var(--bg);border:1px solid var(--rule);border-radius:6px;padding:6px 10px}
.tocbar button{font:500 11px "IBM Plex Mono",monospace;letter-spacing:.06em;text-transform:uppercase;color:var(--accent-ink);background:var(--tint);border:none;border-radius:6px;padding:7px 10px;cursor:pointer}
.toc ol{margin:8px 0 0;padding-left:22px}
.toc li{margin:4px 0;color:var(--ink2)}
.toc .sub{font-size:13px;color:var(--mute)}
.toc .sub a{color:var(--ink2)}
.toc .volgroup{margin-top:14px;font-family:"IBM Plex Mono",monospace;font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:var(--mute)}
.reading li{margin:8px 0}
.volbanner{margin:80px 0 0;padding:22px 0 0;border-top:3px solid var(--accent)}
.voltitle{font-family:Manrope,"IBM Plex Sans",sans-serif;font-size:30px;font-weight:700;letter-spacing:-.02em}
.volnav{font-family:"IBM Plex Mono",monospace;font-size:12px;display:flex;gap:16px;margin:18px 0}
.check{list-style:none;padding-left:4px}
.check li{padding-left:28px;position:relative}
.check li::before{content:"\\2610";position:absolute;left:0;color:var(--accent-ink)}
.note{max-width:none}
@media print{.tocbar{display:none}pre,pre code{white-space:pre-wrap;word-break:break-word}.volbanner{break-before:page}h2{break-after:avoid}details{break-inside:auto}}
"""

SCRIPT = """<script>
document.querySelectorAll('.toc input').forEach(function (box) {
  box.addEventListener('input', function () {
    var q = box.value.toLowerCase();
    box.closest('.toc').querySelectorAll('li').forEach(function (li) {
      li.hidden = q !== '' && li.textContent.toLowerCase().indexOf(q) < 0;
    });
  });
});
document.querySelectorAll('.toc button').forEach(function (btn) {
  btn.addEventListener('click', function () {
    var open = btn.dataset.open !== '1';
    document.querySelectorAll('details').forEach(function (d) { d.open = open; });
    btn.dataset.open = open ? '1' : '0';
    btn.textContent = open ? 'Collapse all' : 'Expand all';
  });
});
window.addEventListener('beforeprint', function () {
  document.querySelectorAll('details').forEach(function (d) { d.open = true; });
});
</script>"""

FONTS = ('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Manrope:wght@500;600;700'
         '&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap">')


def build_snapshot_card(snapshot: dict) -> str:
    if not snapshot:
        return ""
    state = "clean" if not snapshot.get("dirty_paths") else f'{len(snapshot["dirty_paths"])} uncommitted change(s)'
    rows = [("Repository", snapshot.get("repo_name", "")),
            ("Commit", (snapshot.get("commit") or "not a git repository")[:12]),
            ("Branch", snapshot.get("branch", "")),
            ("Working tree", state),
            ("Last commit", snapshot.get("last_commit", "")),
            ("Scope", ", ".join(snapshot.get("scope") or []) or "whole repository"),
            ("Studied", snapshot.get("taken_at", ""))]
    body = "".join(f"<tr><td>{html.escape(k)}</td><td>{html.escape(str(v))}</td></tr>" for k, v in rows if v)
    return f'<div class="card snap"><strong class="kicker">Repository snapshot</strong><div class="tblwrap"><table>{body}</table></div></div>'


def build_reading_order(volumes: list[dict], href_for) -> str:
    items = "".join(
        f'<li><a href="{href_for(v)}"><strong>Volume {v + 1}</strong> · {html.escape(vol["title"])}</a>'
        + (f" — {html.escape(vol['summary'])}" if vol.get("summary") else "") + "</li>"
        for v, vol in enumerate(volumes))
    return f'<div class="card reading"><strong>Reading order</strong><ol>{items}</ol></div>'


def build_toc(renderer: Renderer, volumes: list[dict], only: int | None) -> str:
    groups: dict[int, list[str]] = {}
    for vol, level, anchor, text in renderer.toc:
        if only is not None and vol != only:
            continue
        rows = groups.setdefault(vol, [])
        if level == 1:
            rows.append(f'<li><a href="#{anchor}">{text}</a><div class="sub">')
            rows.append("</div></li>")
        elif rows:
            rows.insert(len(rows) - 1, f'<a href="#{anchor}">{text}</a>')
    if not groups:
        return ""
    blocks = []
    for vol, rows in groups.items():
        label = (f'<div class="volgroup">Volume {vol + 1} · {html.escape(volumes[vol]["title"])}</div>'
                 if len(volumes) > 1 and only is None else "")
        items = re.sub(r'</a>(?=<a href)', "</a> · ", "".join(rows)).replace('<div class="sub"></div>', "")
        blocks.append(f"{label}<ol>{items}</ol>")
    return ('<div class="card toc"><strong>Contents</strong><div class="tocbar">'
            '<input type="search" placeholder="Filter chapters and sections" aria-label="Filter contents">'
            f'<button type="button">Expand all</button></div>{"".join(blocks)}</div>')


def build_page(manifest: dict, title: str, blocks: list[str]) -> str:
    icon = f"data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>{FAVICON}</text></svg>"
    meta = f'<p class="meta">{manifest["meta"]}</p>\n' if manifest.get("meta") else ""
    return ("<!doctype html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n"
            '<meta name="viewport" content="width=device-width,initial-scale=1">\n'
            f"<title>{html.escape(title)}</title>\n<link rel=\"icon\" href=\"{icon}\">\n{FONTS}\n"
            f"<style>{manifest['_css']}</style>\n</head>\n<body>\n<div class=\"wrap\">\n"
            f'<div class="eyebrow">{html.escape(manifest.get("eyebrow", ""))}</div>\n'
            f"<h1>{html.escape(title)}</h1>\n{meta}<div class=\"rule\"></div>\n"
            + "\n".join(b for b in blocks if b) + f"\n</div>\n{SCRIPT}\n</body>\n</html>\n")


def resolve_split_links(page: str, ids: dict[str, int], here: int) -> str:
    def swap(m: re.Match) -> str:
        owner = ids.get(m.group(1))
        return f'href="vol-{owner + 1}.html#{m.group(1)}"' if owner is not None and owner != here else m.group(0)
    return re.sub(r'href="#([^"]+)"', swap, page)


def list_warnings(page: str, renderer: Renderer) -> list[str]:
    text = re.sub(r"<pre.*?</pre>", "", page, flags=re.S)
    text = re.sub(r"<(script|style)>.*?</\1>", "", text, flags=re.S)
    warnings = []
    leaks = text.count("```") + text.count(":::") + len(re.findall(r"\*\*[^*]+\*\*", text)) + text.count("](")
    if leaks:
        warnings.append(f"{leaks} possible leaked Markdown token(s) (```, :::, **, ](…))")
    broken = sorted({a for a in re.findall(r'href="#([^"]+)"', page) if a not in renderer.ids})
    if broken:
        warnings.append("broken anchor link(s): " + ", ".join("#" + b for b in broken[:12]))
    chapters = [t for _, level, _, t in renderer.toc if level == 1]
    repeated = sorted({t for t in chapters if chapters.count(t) > 1})
    if repeated:
        warnings.append("duplicated chapter heading(s): " + "; ".join(repeated))
    return warnings


def build_pdf(manifest: dict, volumes: list[dict], texts: list[list[str]], out: Path) -> str:
    renderer = Renderer(manifest.get("source_url", ""), is_print=True)
    bodies = renderer.render_volumes(volumes, texts)
    page = build_page(manifest, manifest["title"], [manifest["_snap"], build_toc(renderer, volumes, None), *bodies])
    chromes = [shutil.which(c) for c in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser", "msedge")]
    chromes += ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
                "/Applications/Chromium.app/Contents/MacOS/Chromium",
                r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"]
    pdf = out / "handbook.pdf"
    with tempfile.TemporaryDirectory() as tmp:
        src = Path(tmp) / "print.html"
        src.write_text(page, encoding="utf-8")
        for exe in [c for c in chromes if c and Path(c).exists()]:
            cmd = [exe, "--headless=new", "--disable-gpu", "--no-pdf-header-footer", f"--user-data-dir={tmp}/profile",
                   f"--print-to-pdf={pdf}", src.as_uri()]
            if subprocess.run(cmd, capture_output=True, timeout=300, check=False).returncode == 0 and pdf.exists():
                return f"wrote {pdf} (Chrome)"
        if shutil.which("weasyprint"):
            if subprocess.run(["weasyprint", str(src), str(pdf)], capture_output=True, timeout=300, check=False).returncode == 0:
                return f"wrote {pdf} (weasyprint)"
    return "PDF skipped: no headless Chrome/Chromium or weasyprint found"


def main() -> int:
    # Windows pipes default to the ANSI code page; CJK paths or arrows would raise UnicodeEncodeError.
    for stream in (sys.stdout, sys.stderr):
        stream.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("manifest")
    ap.add_argument("-o", "--out", required=True, help="output directory")
    ap.add_argument("--split", action="store_true", help="also write index.html + vol-<n>.html")
    ap.add_argument("--pdf", action="store_true", help="also write handbook.pdf when a converter exists")
    ap.add_argument("--theme", help="path to the theme tokens.css")
    ap.add_argument("--strict", action="store_true", help="exit 1 when any warning is reported")
    a = ap.parse_args()

    base = Path(a.manifest).resolve().parent
    manifest = json.loads(Path(a.manifest).read_text(encoding="utf-8"))
    volumes = manifest["volumes"]
    texts = [[(base / p).read_text(encoding="utf-8") for p in vol["parts"]] for vol in volumes]
    snapshot = json.loads((base / manifest["snapshot"]).read_text(encoding="utf-8")) if manifest.get("snapshot") else {}
    manifest["_css"] = resolve_theme(a.theme).read_text(encoding="utf-8") + PAGE_CSS
    manifest["_snap"] = build_snapshot_card(snapshot)
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)

    renderer = Renderer(manifest.get("source_url", ""), is_print=False)
    bodies = renderer.render_volumes(volumes, texts)
    multi = len(volumes) > 1
    reading = build_reading_order(volumes, lambda v: f"#vol-{v + 1}") if multi else ""
    combined = build_page(manifest, manifest["title"],
                          [manifest["_snap"], reading, build_toc(renderer, volumes, None), *bodies])
    (out / "handbook.html").write_text(combined, encoding="utf-8")
    warnings = list_warnings(combined, renderer)
    report = [f"wrote {out / 'handbook.html'} ({len(combined.encode()):,} bytes, {len(volumes)} volume(s), "
              f"{sum(1 for t in renderer.toc if t[1] == 1)} chapters, {len(renderer.toc)} TOC entries)"]

    if a.split and multi:
        index = build_page(manifest, manifest["title"],
                           [manifest["_snap"], build_reading_order(volumes, lambda v: f"vol-{v + 1}.html"),
                            build_toc(renderer, volumes, None)])
        (out / "index.html").write_text(resolve_split_links(index, renderer.ids, -1), encoding="utf-8")
        for v, body in enumerate(bodies):
            links = ['<a href="index.html">Index</a>']
            if v > 0:
                links.append(f'<a href="vol-{v}.html">‹ Volume {v}</a>')
            if v + 1 < len(volumes):
                links.append(f'<a href="vol-{v + 2}.html">Volume {v + 2} ›</a>')
            nav = f'<nav class="volnav">{"".join(links)}</nav>'
            page = build_page(manifest, f'{manifest["title"]} · Volume {v + 1}',
                              [nav, build_toc(renderer, volumes, v), body, nav])
            (out / f"vol-{v + 1}.html").write_text(resolve_split_links(page, renderer.ids, v), encoding="utf-8")
        report.append(f"wrote {out / 'index.html'} + {len(volumes)} volume page(s)")
    if a.pdf:
        report.append(build_pdf(manifest, volumes, texts, out))

    print("\n".join(report + [f"WARNING: {w}" for w in warnings]))
    return 1 if a.strict and warnings else 0


if __name__ == "__main__":
    sys.exit(main())
