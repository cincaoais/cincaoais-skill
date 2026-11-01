# stealth_fetch.py — CloakBrowser probe notes (W2)

Date: 2026-11-01. Read-only probe: no sign-ins, no clicks, no typing. Sites change; this is a snapshot.

## Environment

- OS: Windows 11 (10.0.26200).
- Python: `C:\Users\Tang Cong Han\AppData\Roaming\uv\python\cpython-3.12.11-windows-x86_64-none\python.exe`, Python 3.12.11.
  - `py -3` resolves to the Windows Store Python 3.13, but every launch failed with `Access is denied`.
  - `python` and `python3` are not on `PATH`. The uv-managed CPython 3.12.11 was the first interpreter that ran.
- cloakbrowser: **0.6.5** (free tier), installed into the user site
  `C:\Users\Tang Cong Han\AppData\Roaming\Python\Python312\site-packages`.
- Bundled stealth Chromium: **146.0.7680.177.5**, at
  `C:\Users\Tang Cong Han\.cloakbrowser\chromium-146.0.7680.177.5\chrome.exe`.
- Install commands actually run (the uv Python is PEP 668 "externally managed", so `--break-system-packages`
  was needed; the package still went to the user site, not into the interpreter):

```sh
"<py>" -m pip install --user --break-system-packages cloakbrowser
"<py>" -m cloakbrowser install
```

`--check` output:

```json
{
  "ready": true,
  "cloakbrowser": "0.6.5",
  "binary": "ready",
  "python": "C:\\Users\\Tang Cong Han\\AppData\\Roaming\\uv\\python\\cpython-3.12.11-windows-x86_64-none\\python.exe",
  "hint": ""
}
```

Exit code 0.

Probe settings unless noted: headless, `--wait-ms 3000` (default), no `--scroll`, `--max-chars 20000`,
60 s navigation timeout. One browser per batch, 2–5 s random pause between URLs. A `--profile` smoke test
on example.com created `~/.cloakbrowser-profiles/research` and returned `blocked: false / none / 917`.

## Results

Headless and headed runs used the same flags; "same" repeats the headless numbers. Headed was tried for
the walled rows (and for Reddit search / X search, which the heuristics missed) — no wall changed.

| Site | URL | Headless: blocked / block_reason / chars_total | Headed: blocked / block_reason / chars_total | First ~150 chars | Judgment |
|---|---|---|---|---|---|
| example.com (control) | `https://example.com` | false / none / 917 | not needed | This domain is for use in documentation examples without needing permission. This is not a service; avoid relying on it for testing and monitoring pur | works |
| Hacker News (control) | `https://news.ycombinator.com` | false / none / 4122 | not needed | Hacker Newsnew \| past \| comments \| ask \| show \| jobs \| submit login 1. Malware uses LLMs to rank victims by how much they're worth (talosintelligence. | works |
| Reddit search | `https://www.reddit.com/r/algotrading/search/?q=backtest&restrict_sr=1` | false / none / 240 | same (false / none / 240) | Prove your humanity We’re committed to safety and security. But not for bots. Complete the challenge below and let us know you’re a real person. Reddi | captcha |
| old Reddit | `https://old.reddit.com/r/algotrading/top/?t=month` | true / login_wall / 416 | same (true / login_wall / 416) | Skip to main content Log in to use old Reddit To keep Reddit safe, accounts are required to access old Reddit. Log in, or continue without an account | needs login |
| X search | `https://x.com/search?q=cloakbrowser&f=live` | false / none / 245 | same (false / none / 245) | See what's happening Select an option below: Continue with phone Continue with Google Continue with Google Continue with Apple or Email or username Co | needs login |
| X profile | `https://x.com/AnthropicAI` | false / none / 2354 | not needed | Anthropic 1,740 posts Anthropic @AnthropicAI We're an AI safety and research company that builds reliable, interpretable, and steerable AI systems. Ta | works |
| Douyin search | `https://www.douyin.com/search/%E9%87%8F%E5%8C%96%E4%BA%A4%E6%98%93` | true / timeout / 624 | true / captcha / 170 | 开启读屏标签 读屏标签已关闭 精选 推荐 关注 朋友 我的 小游戏 下载抖音精选 2026 © 抖音 京ICP备16016397号-3 京公网安备11010802050006号 电子营业执照 信息网络传播视听节目许可证 0126733 广播电视节目制作经营许可证 （京）字第11313号 增值电信业务 | needs login |
| Bilibili search | `https://search.bilibili.com/all?keyword=%E9%87%8F%E5%8C%96%E4%BA%A4%E6%98%93` | false / none / 2711 | not needed | 下载客户端 登录 Switch language here after login ! 更多 消息 动态 收藏 历史 创作中心 投稿 搜索 综合 番剧 0 用户 99+ 16.6万 212 08:29 量化交易普通人为什么根本没机会 MatthewTL · 5月2日 263 0 02:05:47 【 | works |
| Zhihu search | `https://www.zhihu.com/search?q=%E9%87%8F%E5%8C%96%E4%BA%A4%E6%98%93` | true / captcha / 81 | same (true / captcha / 81) | 进入知乎 系统监测到您的网络环境存在异常，为保证您的正常访问，请点击下方验证按钮进行验证。在您验证完成前，该提示将多次出现。 开始验证 登录知乎 · 意见反馈 | captcha |
| HN Algolia API | `https://hn.algolia.com/api/v1/search?query=cloakbrowser&tags=story` | false / none / 21942 | not needed | {"exhaustive":{"nbHits":false,"typo":false},"exhaustiveNbHits":false,"exhaustiveTypo":false,"hits":[{"_highlightResult":{"author":{"matchLevel":"none" | works |

Notes on the literal output:

- Douyin headless was flaky. The final headless run hit the 60 s navigation timeout (blocked `timeout`,
  624 chars); an earlier headless run returned status 200, 623 chars, `captcha`. Both showed only the
  footer plus a login modal, never search results. Headed settled on status 200, 170 chars, `captcha`.
- Reddit search returns status 200 and the heuristic says `none` because its text (240 chars) lacks the
  listed markers. The title is "Reddit - Prove your humanity" and the body asks the reader to complete a
  challenge: it is a captcha wall in practice.
- X search redirects to
  `https://x.com/i/jf/onboarding/web?redirect_after_login=%2Fsearch...&mode=login`; the 245-char
  onboarding text has no "log in"/"sign in", so the heuristic says `none`. It needs a signed-in profile.
- Zhihu's final URL is `/account/unhuman?...&need_login=true` with status 403; the page says 安全验证.
- Douyin's page contains "验证码登录" (verification-code login), so the 验证 marker labels it `captcha`
  even though what it shows is a login modal. The headed text was the same footer plus a login modal
  (`扫码登录` / `验证码登录`), not search results.
- Character counts and snippets are live and differ slightly run to run (HN Algolia returned 3,138 chars
  on one run and 21,942 on the final one).

## Takeaways for the skill writer

- Without login, these worked: example.com, Hacker News HTML, an X **profile** page (`x.com/AnthropicAI`,
  bio/posts readable), Bilibili search (2.7k chars of real results), and the HN Algolia JSON API
  (20k+ chars). X profile pages do not need the login flow; X **search** does.
- These need a signed-in persistent profile: old Reddit (`login_wall`), X search (login onboarding), and
  Douyin search (login modal). Whether `--login` actually unlocks them is **unverified** — this probe was
  read-only and never signed in.
- These are captcha walls that headed mode did not fix: Reddit www search ("Prove your humanity") and
  Zhihu search (403 安全验证). Skip them or try `--login`, but expect a challenge either way.
- Treat `block_reason` as a hint, not a verdict: Reddit's and X search's walls come back as `none`, and
  Douyin's login modal comes back as `captcha`. Read `title`, `final_url` and `blocked` together, and
  fall back on the judgment column here.
- Douyin headless is slow and flaky (one 60 s timeout); if it matters, use `--headed` and expect a login
  modal. Bilibili is the reliable Chinese source without sign-in, so prefer it for Chinese-language
  searching; Zhihu needs a workaround.
- For API endpoints, check `content-type: application/json` and skip the captcha/login text heuristics —
  otherwise a story that merely mentions "captcha" (as HN Algolia's results do) can be misread as a wall.
  The helper does this already.
- After the W2b fix, `block_reason` matches the judgment column for all eight probe rows (see the W2b
  section below); no site still mislabels.

## After the heuristic fix (W2b)

Re-ran the eight probe URLs once, live and headless, on 2026-11-01 with
`uv run plugins/rnd/skills/rnd/scripts/stealth_fetch.py --url ... --format json` (same defaults:
`--wait-ms 3000`, no `--scroll`, `--max-chars 20000`, 60 s timeout). Douyin returned in headless
mode this time, so no `--headed` rerun was needed.

| Site | blocked | block_reason | chars_total | matches the judgment column? |
|---|---|---|---|---|
| Reddit search | true | captcha | 240 | yes |
| old Reddit | true | login_wall | 416 | yes |
| X search | true | login_wall | 245 | yes |
| X profile | false | none | 2354 | yes |
| Douyin search | true | login_wall | 623 | yes |
| Bilibili search | false | none | 2696 | yes |
| Zhihu search | true | captcha | 81 | yes |
| HN Algolia API | false | none | 21842 | yes |

Live character counts drift a little from the W2 run (Bilibili 2711 -> 2696, HN Algolia 21942 -> 21842);
the labels and judgments did not change.
