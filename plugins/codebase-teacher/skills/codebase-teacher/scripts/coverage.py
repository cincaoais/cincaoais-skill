#!/usr/bin/env python3
"""
Snapshot a repository, inventory its files, and check a codebase-teacher
handbook against it. Stdlib only; never writes inside the repository.

Usage:
  coverage.py init <repo> <workdir> [--scope <subdir> ...] [--exclude 'GLOB=reason' ...]
  coverage.py check <workdir> <chapter.md | handbook.html ...> [--index coverage.md]

init writes three files into <workdir>:
  snapshot.json     commit, branch, last commit, uncommitted paths, scope, time
  inventory.json    first-party files (language, line count) and grouped files
                    (vendored, generated, lockfile, binary, ignored) with the
                    reason each group gets no line-level analysis
  fingerprint.json  size + mtime of every file outside .git, for the clean check
and prints a summary (languages, top directories, manifests, groups) to plan
the study from. Git runs with optional locks off so even .git/index is untouched.

check reads the Markdown chapters (coverage, refs) and every given file
(secrets), prints a report, writes <workdir>/check.json, and exits 1 on any
failure:
  coverage  every first-party file is explained: named by the first backticked
            token of a heading or `:::details` summary, or matched by a
            `<!-- covers: glob, glob -->` marker (fnmatch; `*` crosses "/")
  refs      every `path:N` / `path:N-M` reference names an existing file and lines
            inside it; every ```lang path:N-M excerpt equals those lines
  secrets   no credential-shaped string and no secret value from the repo's
            .env files (values are masked in the report)
  clean     the repository's files and HEAD are exactly as init recorded them
--index writes the "Complete file-coverage index" chapter. Pass chapters in
reading order so its links point at each file's first explanation.
"""
from __future__ import annotations

import argparse
import fnmatch
import glob
import json
import os
import re
import subprocess
import sys
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path

# keep the installed skill directory free of __pycache__
sys.dont_write_bytecode = True
from build_handbook import FENCE_RE, REF_RE, get_heading_path, is_path_like, slugify  # noqa: E402 - after the bytecode switch

GROUP_DIRS = {
    "node_modules": "vendored dependencies", "bower_components": "vendored dependencies",
    "vendor": "vendored dependencies", "third_party": "vendored dependencies",
    "third-party": "vendored dependencies", "Pods": "vendored dependencies", ".yarn": "package manager cache",
    "dist": "build output", ".next": "build output", ".nuxt": "build output", "__pycache__": "build output",
    ".venv": "virtual environment", "venv": "virtual environment", "coverage": "test coverage output",
    ".git": "version control metadata", ".hg": "version control metadata", ".svn": "version control metadata",
}
LOCKFILES = {"package-lock.json", "yarn.lock", "pnpm-lock.yaml", "bun.lockb", "poetry.lock", "uv.lock",
             "Pipfile.lock", "Cargo.lock", "Gemfile.lock", "composer.lock", "go.sum", "mix.lock",
             "packages.lock.json", "pubspec.lock", "flake.lock"}
GENERATED_NAMES = ("*.min.js", "*.min.css", "*.map", "*_pb2.py", "*_pb2_grpc.py", "*.pb.go",
                   "*.g.dart", "*.generated.*", "*.Designer.cs", "*.snap")
GENERATED_MARKER = re.compile(r"@generated|DO NOT EDIT|Code generated|auto-?generated|automatically generated", re.I)
ASSET_EXT = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico", ".svg", ".bmp", ".pdf", ".woff", ".woff2",
             ".ttf", ".otf", ".eot", ".mp3", ".mp4", ".wav", ".webm", ".mov", ".zip", ".gz", ".tgz", ".tar",
             ".jar", ".war", ".exe", ".dll", ".so", ".dylib", ".pyc", ".class", ".sqlite", ".sqlite3", ".db"}
LANGUAGES = {
    ".py": "Python", ".pyi": "Python", ".js": "JavaScript", ".mjs": "JavaScript", ".cjs": "JavaScript",
    ".jsx": "JavaScript", ".ts": "TypeScript", ".tsx": "TypeScript", ".vue": "Vue", ".svelte": "Svelte",
    ".go": "Go", ".rs": "Rust", ".rb": "Ruby", ".erb": "Ruby template", ".ex": "Elixir", ".exs": "Elixir",
    ".heex": "Elixir template", ".java": "Java", ".kt": "Kotlin", ".kts": "Kotlin", ".scala": "Scala",
    ".cs": "C#", ".fs": "F#", ".swift": "Swift", ".php": "PHP", ".dart": "Dart", ".c": "C", ".h": "C",
    ".cpp": "C++", ".hpp": "C++", ".html": "HTML", ".css": "CSS", ".scss": "CSS", ".sql": "SQL",
    ".sh": "Shell", ".md": "Markdown", ".rst": "reStructuredText", ".json": "JSON", ".yml": "YAML",
    ".yaml": "YAML", ".toml": "TOML", ".ini": "INI", ".cfg": "INI", ".xml": "XML", ".proto": "Protobuf",
    ".graphql": "GraphQL", ".tf": "Terraform", ".csproj": "MSBuild", ".gradle": "Gradle",
}
MANIFESTS = {"package.json", "pyproject.toml", "setup.py", "setup.cfg", "requirements.txt", "go.mod",
             "Cargo.toml", "pom.xml", "build.gradle", "build.gradle.kts", "Gemfile", "mix.exs",
             "composer.json", "pubspec.yaml", "manage.py", "Dockerfile", "docker-compose.yml",
             "docker-compose.yaml", "compose.yml", "compose.yaml", "Procfile", "Makefile", "justfile",
             "Justfile", "tsconfig.json", "vite.config.ts", "next.config.js", "angular.json",
             "serverless.yml", "app.yaml", "fly.toml", "render.yaml", "vercel.json", "netlify.toml"}
HIGH_CONFIDENCE = {
    "private key": r"-----BEGIN [A-Z ]*PRIVATE KEY-----",
    "AWS access key": r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b",
    "GitHub token": r"\b(?:gh[pousr]_[A-Za-z0-9]{36,}|github_pat_[A-Za-z0-9_]{22,})",
    "Slack token": r"\bxox[abposr]-[A-Za-z0-9-]{10,}",
    "API key (sk-)": r"\bsk-(?:ant-|proj-|live-)?[A-Za-z0-9_-]{20,}",
    "Google API key": r"\bAIza[0-9A-Za-z_-]{35}\b",
    "Stripe live key": r"\b[rsp]k_live_[0-9A-Za-z]{16,}",
    "JWT": r"\beyJ[\w-]{10,}\.eyJ[\w-]{10,}\.[\w-]{10,}",
    "URL with credentials": r"\b[a-z][a-z0-9+.-]*://[^/\s:@'\"<>]+:[^/\s@'\"<>]{3,}@",
}
ASSIGNMENT = re.compile(r"(?i)\b(password|passwd|secret|token|api[_-]?key|private[_-]?key|client[_-]?secret)"
                        r"\b\s*[:=]\s*['\"]?([^\s'\"<>`,;)]{8,})")
PLACEHOLDER = re.compile(r"(?i)^(\$\{|\$|<|%|\{\{|x{4,}|\*{3,}|\.{3}|changeme|example|placeholder|your[_-]|dummy|"
                         r"fake|test|sample|redacted|os\.|env\b|settings\.|process\.env|config\.)")
SECRET_KEY = re.compile(r"(?i)key|secret|token|pass|pwd|credential|private|auth|dsn|cookie|salt|signing")
ENV_EXAMPLE = (".example", ".sample", ".template", ".dist", ".defaults")


def run_git(repo: Path, *args: str) -> str:
    env = {**os.environ, "GIT_OPTIONAL_LOCKS": "0"}
    done = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, encoding="utf-8", errors="replace", env=env, check=False)
    return done.stdout if done.returncode == 0 else ""


def build_snapshot(repo: Path, scope: list[str]) -> dict:
    snapshot = {"repo_path": str(repo), "repo_name": repo.name, "scope": scope,
                "taken_at": datetime.now(UTC).strftime("%Y-%m-%d %H:%M UTC")}
    if run_git(repo, "rev-parse", "--is-inside-work-tree").strip() != "true":
        return {**snapshot, "commit": None, "dirty_paths": []}
    remote = run_git(repo, "remote", "get-url", "origin").strip()
    status = run_git(repo, "status", "--porcelain=v1", "--untracked-files=all").splitlines()
    return {**snapshot,
            "commit": run_git(repo, "rev-parse", "HEAD").strip(),
            "branch": run_git(repo, "rev-parse", "--abbrev-ref", "HEAD").strip(),
            "last_commit": run_git(repo, "log", "-1", "--format=%h %cs %s").strip(),
            "remote": re.sub(r"//[^/@]+@", "//", remote),
            "dirty_paths": [line[3:] for line in status]}


def list_fingerprint(repo: Path) -> dict[str, list[int]]:
    prints = {}
    for root, dirs, files in os.walk(repo):
        dirs[:] = [d for d in dirs if d != ".git"]
        for name in files:
            p = Path(root) / name
            st = p.lstat()
            prints[str(p.relative_to(repo))] = [st.st_size, st.st_mtime_ns]
    return prints


def list_repo_files(repo: Path) -> tuple[list[str], list[str]]:
    """Candidate files and ignored paths: from git when available, else a walk."""
    tracked = run_git(repo, "ls-files", "-z", "--cached", "--others", "--exclude-standard")
    if tracked:
        ignored = run_git(repo, "ls-files", "-z", "--others", "--ignored", "--exclude-standard", "--directory")
        files = [f for f in tracked.split("\0") if f and (repo / f).is_file()]
        return sorted(set(files)), sorted(f for f in ignored.split("\0") if f)
    files = []
    for root, dirs, names in os.walk(repo):
        dirs[:] = [d for d in dirs if d not in (".git", ".hg", ".svn")]
        files += [(Path(root) / n).relative_to(repo).as_posix() for n in names]
    return sorted(files), []


def resolve_group(rel: str, repo: Path, excludes: list[tuple[str, str]]) -> tuple[str, str] | None:
    """(pattern, reason) when a file gets no line-level analysis, else None."""
    for glob, reason in excludes:
        if fnmatch.fnmatchcase(rel, glob):
            return glob, reason
    parts = rel.split("/")
    for depth, part in enumerate(parts[:-1]):
        if part in GROUP_DIRS:
            return "/".join(parts[:depth + 1]) + "/**", GROUP_DIRS[part]
    name, ext = parts[-1], os.path.splitext(parts[-1])[1].lower()
    if name in LOCKFILES:
        return rel, "dependency lockfile (generated by the package manager)"
    if any(fnmatch.fnmatchcase(name, g) for g in GENERATED_NAMES):
        return rel, "generated file (by file name)"
    if ext in ASSET_EXT:
        return rel, "binary or media asset"
    try:
        head = (repo / rel).open("rb").read(8192)
    except OSError:
        return rel, "unreadable file"
    if b"\0" in head:
        return rel, "binary file"
    if GENERATED_MARKER.search(head[:2048].decode("utf-8", "replace")):
        return rel, "generated file (header marker)"
    return None


def get_language(rel: str) -> str:
    name = rel.rsplit("/", 1)[-1]
    if name in ("Dockerfile", "Makefile", "justfile", "Justfile", "Procfile"):
        return name
    return LANGUAGES.get(os.path.splitext(name)[1].lower(), "Other")


def build_inventory(repo: Path, scope: list[str], excludes: list[tuple[str, str]]) -> dict:
    candidates, ignored = list_repo_files(repo)
    files: dict[str, dict] = {}
    pattern_groups: Counter = Counter()
    listed_groups: dict[str, list[str]] = {}
    for rel in candidates:
        if scope and not any(rel == s or rel.startswith(s.rstrip("/") + "/") for s in scope):
            continue
        group = resolve_group(rel, repo, excludes)
        if group and group[0] == rel:
            listed_groups.setdefault(group[1], []).append(rel)
        elif group:
            pattern_groups[group] += 1
        else:
            data = (repo / rel).read_bytes()
            lines = data.count(b"\n") + (1 if data and not data.endswith(b"\n") else 0)
            files[rel] = {"language": get_language(rel), "lines": lines}
    grouped = [{"pattern": p, "reason": r, "files": n, "paths": []} for (p, r), n in pattern_groups.items()]
    grouped += [{"pattern": ", ".join(paths[:5]) + (f" …and {len(paths) - 5} more" if len(paths) > 5 else ""),
                 "reason": r, "files": len(paths), "paths": paths} for r, paths in listed_groups.items()]
    grouped += [{"pattern": p, "reason": "ignored by .gitignore (local, dependency, or build output)",
                 "files": None, "paths": []} for p in ignored]
    return {"files": files, "groups": grouped}


def print_summary(snapshot: dict, inventory: dict) -> None:
    files = inventory["files"]
    by_lang: Counter = Counter()
    by_dir: Counter = Counter()
    for rel, info in files.items():
        by_lang[info["language"]] += info["lines"]
        by_dir[rel.split("/")[0] if "/" in rel else "(root)"] += 1
    state = "clean" if not snapshot["dirty_paths"] else f"{len(snapshot['dirty_paths'])} uncommitted path(s)"
    print(f"snapshot  {snapshot.get('commit') or 'no git'} {snapshot.get('branch', '')} · {state}")
    print(f"files     {len(files)} first-party · {sum(i['lines'] for i in files.values()):,} lines · "
          f"{len(inventory['groups'])} grouped pattern(s)")
    print("languages " + ", ".join(f"{k} {v:,}" for k, v in by_lang.most_common(10)))
    print("top dirs  " + ", ".join(f"{k} ({v})" for k, v in by_dir.most_common(15)))
    print("manifests " + (", ".join(r for r in files if r.rsplit("/", 1)[-1] in MANIFESTS) or "none found"))
    for g in inventory["groups"][:20]:
        print(f"grouped   {g['pattern']} — {g['reason']}")


def cmd_init(a: argparse.Namespace) -> int:
    repo, work = Path(a.repo).resolve(), Path(a.workdir).resolve()
    if work == repo or repo in work.parents:
        sys.exit(f"workdir {work} is inside the repository; choose a scratch directory outside it")
    excludes = [tuple(e.split("=", 1)) if "=" in e else (e, "excluded by the study plan") for e in a.exclude]
    a.scope = [Path(s).as_posix() for s in a.scope]  # 'src\api' or './src/api' -> 'src/api'
    work.mkdir(parents=True, exist_ok=True)
    snapshot = build_snapshot(repo, a.scope)
    inventory = build_inventory(repo, a.scope, excludes)
    if a.scope and not inventory["files"]:
        sys.exit(f"scope {a.scope} matched no first-party files; use repo-relative paths")
    (work / "snapshot.json").write_text(json.dumps(snapshot, indent=1), encoding="utf-8")
    (work / "inventory.json").write_text(json.dumps(inventory, indent=1), encoding="utf-8")
    (work / "fingerprint.json").write_text(json.dumps(list_fingerprint(repo)), encoding="utf-8")
    print_summary(snapshot, inventory)
    return 0


def get_lines(repo: Path, rel: str, cache: dict[str, list[str] | None]) -> list[str] | None:
    if rel not in cache:
        p = repo / rel
        cache[rel] = p.read_text(encoding="utf-8", errors="replace").splitlines() if p.is_file() else None
    return cache[rel]


def compute_coverage(md_files: list[Path], repo: Path, files: dict) -> tuple[dict, list[str], list[str]]:
    """Map each explained first-party file to where it is explained; also refs failures and warnings."""
    explained: dict[str, dict] = {}
    failures: list[str] = []
    warnings: list[str] = []
    cache: dict[str, list[str] | None] = {}

    def validate_ref(token: str, where: str) -> None:
        ref = REF_RE.match(token)
        if not ref or not is_path_like(ref.group(1)):
            return
        path, start = ref.group(1), int(ref.group(2))
        end = int(ref.group(3) or start)
        lines = get_lines(repo, path, cache)
        if lines is None:
            failures.append(f"refs: {where}: `{token}` names a file that does not exist")
        elif not 1 <= start <= end <= len(lines):
            failures.append(f"refs: {where}: `{token}` is outside the file ({len(lines)} lines)")

    for md in md_files:
        chapter = section = ""
        lines = md.read_text(encoding="utf-8").splitlines()
        i = 0
        while i < len(lines):
            line, where = lines[i], f"{md.name}:{i + 1}"
            fence = FENCE_RE.match(line)
            if fence:
                body = []
                i += 1
                while i < len(lines) and not lines[i].startswith("```"):
                    body.append(lines[i])
                    i += 1
                ref = REF_RE.match((fence.group(2) or "").strip())
                if ref and fence.group(1) != "diagram":
                    validate_ref(fence.group(2).strip(), where)
                    source = get_lines(repo, ref.group(1), cache) or []
                    start = int(ref.group(2))
                    expected = source[start - 1:int(ref.group(3) or start)]
                    if source and [b.rstrip() for b in body] != [e.rstrip() for e in expected]:
                        drift = next((k for k, (b, e) in enumerate(zip(body, expected, strict=False)) if b.rstrip() != e.rstrip()),
                                     min(len(body), len(expected)))
                        failures.append(f"refs: {where}: excerpt {fence.group(2).strip()} differs from the file "
                                        f"at line {start + drift}")
                i += 1
                continue
            for token in re.findall(r"`([^`\s]+)`", line):
                validate_ref(token, where)
            location = " › ".join(x for x in (chapter, section) if x) or md.name
            heading = re.match(r"^(#{1,4})\s+(.*)$", line)
            target = None
            if heading:
                target = get_heading_path(heading.group(2))
                if not target and len(heading.group(1)) == 1:
                    chapter, section = heading.group(2).strip(), ""
                elif not target and len(heading.group(1)) == 2:
                    section = heading.group(2).strip()
            elif line.startswith(":::details"):
                target = get_heading_path(line[len(":::details"):])
            if target in files:
                explained.setdefault(target, {"where": location, "anchor": "f-" + slugify(target)})
            elif target and is_path_like(target) and not (repo / target.rstrip("/")).exists():
                failures.append(f"coverage: {where}: heading names `{target}`, which does not exist")
            for marker in re.findall(r"<!--\s*covers:\s*(.*?)-->", line):
                globs = [g for g in re.split(r"[,\s]+", marker) if g]
                for glob in globs:
                    hits = [f for f in files if fnmatch.fnmatchcase(f, glob)]
                    if not hits:
                        warnings.append(f"coverage: {where}: covers marker `{glob}` matches no first-party file")
                    for f in hits:
                        explained.setdefault(f, {"where": location + " (grouped)", "anchor": None})
            i += 1
    return explained, failures, warnings


def list_secret_findings(paths: list[Path], repo: Path) -> tuple[list[str], list[str]]:
    secret_values: set[str] = set()
    for root, dirs, names in os.walk(repo):
        dirs[:] = [d for d in dirs if d not in GROUP_DIRS]
        for name in names:
            if not (name == ".env" or name.startswith(".env.")) or name.endswith(ENV_EXAMPLE):
                continue
            for raw in (Path(root) / name).read_text(encoding="utf-8", errors="replace").splitlines():
                m = re.match(r"^\s*(?:export\s+)?([A-Za-z_][\w.]*)\s*=\s*(.*)$", raw)
                if m and SECRET_KEY.search(m.group(1)):
                    value = m.group(2).strip().strip("'\"")
                    if len(value) >= 8 and not PLACEHOLDER.match(value):
                        secret_values.add(value)
    failures, warnings = [], []
    for p in paths:
        text = p.read_text(encoding="utf-8", errors="replace")
        for label, pattern in HIGH_CONFIDENCE.items():
            for m in re.finditer(pattern, text):
                line = text.count("\n", 0, m.start()) + 1
                failures.append(f"secrets: {p.name}:{line}: {label} ({m.group(0)[:4]}…)")
        for value in secret_values:
            if value in text:
                line = text.count("\n", 0, text.index(value)) + 1
                failures.append(f"secrets: {p.name}:{line}: a value from the repository's .env files ({value[:3]}…)")
        for m in ASSIGNMENT.finditer(text):
            if not PLACEHOLDER.match(m.group(2)):
                line = text.count("\n", 0, m.start()) + 1
                warnings.append(f"secrets: {p.name}:{line}: review `{m.group(1)}` value ({m.group(2)[:3]}…)")
    return failures, warnings


def list_repo_changes(work: Path, repo: Path, snapshot: dict) -> list[str]:
    before = json.loads((work / "fingerprint.json").read_text(encoding="utf-8"))
    after = list_fingerprint(repo)
    changes = [f"clean: added {p}" for p in after.keys() - before.keys()]
    changes += [f"clean: removed {p}" for p in before.keys() - after.keys()]
    changes += [f"clean: modified {p}" for p in before.keys() & after.keys() if before[p] != after[p]]
    if snapshot.get("commit") and run_git(repo, "rev-parse", "HEAD").strip() != snapshot["commit"]:
        changes.append("clean: HEAD moved since the snapshot; line references may be stale")
    return sorted(changes)[:40]


def build_index(snapshot: dict, inventory: dict, explained: dict) -> str:
    files = inventory["files"]
    missing = sorted(set(files) - set(explained))
    out = ["# Complete file-coverage index", "",
           f"Snapshot `{(snapshot.get('commit') or 'no git')[:12]}` · {len(files)} first-party files · "
           f"{len(files) - len(missing)} explained · {len(missing)} not yet explained · "
           f"{len(inventory['groups'])} grouped pattern(s) without line-level analysis.", "",
           "Each first-party file links to the place it is first explained. Files marked *(grouped)* "
           "are explained together in that section.", ""]
    by_dir: dict[str, list[str]] = {}
    for rel in sorted(files):
        by_dir.setdefault(rel.split("/")[0] if "/" in rel else "(repository root)", []).append(rel)
    out += ["## First-party files", ""]
    for top, rels in by_dir.items():
        out += [f":::details {top} — {len(rels)} file(s)", "", "| File | Lines | Explained in |", "|---|---|---|"]
        for rel in rels:
            e = explained.get(rel)
            cell = "**not yet explained**" if not e else (
                f"[{e['where']}](#{e['anchor']})" if e["anchor"] else e["where"])
            out.append(f"| `{rel}` | {files[rel]['lines']} | {cell.replace('|', '/')} |")
        out += ["", ":::", ""]
    out += ["## Grouped without line-level analysis", "", "| Pattern | Files | Reason |", "|---|---|---|"]
    for g in inventory["groups"]:
        out.append(f"| `{g['pattern']}` | {g['files'] if g['files'] is not None else '—'} | {g['reason']} |")
    if missing:
        out += ["", "## Not yet explained", ""] + [f"- `{m}`" for m in missing]
    return "\n".join(out) + "\n"


def cmd_check(a: argparse.Namespace) -> int:
    work = Path(a.workdir).resolve()
    snapshot = json.loads((work / "snapshot.json").read_text(encoding="utf-8"))
    inventory = json.loads((work / "inventory.json").read_text(encoding="utf-8"))
    repo = Path(snapshot["repo_path"])
    # PowerShell passes globs like out/*.html through unexpanded
    paths = [Path(q) for p in a.files for q in (glob.glob(p) or [p])]
    md_files = [p for p in paths if p.suffix == ".md" and p.name != Path(a.index or "").name]
    explained, failures, warnings = compute_coverage(md_files, repo, inventory["files"])
    missing = sorted(set(inventory["files"]) - set(explained))
    failures += [f"coverage: not explained: {m}" for m in missing]
    secret_failures, secret_warnings = list_secret_findings(paths, repo)
    # secrets and repo changes first, so the 60-line print cap never hides them
    failures = secret_failures + list_repo_changes(work, repo, snapshot) + failures
    warnings += secret_warnings
    if a.index:
        Path(a.index).write_text(build_index(snapshot, inventory, explained), encoding="utf-8")
    total = len(inventory["files"])
    result = {"first_party": total, "explained": total - len(missing), "missing": missing,
              "failures": failures, "warnings": warnings, "complete": not failures}
    (work / "check.json").write_text(json.dumps(result, indent=1), encoding="utf-8")
    print(f"coverage  {total - len(missing)}/{total} first-party files explained")
    print(f"result    {'PASS' if not failures else f'FAIL ({len(failures)} failure(s))'}, {len(warnings)} warning(s)")
    for line in failures[:60] + [f"warning: {w}" for w in warnings[:30]]:
        print(line)
    return 0 if not failures else 1


def main() -> int:
    # Windows pipes default to the ANSI code page; CJK paths or arrows would raise UnicodeEncodeError.
    for stream in (sys.stdout, sys.stderr):
        stream.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="command", required=True)
    init = sub.add_parser("init", help="snapshot + inventory the repository")
    init.add_argument("repo")
    init.add_argument("workdir")
    init.add_argument("--scope", action="append", default=[], help="limit first-party files to this subdirectory")
    init.add_argument("--exclude", action="append", default=[], help="'GLOB=reason' to group instead of explain")
    check = sub.add_parser("check", help="check chapters against the snapshot")
    check.add_argument("workdir")
    check.add_argument("files", nargs="+")
    check.add_argument("--index", help="write the coverage-index chapter here")
    a = ap.parse_args()
    return cmd_init(a) if a.command == "init" else cmd_check(a)


if __name__ == "__main__":
    sys.exit(main())
