#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["cloakbrowser>=0.6.5"]
# ///
"""Fetch bot-walled pages with CloakBrowser and report whether they were blocked.

Read-only helper for the rnd skill. It loads pages, waits, optionally scrolls to
trigger lazy content, and classifies what came back. It never clicks, types,
submits forms, signs in, or handles credentials.

Requires Python >= 3.10 and the ``cloakbrowser`` package (which bundles
Playwright and its own stealth Chromium build). The PEP 723 header above lets
``uv`` install both on demand, so this is the easy path from any directory:

Examples:
    uv run stealth_fetch.py --check
    uv run stealth_fetch.py --url https://example.com --format json
    uv run stealth_fetch.py --url https://x.com/AnthropicAI --headed --wait-ms 4000
    uv run stealth_fetch.py --profile --url https://old.reddit.com/r/algotrading/top/
    uv run stealth_fetch.py --login https://x.com

If cloakbrowser is already installed in your Python, the plain interpreter also
works:

    python stealth_fetch.py --check
    python stealth_fetch.py --url https://example.com --format json
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import random
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlsplit

EXIT_OK = 0
EXIT_NOT_READY = 3
EXIT_ALL_BLOCKED = 4
EXIT_ERROR = 1

DEFAULT_PROFILE_DIR = Path.home() / ".cloakbrowser-profiles" / "research"
DEFAULT_WAIT_MS = 3000
DEFAULT_MAX_CHARS = 20000
DEFAULT_TIMEOUT_MS = 60000
LOGIN_TIMEOUT_MS = 600000  # 10 minutes per the interface contract.
PAUSE_MIN_S = 2.0
PAUSE_MAX_S = 5.0

CAPTCHA_MARKERS = (
    "captcha",
    "verify you are human",
    "unusual traffic",
    "are you a robot",
    "prove your humanity",
    "not for bots",
    "complete the challenge",
)
CAPTCHA_MARKERS_CJK = ("验证", "滑块", "安全验证")
LOGIN_MARKERS = (
    "log in",
    "sign in",
    "continue with google",
    "continue with apple",
    "continue with phone",
    "log in to",
    "sign up",
)
LOGIN_MARKERS_CJK = ("登录", "注册")
# Douyin shows a login modal whose text also contains 验证/验证码. These markers
# are checked before the CJK captcha markers so the modal reads as a login wall.
LOGIN_MODAL_MARKERS_CJK = ("扫码登录", "验证码登录", "密码登录", "手机号登录")
LOGIN_URL_SUBSTRINGS = (
    "/login",
    "/signin",
    "/i/flow/login",
    "/onboarding",
    "mode=login",
    "/account/login",
)
LOGIN_URL_HOST_PREFIXES = ("passport.", "accounts.")
CAPTCHA_URL_SUBSTRINGS = ("unhuman", "/captcha", "/challenge")

LOGIN_WALL_TEXT_LIMIT = 1500
EMPTY_TEXT_LIMIT = 200


@dataclass
class FetchResult:
    url: str
    final_url: str
    status: int | None
    title: str
    text: str
    chars_total: int
    blocked: bool
    block_reason: str
    error: str | None

    def as_dict(self) -> dict:
        return {
            "url": self.url,
            "final_url": self.final_url,
            "status": self.status,
            "title": self.title,
            "text": self.text,
            "chars_total": self.chars_total,
            "blocked": self.blocked,
            "block_reason": self.block_reason,
            "error": self.error,
        }


# ---------------------------------------------------------------------------
# Output helpers
# ---------------------------------------------------------------------------


def configure_stdio() -> None:
    """Make Windows consoles emit UTF-8 instead of dying on Chinese text."""
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is None:
            continue
        try:
            reconfigure(encoding="utf-8", errors="replace")
        except (OSError, ValueError):
            pass


def quiet_logging() -> None:
    """Keep cloakbrowser's progress logs off stdout and out of the JSON."""
    logging.basicConfig(level=logging.WARNING, stream=sys.stderr, force=True)
    logging.getLogger("cloakbrowser").setLevel(logging.ERROR)
    logging.getLogger("httpx").setLevel(logging.WARNING)


def install_hint() -> str:
    script = Path(__file__).resolve()
    return (
        f'uv run "{script}" --check; '
        f'if uv is unavailable: "{sys.executable}" -m pip install --user cloakbrowser '
        f'(add --break-system-packages if pip reports an externally-managed environment), '
        f'then "{sys.executable}" -m cloakbrowser install'
    )


def check_payload(version: str | None, binary: str) -> dict:
    ready = version is not None and binary == "ready"
    return {
        "ready": ready,
        "cloakbrowser": version,
        "binary": binary,
        "python": sys.executable,
        "hint": "" if ready else install_hint(),
    }


def emit_check(payload: dict) -> None:
    print(json.dumps(payload, ensure_ascii=False, indent=2))


def import_cloakbrowser():
    """Import cloakbrowser, returning (module, error)."""
    try:
        import cloakbrowser  # type: ignore import-not-found
    except Exception as exc:  # ImportError, or a broken dependency inside it.
        return None, exc
    return cloakbrowser, None


def resolve_binary_status(cloakbrowser) -> str:
    try:
        info = cloakbrowser.binary_info()
    except Exception:
        return "unknown"
    if not isinstance(info, dict):
        return "unknown"
    return "ready" if info.get("installed") else "missing"


# ---------------------------------------------------------------------------
# Block detection
# ---------------------------------------------------------------------------


def url_block_signal(final_url: str) -> str | None:
    """Return login_wall/captcha from URL structure, or None.

    A redirect to a login or challenge endpoint is a stronger signal than page
    text, which on these sites is often just a modal or a stub.
    """
    if not final_url:
        return None
    lowered = final_url.lower()
    try:
        host = (urlsplit(final_url).hostname or "").lower()
    except ValueError:
        host = ""
    if host.startswith(LOGIN_URL_HOST_PREFIXES) or any(
        marker in lowered for marker in LOGIN_URL_SUBSTRINGS
    ):
        return "login_wall"
    if any(marker in lowered for marker in CAPTCHA_URL_SUBSTRINGS):
        return "captcha"
    return None


def classify_block(
    status: int | None,
    text: str,
    final_url: str = "",
    title: str = "",
    is_json: bool = False,
) -> str:
    """Return none|http_error|login_wall|captcha|empty.

    Precedence, highest first:

    1. URL structure: /login, /signin, /i/flow/login, /onboarding, mode=login,
       /account/login, or a passport./accounts. host -> login_wall; unhuman,
       /captcha or /challenge -> captcha. This catches redirects that leave only
       a stub page behind.
    2. Chinese login-modal wording (扫码登录, 验证码登录, 密码登录, 手机号登录)
       -> login_wall, before the generic CJK captcha markers, so Douyin's modal
       is not called a captcha.
    3. Captcha text or title markers -> captcha. Checking the title catches
       Reddit's "Prove your humanity" even when the body is short.
    4. HTTP status >= 400 -> http_error.
    5. JSON responses are exempt from the text heuristics: an API payload can
       legitimately mention "captcha" in a story. For them only the status and
       empty checks apply.
    6. Login text markers, but only when the text is short (< 1500 chars) ->
       login_wall. This is what catches X's Continue-with-Google onboarding.
    7. Short text (< 200 chars) -> empty.
    8. Otherwise none.
    """
    stripped_len = len(text.strip())
    lowered = text.lower()
    title_lowered = title.lower()

    signal = url_block_signal(final_url)
    if signal is not None:
        return signal

    if not is_json:
        if any(marker in text for marker in LOGIN_MODAL_MARKERS_CJK):
            return "login_wall"
        if (
            any(marker in lowered for marker in CAPTCHA_MARKERS)
            or any(marker in text for marker in CAPTCHA_MARKERS_CJK)
            or any(marker in title_lowered for marker in CAPTCHA_MARKERS)
            or any(marker in title for marker in CAPTCHA_MARKERS_CJK)
        ):
            return "captcha"

    if status is not None and status >= 400:
        return "http_error"
    if is_json:
        return "empty" if stripped_len < EMPTY_TEXT_LIMIT else "none"

    if stripped_len < LOGIN_WALL_TEXT_LIMIT and (
        any(marker in lowered for marker in LOGIN_MARKERS)
        or any(marker in text for marker in LOGIN_MARKERS_CJK)
    ):
        return "login_wall"
    if stripped_len < EMPTY_TEXT_LIMIT:
        return "empty"
    return "none"


# ---------------------------------------------------------------------------
# Fetching
# ---------------------------------------------------------------------------


def read_page(page) -> tuple[str, str, str]:
    """Best-effort (title, text, final_url); never raises."""
    try:
        title = page.title() or ""
    except Exception:
        title = ""
    try:
        text = page.evaluate("document.body ? document.body.innerText : ''")
    except Exception:
        text = ""
    if not isinstance(text, str):
        text = ""
    try:
        final_url = page.url or ""
    except Exception:
        final_url = ""
    return title, text, final_url


def fetch_one(page, url: str, args) -> FetchResult:
    from playwright.sync_api import Error as PlaywrightError
    from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

    status: int | None = None
    response = None
    error: str | None = None
    timed_out = False
    is_json = False

    try:
        response = page.goto(url, wait_until="load", timeout=DEFAULT_TIMEOUT_MS)
        status = response.status if response is not None else None
        if response is not None:
            content_type = (response.headers or {}).get("content-type", "")
            is_json = "json" in content_type.lower()
        if args.wait_ms > 0:
            page.wait_for_timeout(args.wait_ms)
        for _ in range(max(0, args.scroll)):
            page.evaluate(
                "window.scrollBy(0, Math.max(window.innerHeight, 800))"
            )
            page.wait_for_timeout(750)
    except PlaywrightTimeoutError as exc:
        timed_out = True
        error = f"timeout after {DEFAULT_TIMEOUT_MS} ms: {exc}".strip()
    except PlaywrightError as exc:
        error = f"{type(exc).__name__}: {exc}"
    except Exception as exc:  # Never let one URL kill the run.
        error = f"{type(exc).__name__}: {exc}"

    title, text, final_url = read_page(page)
    final_url = final_url or url
    chars_total = len(text)
    shown = text[: args.max_chars] if args.max_chars > 0 else text

    if timed_out:
        block_reason = "timeout"
    elif error is not None and status is None:
        block_reason = "error"
    else:
        block_reason = classify_block(
            status=status,
            text=text,
            final_url=final_url,
            title=title,
            is_json=is_json,
        )

    return FetchResult(
        url=url,
        final_url=final_url,
        status=status,
        title=title,
        text=shown,
        chars_total=chars_total,
        blocked=block_reason != "none",
        block_reason=block_reason,
        error=error,
    )


def resolve_profile(profile_arg: str | None) -> Path | None:
    if profile_arg is None:
        return None
    if profile_arg == "":
        return DEFAULT_PROFILE_DIR
    return Path(os.path.expanduser(profile_arg))


def print_md(results: list[FetchResult]) -> None:
    for index, result in enumerate(results):
        if index:
            print()
        print(f"## {result.url}")
        print(f"- final_url: {result.final_url}")
        print(f"- status: {result.status}")
        print(f"- blocked: {str(result.blocked).lower()} ({result.block_reason})")
        print(f"- chars_total: {result.chars_total}")
        print(f"- title: {result.title}")
        print(f"- error: {result.error}")
        print()
        print(result.text)


def run_fetch(cloakbrowser, args) -> int:
    profile_dir = resolve_profile(args.profile)
    headless = not args.headed
    launch_kwargs = {"headless": headless, "humanize": True}

    browser = None
    context = None
    try:
        if profile_dir is not None:
            profile_dir.mkdir(parents=True, exist_ok=True)
            context = cloakbrowser.launch_persistent_context(
                str(profile_dir), **launch_kwargs
            )
            page_factory = context.new_page
            closer = context.close
        else:
            browser = cloakbrowser.launch(**launch_kwargs)
            page_factory = browser.new_page
            closer = browser.close

        results: list[FetchResult] = []
        try:
            for index, url in enumerate(args.url):
                if index:
                    time.sleep(random.uniform(PAUSE_MIN_S, PAUSE_MAX_S))
                page = page_factory()
                try:
                    results.append(fetch_one(page, url, args))
                finally:
                    try:
                        page.close()
                    except Exception:
                        pass
        finally:
            try:
                closer()
            except Exception:
                pass
    except Exception as exc:
        print(
            f"{type(exc).__name__}: {exc}",
            file=sys.stderr,
        )
        return EXIT_ERROR

    if args.format == "json":
        print(json.dumps([r.as_dict() for r in results], ensure_ascii=False, indent=2))
    else:
        print_md(results)

    return EXIT_OK if any(not r.blocked for r in results) else EXIT_ALL_BLOCKED


# ---------------------------------------------------------------------------
# Login (one-time, interactive)
# ---------------------------------------------------------------------------


def run_login(cloakbrowser, args) -> int:
    profile_dir = resolve_profile(args.profile)
    if profile_dir is None:
        profile_dir = DEFAULT_PROFILE_DIR
    profile_dir.mkdir(parents=True, exist_ok=True)

    context = None
    page = None
    try:
        context = cloakbrowser.launch_persistent_context(
            str(profile_dir), headless=False, humanize=True
        )
        page = context.pages[0] if context.pages else context.new_page()
        try:
            page.goto(args.login, wait_until="load", timeout=DEFAULT_TIMEOUT_MS)
        except Exception as exc:
            print(f"Could not load {args.login}: {exc}", file=sys.stderr)
        print("Sign in in the browser window, then close it.", flush=True)
        try:
            page.wait_for_event("close", timeout=LOGIN_TIMEOUT_MS)
        except Exception:
            pass
        return EXIT_OK
    except Exception as exc:
        print(f"{type(exc).__name__}: {exc}", file=sys.stderr)
        return EXIT_ERROR
    finally:
        if context is not None:
            try:
                context.close()
            except Exception:
                pass


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="stealth_fetch.py",
        description=(
            "Fetch bot-walled pages with CloakBrowser (stealth Chromium) and "
            "report whether each page was blocked. Read-only: it never clicks, "
            "types, submits forms, or handles credentials."
        ),
        epilog=(
            "Examples:\n"
            "  %(prog)s --check\n"
            "  %(prog)s --url https://example.com --url https://x.com/AnthropicAI\n"
            "  %(prog)s --url https://old.reddit.com/r/algotrading/top/ "
            "--headed --wait-ms 4000 --format md\n"
            "  %(prog)s --profile --url https://www.reddit.com/r/algotrading/\n"
            "  %(prog)s --login https://x.com\n\n"
            "Exit codes: 0 at least one page fetched (or --check ready / --login), "
            "3 cloakbrowser missing, 4 every page blocked."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Print one JSON readiness object and exit (0 ready, 3 not ready).",
    )
    parser.add_argument(
        "--url",
        action="append",
        metavar="URL",
        help="URL to fetch; repeat the flag to fetch several in one browser.",
    )
    parser.add_argument(
        "--headed",
        action="store_true",
        help="Show the browser window instead of running headless.",
    )
    parser.add_argument(
        "--profile",
        nargs="?",
        const="",
        default=None,
        metavar="DIR",
        help=(
            "Use a persistent profile so sign-ins persist. With no DIR, uses "
            f"{DEFAULT_PROFILE_DIR}."
        ),
    )
    parser.add_argument(
        "--wait-ms",
        type=int,
        default=DEFAULT_WAIT_MS,
        metavar="MS",
        help=f"Extra wait after load, in milliseconds (default {DEFAULT_WAIT_MS}).",
    )
    parser.add_argument(
        "--scroll",
        type=int,
        default=0,
        metavar="N",
        help="Scroll down N times to trigger lazy content (default 0).",
    )
    parser.add_argument(
        "--max-chars",
        type=int,
        default=DEFAULT_MAX_CHARS,
        metavar="N",
        help=f"Truncate each page's text to N characters (default {DEFAULT_MAX_CHARS}).",
    )
    parser.add_argument(
        "--format",
        choices=("json", "md"),
        default="json",
        help="Output format (default json).",
    )
    parser.add_argument(
        "--login",
        metavar="URL",
        help=(
            "Open a headed persistent-profile browser at URL for a one-time "
            "sign-in, then wait for the window to close (max 10 minutes)."
        ),
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    configure_stdio()
    quiet_logging()
    parser = build_parser()
    args = parser.parse_args(argv)

    if not args.check and not args.url and not args.login:
        parser.error("one of --check, --url, or --login is required")

    cloakbrowser, import_error = import_cloakbrowser()
    if cloakbrowser is None:
        payload = check_payload(None, "unknown")
        emit_check(payload)
        if import_error is not None:
            print(f"cloakbrowser is not available: {import_error}", file=sys.stderr)
        return EXIT_NOT_READY

    if args.check:
        version = getattr(cloakbrowser, "__version__", None)
        binary = resolve_binary_status(cloakbrowser)
        payload = check_payload(version, binary)
        emit_check(payload)
        return EXIT_OK if payload["ready"] else EXIT_NOT_READY

    if args.login:
        return run_login(cloakbrowser, args)

    return run_fetch(cloakbrowser, args)


if __name__ == "__main__":
    sys.exit(main())