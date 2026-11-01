# Search angles

Search with the field's vocabulary, not the user's first phrasing. The keyword map turns a topic into
that vocabulary. Build it before the first search, then grow it after every useful source. Detailed
access notes for each platform are in `source-access.md`.

## The keyword-map worksheet

One table is enough. Keep it in a scratch file next to the report, so a long run can survive a lost
context. Add rows as you learn; the point is coverage, not neatness.

| Angle | What to extract | Example query shapes | Source it suits |
| --- | --- | --- | --- |
| User's words | The topic as stated, plus synonyms they might accept | `"<user phrase>"`, `<user phrase> alternative` | Web search, GitHub |
| Problem language | How the sufferer describes the symptom, not the solution | `"how do I stop <symptom>"`, `"<symptom>" <domain>` | Reddit, Hacker News, Stack Overflow |
| Expert jargon | The word a practitioner would use for the solution | `<concept> architecture`, `<technique> tutorial`, `<acronym>` | Docs, papers, expert blogs |
| Named artifacts | Tools, libraries, frameworks, papers, people, companies | `<tool> vs`, `"<paper title>"`, `<company> engineering blog` | GitHub, docs, papers |
| Comparisons and alternatives | The shortlist, and what each is chosen over | `<tool> alternatives`, `<tool> vs <tool>`, `best <category> 2026` | Web search, awesome-lists |
| Failures and critiques | Limits, migrations away, production pain | `<tool> problems`, `<tool> issues`, `why we moved off <tool>` | Issues, Reddit, HN |
| GitHub vocabulary | Words that match repo names, descriptions and topics | `awesome <topic>`, `topic:<tag>`, `<topic> self-hosted`, `<topic> boilerplate` | GitHub search |
| Chinese-language | Local terms, tools and practice when the field is active in China | `<中文关键词>`, `<中文关键词> 教程`, `<中文关键词> 开源` | Bilibili, Zhihu, Douyin, CSDN, Juejin |
| Adjacent fields | Other domains that solved the same shape of problem | `<problem> in <adjacent field>` | Papers, cross-domain blogs |
| People and orgs | Researchers, maintainers, teams whose work anchors the field | `"<person>" <topic>`, `<lab> <topic>` | Papers, GitHub, talks |

## Worked example: "local LLM code review bot"

Start from the prompt: *"I want a bot that reviews pull requests with a local LLM, in CI, with no code
leaving the machine."* The first query, taken literally, is weak. `local LLM code review bot` mostly
returns listicles and vendor pages. The map fixes that.

**Round one — the obvious angles.**

The "What came back" column and the terms in round two are illustrative of what such searches
typically surface, not transcripts of a real run.

| Angle | Query tried | What came back |
| --- | --- | --- |
| User's words | `local LLM code review bot` | Vendor blogs, generic "AI code review" listicles |
| Problem language | `automate PR review without sending code to the cloud` | Reddit and HN threads about privacy and CI cost |
| Expert jargon | `LLM code review agent architecture` | Papers and engineering blogs using "code review agent", "LLM-as-a-judge" |
| Named artifacts | `ollama code review github action` | A few GitHub Actions and small repos |
| Comparisons | `coderabbit alternatives self-hosted` | Commercial and open options, including PR-Agent |

**Round two — snowball from what those sources named.** The listicles mention commercial products;
the HN threads mention the open alternatives by name; the GitHub repos carry topic tags and link to
each other. New terms: `PR-Agent`, `Qodo Merge`, `self-hosted code review`, `diff review`, `review
comment generation`, `Qwen2.5-Coder`, `llama.cpp`, `Ollama`, `vLLM`, `SWE-bench`, `CodeRabbit
self-hosted`, `local-first AI review`. The Chinese angle adds `本地大模型 代码审查`, `私有化 代码审查`,
`代码审查 Agent`.

**Round three — the final map, ready to run.**

| Angle | Queries | Where |
| --- | --- | --- |
| Existing products to learn from | `PR-Agent`, `Qodo Merge self-hosted`, `CodeRabbit self-hosted`, `reviewdog` | GitHub, vendor docs |
| Open implementations | `gh search repos "code review LLM" --sort stars`, `topic:code-review`, `awesome code review` | GitHub |
| Local serving | `ollama code review`, `vLLM code review agent`, `llama.cpp structured output` | GitHub, docs |
| Quality and evaluation | `LLM code review benchmark`, `SWE-bench review`, `false positive code review LLM` | Papers, blogs |
| Production pain | `PR-Agent issues self-hosted`, `AI code review too noisy`, `why we turned off AI review` | GitHub issues, Reddit, HN |
| Chinese practice | `本地大模型 代码审查`, `私有化 代码审查 开源`, `代码审查 Agent 实践` | Bilibili, Zhihu, CSDN |
| Adjacent | `static analysis LLM reranking`, `LLM-as-a-judge code` | Papers |

The map now supports a decision: reuse an existing review agent with a local OpenAI-compatible
endpoint, or build a thin CI wrapper around it. The searches that matter are the ones that measure
maturity and noise, not the ones that repeat the original phrasing.

**What a real run does next.** It reads the READMEs and the issue trackers of the top candidates, looks
for a self-hosted/local-model path in their docs, checks release cadence and licence, and reads the
complaints about false positives. Only then does it form a verdict.

## GitHub query cookbook

```sh
gh search repos "<terms>" --sort stars --limit 20 \
  --json fullName,stargazersCount,pushedAt,license,description

gh search repos "<terms>" --sort updated --limit 20 \
  --json fullName,stargazersCount,pushedAt,description

gh search code "<symbol or phrase>" --language python
gh search issues "<pain words>" --repo owner/repo --state all --limit 20

gh api repos/owner/repo --jq \
  '{stars: .stargazers_count, pushed: .pushed_at, issues: .open_issues_count,
    license: .license.spdx_id, archived: .archived, topics: .topics}'

gh api "repos/owner/repo/releases?per_page=5" --jq '.[] | {tag: .tag_name, date: .published_at}'
```

Useful qualifiers inside `<terms>`: `topic:<tag>`, `stars:>500`, `pushed:>2025-01-01`,
`language:python`, `archived:false`. Search descriptions, not just names, when the obvious name is
taken. For curated starting points search `awesome <topic>` and read the list's own last-update date.

Read a candidate repo like a reviewer: README for scope and installation, `docs/` for the real
workflow, issues for recurring pain, releases for cadence, tests and CI for whether anyone verifies
claims. Stars date quickly; last push and whether maintainers answer issues say more.

## Community and platform patterns

- **Hacker News** — HTML search at `https://hn.algolia.com/api/v1/search?query=<terms>&tags=story`
  returns JSON and has no bot wall. Also usable from the site. Good for candid "we tried this" threads.
- **Reddit** — `https://www.reddit.com/search/?q=<terms>&sort=relevance&t=year` and
  `https://old.reddit.com/r/<sub>/search?q=<terms>&restrict_sr=on`. Both commonly hit a captcha or login
  wall; see `source-access.md` before planning around them.
- **X** — profile pages such as `https://x.com/<handle>` are readable without signing in; search at
  `https://x.com/search?q=<terms>&f=live` needs a signed-in profile. Use profiles for named
  practitioners and threads, not as the primary search engine.
- **Bilibili** — `https://search.bilibili.com/all?keyword=<中文关键词>` returned real results in the
  probe. The most reliable Chinese-language search source without sign-in.
- **Douyin** — `https://www.douyin.com/search/<中文关键词>` showed only a login modal in the probe.
- **Zhihu** — `https://www.zhihu.com/search?q=<中文关键词>` hit a captcha wall in the probe.
- **Xiaohongshu, CSDN, Juejin** — try normal search first; treat them like the walled sites above when
  they refuse.

Search-engine operators still help across all of these: `site:reddit.com <terms>`,
`site:github.com <terms>`, `site:news.ycombinator.com <terms>`, `<terms> after:2025-01-01`. They also
find cached or mirrored discussions when the original page is walled.