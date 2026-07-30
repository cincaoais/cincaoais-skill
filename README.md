# claude-skills

A personal [Claude Code](https://claude.com/claude-code) plugin marketplace. Skills live in git,
so installing the marketplace once on each machine or account keeps them updated from a single
source of truth.

## Install

```bash
# once per machine / account
/plugin marketplace add <your-github-user>/claude-skills-marketplace

# then install what you want
/plugin install video-analysis@claude-skills
```

Updates land with:

```bash
/plugin marketplace update claude-skills
```

## Plugins

| Plugin | Version | What it does |
|---|---|---|
| `video-analysis` | 1.1.0 | Turns a video URL or local file into structured, timestamped knowledge notes |

### video-analysis

Decomposes a video into things a model can actually read — sampled frames, scene keyframes, and a
transcript — then writes notes from both. Invoked as `video-analysis:video-analysis`, or triggered
automatically when you paste a video link and ask for a summary.

Supports YouTube, TikTok, Douyin 抖音, RedNote/Xiaohongshu 小红书, Bilibili, anything else yt-dlp
handles, and local `.mp4/.mov/.mkv/.webm/.avi` files.

**Runtime dependencies** (the scripts check these and print install commands on failure):

| Tool | Required for | Install |
|---|---|---|
| `ffmpeg` / `ffprobe` | always | `winget install Gyan.FFmpeg` · `brew install ffmpeg` · `apt install ffmpeg` |
| `yt-dlp` | URLs only | `winget install yt-dlp.yt-dlp` · `pipx install yt-dlp` |
| `faster-whisper` | videos without captions | `pip install faster-whisper` — **`pip`, not `pipx`** (see below) |

Alternatives to `faster-whisper`: `openai-whisper`, `whisper.cpp` (`whisper-cli`), or `mlx-whisper`
on Apple Silicon.

**Environment variables**

| Variable | Default | Purpose |
|---|---|---|
| `WHISPER_MODEL` | `small` | Model size. `base` is 4–5× faster; `medium` when accuracy suffers. |
| `WHISPER_LANG` | auto-detect | Force a language, e.g. `zh`. Useful when intro music causes misdetection. |
| `WHISPER_CPP_MODEL` | `~/.cache/whisper.cpp/ggml-small.bin` | ggml model path for the whisper.cpp path. |

## Changes from the upstream skill (v1.1.0)

This vendors a third-party skill with three bug fixes applied. All were reproduced and verified
against a synthetic 300s clip with hard cuts plus a real 50-minute Douyin video.

1. **Scene detection failed on Windows** — `extract_frames.sh` passed a path to
   `metadata=print:file=` *inside* the ffmpeg filtergraph, where `:` is an option separator and
   MSYS/Git-Bash does not rewrite `/c/Users/...` to `C:/Users/...`. Produced zero keyframes and
   `Error initializing filters`. Now uses `showinfo`, which reports `pts_time` on stderr and needs
   no path at all.

2. **Montage grids were scrambled on every platform** — `make_grids` sorted with
   `sort -t t -k2 -g`, which splits the *entire path* on the letter `t`. Any `t` in a parent
   directory (`/tmp/...`, `.../scratchpad/...`) shifted the sort key and silently degraded the
   order to lexicographic: `0, 10, 100, 110, ..., 190, 20, 200, ...`. The grid index still looked
   plausible, so the corruption was easy to miss. Now sorts numerically on the basename.

3. **`faster-whisper` was never detected** — the PyPI package ships **no console script**
   (verified on 1.2.1: its `entry_points` list is empty), so `command -v faster-whisper` never
   matched and the script reported "no transcription tool found" while a working library sat
   installed. This is also why the old install hint `pipx install faster-whisper` was wrong —
   pipx installs console scripts, and this package has none. A new branch drives the library
   directly through Python.

Also fixed alongside these: scene keyframes rounding to 0.1s could collide on rapid cuts and
silently overwrite each other (310 frames in, 286 out); collisions now get a numeric suffix.

## Attribution

The `video-analysis` skill originated as a third-party `.skill` archive; the original author is
not recorded in the package. The fixes listed above are the only modifications. If you know the
upstream source, the bug fixes are worth sending back — bug 2 in particular affects every user on
every platform, not just Windows.

No license is asserted here, because the upstream skill shipped without one. Confirm the original
terms before making this repository public or redistributing it.
