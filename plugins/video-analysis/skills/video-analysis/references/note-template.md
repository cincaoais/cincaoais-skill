# Knowledge Notes — Output Template

Follow this structure exactly. Sections marked (omit if empty) may be dropped;
everything else always appears. Write in the video's primary language unless
the user requested otherwise. Save as `<sanitized-video-title>.md`.

## Why this format

These notes serve two masters: a human re-reading them later, and downstream
reuse as prompt material. That is why atomic knowledge lives in its own section
(easy to lift line-by-line) and why the final Distillation must be fully
self-contained — the user pastes it into other systems' prompts, where "the
video" and "the speaker" mean nothing.

## Template

```markdown
---
title: "<video title>"
source: "<url or local path>"
platform: <youtube|tiktok|douyin|rednote|bilibili|local|other>
creator: "<uploader/creator if known>"
duration: "<mm:ss>"
language: <zh|en|mixed|...>
analyzed: <YYYY-MM-DD>
content_type: <tutorial|talk|review|vlog|demo|documentary|course|other>
tags: [<3-8 topical tags>]
---

# <Video title>

## 摘要 / Summary
<2–4 sentences: what the video is, who it's for, its core claim or purpose.>

## 核心要点 / Key Takeaways
<5–10 bullets. Each one a complete, standalone insight — not a topic label.
Bad: "Discusses pricing." Good: "Price anchoring works best when the anchor
appears before the real price, ideally 3–5× higher.">

## 内容分解 / Timestamped Breakdown
### [00:00] <segment heading>
<What is taught/shown/argued in this segment. Include concrete details:
numbers, names, steps, formulas, exact terms used. Quote short memorable
phrases with quotation marks and timestamp.>

### [02:35] <next segment heading>
<...continue for each meaningful segment. Segment at topic changes, not at
fixed intervals.>

## 视觉信息 / Visual-Only Information (omit if empty)
<Knowledge visible on screen but never spoken: on-screen text and captions,
charts and their actual values, UI steps in demos, ingredient amounts shown,
product details, diagrams. Cite timestamps. This section is the main payoff
of frame analysis — be thorough here.>

## 知识点提取 / Extracted Knowledge
<Atomic, context-free factual statements and claims from the video, one per
line, no timestamps. Each line must be understandable with zero context.
Mark disputed/unverified claims with (claim). This is the section designed
for line-by-line reuse.>
- <fact 1>
- <fact 2>
- ...

## 金句引用 / Notable Quotes (omit if empty)
- [mm:ss] "<verbatim quote>" — <why it matters, one clause>

## 疑点与局限 / Caveats (omit if empty)
<Errors spotted, outdated info, sponsored-content signals, claims that
contradict established knowledge — with your reasoning.>

## Prompt-Ready Distillation
<A fenced code block containing a self-contained restatement of the video's
knowledge/methodology, written as if it were reference material or system-
prompt instructions. Rules:
- NO references to "the video", "the speaker", "as shown above"
- Imperative or declarative voice ("Do X", "X works because Y")
- Include the concrete parameters, steps, and numbers — not summaries of them
- Dense but complete: this block alone should transfer the video's usable
  knowledge to another AI system>

    ```
    <distilled content here>
    ```
```

## Quality bar

- Every number, name, and step from the video that a reader might act on must
  appear somewhere in the notes. If it was worth saying in the video, it's
  worth capturing.
- Timestamps must be real (from transcript/frame names), never invented.
- If audio and visuals contradict each other, note both with timestamps.
- Do not pad. A 60-second video produces short notes; that is correct.
