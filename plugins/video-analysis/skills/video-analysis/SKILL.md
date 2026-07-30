---
name: video-analysis
description: >
  Watch, analyze, and take knowledge notes from videos. Use this skill whenever the
  user provides a video URL (YouTube, TikTok, Douyin 抖音, RedNote/Xiaohongshu 小红书,
  Bilibili, or any yt-dlp-supported site) or a local video file path (.mp4, .mov, .mkv,
  .webm, .avi), and wants any of: analysis, a summary, notes, knowledge extraction,
  a transcript, "what does this video say", "总结这个视频", "帮我做笔记", or wants the
  video's content turned into a prompt or document. Trigger even if the user just
  pastes a video link with a short question about it — answering requires actually
  watching the video via this skill, never guessing from the URL or title.
---

# Video Analysis & Knowledge Notes

Turn any video into structured knowledge notes by decomposing it into frames
(visual) and a transcript (audio), analyzing both, and writing notes using the
template in `references/note-template.md`.

Claude cannot watch video files directly. The pipeline below converts the video
into things Claude can read: images and text. Never skip the pipeline and guess
content from a URL, title, or thumbnail.

## Dependencies

Required: `ffmpeg`/`ffprobe`, `yt-dlp` (for URLs). For transcription when no
captions exist: one of `faster-whisper`, `whisper` (openai-whisper),
`whisper-cli` (whisper.cpp), or `mlx_whisper` (Apple Silicon).

Each script checks its own dependencies and prints exact install commands on
failure. If a dependency is missing, show the user the install command and ask
before installing anything on their machine.

## Workflow

Work inside a scratch directory, e.g. `/tmp/video-analysis/<job-name>/`.

### Step 1 — Acquire the video

```bash
bash scripts/fetch_video.sh "<url-or-local-path>" <workdir>
```

Handles both URLs (via yt-dlp, with platform-specific flags) and local paths.
Also downloads captions/subtitles when the platform provides them (saves a
whole transcription step). On success it prints the resolved video path and a
`metadata.json`.

Douyin and RedNote links often fail on the first try — this is expected, not a
dead end. Read `references/sources.md` for the per-platform fallback ladder
before telling the user it can't be done.

### Step 2 — Probe and plan

```bash
bash scripts/probe.sh <video-file>
```

Prints duration, resolution, fps, audio info, and a suggested extraction tier:

| Tier | Duration | Frame strategy |
|------|----------|----------------|
| short | < 4 min | 1 frame every 2–3 s, read individually |
| medium | 4–20 min | scene-change keyframes + 1 frame/10 s, read as 3×3 grids |
| long | > 20 min | scene-change keyframes only + 1 frame/30 s, read as 3×3 grids |

The tier controls token cost. Follow the script's suggestion unless the user
asks for finer detail on a specific time range.

### Step 3 — Extract frames and transcript (both, always)

Default analysis depth is **full**: frames AND transcript, every time. Visual
content (on-screen text, demos, charts, products, cooking steps, UI walkthroughs)
frequently carries knowledge that never appears in the audio.

```bash
bash scripts/extract_frames.sh <video-file> <workdir>/frames <tier>
bash scripts/get_transcript.sh <video-file> <workdir>
```

`extract_frames.sh` writes timestamp-named frames (`t0042.5.jpg` = 42.5 s) and,
for medium/long tiers, montage grids (`grid_001.jpg`) plus `grid_index.txt`
mapping each grid cell to its timestamp.

`get_transcript.sh` prefers captions downloaded in Step 1; otherwise extracts
audio and runs whichever Whisper variant is installed, with language
auto-detection (works for Chinese, English, mixed). Output: `transcript.txt`
with timestamps.

### Step 4 — Read and analyze

1. Read `transcript.txt` fully.
2. View the frames (grids for medium/long, individual frames for short).
   Cross-reference grid cells with `grid_index.txt` for timestamps.
3. If a segment seems important but under-sampled (dense on-screen text, a
   chart, a key demo moment), extract extra frames for just that range:
   `bash scripts/extract_frames.sh <video> <outdir> zoom <start-s> <end-s>`
4. Reconcile audio and visual: note things said but not shown, and shown but
   not said. The second category is what pure-transcript analysis misses —
   it deserves explicit attention in the notes.

### Step 5 — Write the notes

Read `references/note-template.md` and follow it exactly. Key rules:

- Write notes in the video's primary language unless the user asks otherwise
  (Chinese video → Chinese notes, 中文视频输出中文笔记).
- Timestamps in `[mm:ss]` format so the user can jump back into the video.
- Always include the final **Prompt-Ready Distillation** section — the user
  frequently repurposes these notes as system-prompt material, and that
  section must stand alone with zero references to "the video".
- Save the notes as a `.md` file named after the video title, and deliver the
  file to the user (don't only print to chat).

### Step 6 — Clean up

Ask before deleting the scratch directory — the user may want the frames or
transcript. Offer to keep `transcript.txt` alongside the notes.

## Multi-video and batch requests

For multiple URLs, run the full pipeline per video and write one notes file
each, then a short comparison/index note if the user asked for synthesis.
Process sequentially; frame extraction is disk-heavy.

## When things fail

Read `references/sources.md` — it has the fallback ladder per platform
(cookies, share-link expansion, manual download → treat as local file) and
common ffmpeg/whisper errors. Report the specific failing step and the exact
error to the user; never silently degrade to guessing content.
