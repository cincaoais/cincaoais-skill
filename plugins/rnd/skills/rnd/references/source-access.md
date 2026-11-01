# Source access

Some of the best practitioner discussion lives behind bot walls. `scripts/stealth_fetch.py` wraps
CloakBrowser — a stealth Chromium with its bundled Playwright — to fetch those pages read-only. Normal
fetch and search first; use the helper only when a source you actually need refuses.

## Setup and readiness

The script carries a PEP 723 header, so `uv` installs its dependencies on demand:

```sh
uv run "<skill-dir>/scripts/stealth_fetch.py" --check
```

If `uv` is unavailable, use a Python 3.10+ interpreter that already has `cloakbrowser` installed, with
`python "<skill-dir>/scripts/stealth_fetch.py" --check` instead of the `uv run` form. Otherwise install
it once:

```sh
<py> -m pip install cloakbrowser
<py> -m cloakbrowser install
```

The second command downloads the stealth Chromium build (about 200 MB). If pip refuses because the
interpreter is externally managed, prefer a virtual environment or the override pip suggests, then run
the `cloakbrowser install` step. `uv run` avoids the problem entirely because it installs the script's
declared dependencies into its own environment.

`--check` prints one JSON object and never raises a traceback:

```json
{
  "ready": true,
  "cloakbrowser": "0.6.5",
  "binary": "ready",
  "python": "C:\\...\\python.exe",
  "hint": ""
}
```

`ready` is true only when the package imports and the browser binary is installed. If it is false,
`hint` contains the install path for that interpreter.

## CLI reference

```
stealth_fetch.py [-h] [--check] [--url URL] [--headed] [--profile [DIR]]
                 [--wait-ms MS] [--scroll N] [--max-chars N]
                 [--format {json,md}] [--login URL]
```

| Flag | What it does |
| --- | --- |
| `--check` | Print the readiness JSON and exit. Use before planning work on a walled site. |
| `--url URL` | URL to fetch. Repeat the flag to fetch several URLs in one browser. |
| `--headed` | Show the browser window. Use when a headless result is suspicious or flaky. |
| `--profile [DIR]` | Use a persistent profile so sign-ins persist. With no `DIR`, uses `~/.cloakbrowser-profiles/research`. |
| `--wait-ms MS` | Extra wait after page load, in milliseconds (default 3000). |
| `--scroll N` | Scroll down N times to trigger lazy content (default 0). |
| `--max-chars N` | Truncate each page's text to N characters (default 20000). |
| `--format {json,md}` | Output format (default `json`). `md` is easier to skim; `json` is easier to filter. |
| `--login URL` | Open a headed persistent-profile browser at URL for a one-time sign-in. Waits for the window to close, or 10 minutes. |
| `--help` | Print the same help text. |

All examples use `uv run`; without `uv`, replace it with the interpreter path, for example
`python "<skill-dir>/scripts/stealth_fetch.py" --check`.

Each URL result has these fields:

```
url, final_url, status, title, text, chars_total, blocked, block_reason, error
```

`text` is truncated to `--max-chars`; `chars_total` is the untruncated length. The helper pauses 2–5
seconds between URLs and gives each navigation 60 seconds.

Exit codes: `0` means at least one page was not blocked (or `--check` is ready, or `--login` finished);
`3` means cloakbrowser is missing or not ready; `4` means every URL was blocked; `1` means the browser
failed to launch for an unexpected reason.

Examples:

```sh
# One readable page, human-friendly output
uv run "<skill-dir>/scripts/stealth_fetch.py" \
  --url https://x.com/AnthropicAI --format md

# Several URLs in one browser, with a longer wait and lazy-content scrolling
uv run "<skill-dir>/scripts/stealth_fetch.py" \
  --url https://www.reddit.com/r/algotrading/search/?q=backtest \
  --url https://old.reddit.com/r/algotrading/top/?t=month \
  --wait-ms 4000 --scroll 2 --max-chars 40000

# Reuse the signed-in profile once the login flow has been run
uv run "<skill-dir>/scripts/stealth_fetch.py" \
  --profile --url https://x.com/search?q=cloakbrowser --format json
```

## Reading the result

Read `blocked`, `block_reason`, `title` and `final_url` together. The current helper labelled every
probed site in line with the judgments below, but sites change: a redirect to `/onboarding` or
`/i/flow/login` is a login wall even when the visible text is short, and a 200 page titled "Prove your
humanity" is a captcha wall even when the body has more than 200 characters. Treat the reason as a
strong signal, not an oracle.

| `block_reason` | What it usually means | What to try next |
| --- | --- | --- |
| `none` | The page loaded and looks real | Read the text; spot-check the title and length. |
| `http_error` | Status 400 or above | Check the URL or the site's current structure; a 403 often means a wall. |
| `login_wall` | Login/onboarding page or modal | Run the one-time `--login` flow, then retry with `--profile`. |
| `captcha` | Captcha or human-verification page | Try `--login`; if it persists, skip the source and record the gap. |
| `empty` | Under 200 characters of text | Add `--wait-ms`, `--scroll`, or try `--headed`; JavaScript may not have run. |
| `timeout` | The 60-second navigation timeout | Retry once; then try `--headed` or skip. Douyin is known to be flaky. |
| `error` | Playwright or navigation error | Read `error`; retry once before treating the source as unreachable. |

When a page's `text` contains JSON, the script detects the content type and skips the captcha/login text
heuristics, so an API story that merely mentions "captcha" is not misread as a wall. Still check the
`status`.

## One-time login

```sh
uv run "<skill-dir>/scripts/stealth_fetch.py" --login https://x.com
```

This opens a visible browser on the persistent profile. Sign in yourself, then close the window; it
prints "Sign in in the browser window, then close it." and waits up to 10 minutes. Later fetches reuse
the profile with `--profile` (default `~/.cloakbrowser-profiles/research`, on Windows
`C:\Users\<you>\.cloakbrowser-profiles\research`), or with `--profile DIR` if you chose a custom
directory.

Offer the login flow once per site. If the user declines, carry on without it and list what was missed.
The helper never types credentials, clicks, or stores them in arguments or files — the sign-in happens
by hand in the visible browser. Keep it read-only: no posting, liking, following, commenting, messaging
or form submission, and pause between page loads on the same site.

## Per-site snapshot (probe dated 2026-11-01)

Read-only probe on Windows 11 with cloakbrowser 0.6.5 and its bundled Chromium; headless unless noted,
`--wait-ms 3000`, no `--scroll`, `--max-chars 20000`. Sites change, and the text on a page is live, so
this is a snapshot, not a permanent contract.

The results below are from the re-run after the heuristic fix, so `block_reason` matches the judgment
column for all eight walled/relevant rows. The two controls were measured in the first run.

| Site | URL tried | Headless: blocked / reason / chars | Headed | Sign-in needed | Judgment |
| --- | --- | --- | --- | --- | --- |
| example.com (control) | `https://example.com` | false / none / 917 | not needed | no | Works without login |
| Hacker News (control) | `https://news.ycombinator.com` | false / none / 4122 | not needed | no | Works without login |
| Reddit search | `https://www.reddit.com/r/algotrading/search/?q=backtest&restrict_sr=1` | true / captcha / 240 | same wall | no — captcha in practice | Skip (captcha wall) |
| old Reddit | `https://old.reddit.com/r/algotrading/top/?t=month` | true / login_wall / 416 | same wall | yes | Needs one-time `--login` (unverified) |
| X search | `https://x.com/search?q=cloakbrowser&f=live` | true / login_wall / 245 | same wall | yes | Needs one-time `--login` (unverified) |
| X profile | `https://x.com/AnthropicAI` | false / none / 2354 | not needed | no | Works without login |
| Douyin search | `https://www.douyin.com/search/%E9%87%8F%E5%8C%96%E4%BA%A4%E6%98%93` | true / login_wall / 623 | login modal (captcha label in the first run) | yes | Needs one-time `--login` (unverified; flaky) |
| Bilibili search | `https://search.bilibili.com/all?keyword=%E9%87%8F%E5%8C%96%E4%BA%A4%E6%98%93` | false / none / 2696 | not needed | no | Works without login |
| Zhihu search | `https://www.zhihu.com/search?q=%E9%87%8F%E5%8C%96%E4%BA%A4%E6%98%93` | true / captcha / 81 | same wall | no — captcha persists | Skip (captcha wall) |
| HN Algolia API | `https://hn.algolia.com/api/v1/search?query=cloakbrowser&tags=story` | false / none / 21842 | not needed | no | Works without login |

What the snapshot means in practice:

- **Works without login:** Hacker News HTML, an X *profile* page, Bilibili search, and the HN Algolia
  JSON API. Prefer Bilibili for Chinese-language searching.
- **Needs one-time `--login`:** old Reddit, X *search*, and Douyin search. The probe was read-only and
  never signed in, so whether the sign-in actually unlocks them is unverified. Try it once, and fall
  back to the skip row if the wall persists.
- **Skip, or expect a challenge:** Reddit `www` search and Zhihu search are captcha walls that headed
  mode did not fix. Douyin headless is slow and flaky; use `--headed` if it matters and expect a login
  modal.
- The first probe run, before the heuristic fix, mislabeled Reddit search and X search as `none` and
  Douyin's login modal as `captcha`. The current helper labels all eight rows as shown. Character counts
  drift between runs (Bilibili 2711 -> 2696, HN Algolia 21942 -> 21842); the judgments did not change.

If a walled source is skipped, say so under "Coverage gaps" in the report and name what it would have
added — for example, "X search skipped; direct practitioner reaction to the framework is missing."