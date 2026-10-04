#!/usr/bin/env python3
"""Build index.html for a code-mentor learning folder.

Renders LESSON.md and QUIZ.md as tabs, with Mermaid diagrams drawn in the browser.
ANSWERS.md is left out so the quiz stays a test.

Usage: python3 build_viewer.py <learning-folder> [--title TITLE]
"""

import argparse
import html
import json
import sys
from pathlib import Path

TABS = (("Lesson", "LESSON.md"), ("Quiz", "QUIZ.md"))


def build_docs(folder: Path) -> list[dict[str, str]]:
    return [
        {"label": label, "markdown": (folder / name).read_text(encoding="utf-8")}
        for label, name in TABS
        if (folder / name).is_file()
    ]


def get_title(docs: list[dict[str, str]], folder: Path) -> str:
    for line in docs[0]["markdown"].splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return folder.resolve().name


def main() -> None:
    parser = argparse.ArgumentParser(description="Build index.html for a code-mentor learning folder.")
    parser.add_argument("folder", type=Path)
    parser.add_argument("--title", help="page title (default: first heading of LESSON.md)")
    args = parser.parse_args()

    docs = build_docs(args.folder)
    if not docs:
        sys.exit(f"No LESSON.md or QUIZ.md found in {args.folder}")
    title = args.title or get_title(docs, args.folder)
    template = (Path(__file__).resolve().parent.parent / "assets" / "viewer.html").read_text(encoding="utf-8")
    # < stops a "</script>" inside the Markdown from closing the data tag early
    payload = json.dumps(docs).replace("<", "\\u003c")
    page = template.replace("__TITLE__", html.escape(title)).replace("__DOCS_JSON__", payload)
    output = args.folder / "index.html"
    output.write_text(page, encoding="utf-8")
    print(output.resolve())


if __name__ == "__main__":
    main()
