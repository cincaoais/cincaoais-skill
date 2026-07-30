# claude-skills

A personal [Claude Code](https://claude.com/claude-code) plugin marketplace. Skills live in git,
so adding the marketplace once on each machine or account keeps them updated from a single source
of truth.

This repository is intended to be **private**.

## Install

```bash
# once per machine / account
/plugin marketplace add <your-github-user>/claude-skills-marketplace

# then install whichever you want
/plugin install video-analysis@claude-skills
/plugin install orchestrate@claude-skills
```

Pull updates with:

```bash
/plugin marketplace update claude-skills
```

## Plugins

| Plugin | Version | What it does |
|---|---|---|
| `video-analysis` | 1.1.0 | Turns a video URL or local file into structured, timestamped knowledge notes |
| `orchestrate` | 1.0.0 | Plan with the expensive model, fan execution out to parallel Sonnet subagents |
| `rnd` | 1.0.0 | General-purpose R&D investigation → structured report |
| `trading-rnd` | 1.0.0 | R&D pipeline specialised for US-stocks auto-trading topics |
| `system-builder` | 1.0.0 | Phase-gated build workflow: interview → R&D → plan → execute → review |

### Notes on individual plugins

**`system-builder` pairs with `orchestrate`.** It delegates research and coding fan-out through
orchestrate's delegate protocol. Claude Code plugins have no dependency field, so this is not
declared in the manifest — but system-builder degrades gracefully, falling back to
general-purpose subagents when orchestrate is absent. Install both for the intended behaviour.

**`rnd` and `trading-rnd` overlap deliberately.** `trading-rnd` is the specialised path for
trading topics; `rnd` handles everything else and defers to `trading-rnd` when it is installed.

**`video-analysis` needs external tools.** The scripts check for them and print install commands
on failure:

| Tool | Required for | Install |
|---|---|---|
| `ffmpeg` / `ffprobe` | always | `winget install Gyan.FFmpeg` · `brew install ffmpeg` · `apt install ffmpeg` |
| `yt-dlp` | URLs only | `winget install yt-dlp.yt-dlp` · `pipx install yt-dlp` |
| `faster-whisper` | videos without captions | `pip install faster-whisper` — **`pip`, not `pipx`** (see below) |

Alternatives to `faster-whisper`: `openai-whisper`, `whisper.cpp` (`whisper-cli`), or
`mlx-whisper` on Apple Silicon.

| Variable | Default | Purpose |
|---|---|---|
| `WHISPER_MODEL` | `small` | Model size. `base` is 4–5× faster; `medium` when accuracy suffers. |
| `WHISPER_LANG` | auto-detect | Force a language, e.g. `zh`, when intro music causes misdetection. |
| `WHISPER_CPP_MODEL` | `~/.cache/whisper.cpp/ggml-small.bin` | ggml model path for the whisper.cpp route. |

## video-analysis changes from upstream (v1.1.0)

Three bugs, each reproduced and verified against a synthetic 300s clip with hard cuts and a real
50-minute Douyin video.

1. **Scene detection failed on Windows.** `extract_frames.sh` passed a path to
   `metadata=print:file=` *inside* the ffmpeg filtergraph, where `:` is an option separator and
   MSYS/Git-Bash does not rewrite `/c/Users/...` to `C:/Users/...`. Result: zero keyframes and
   `Error initializing filters`. Now uses `showinfo`, which reports `pts_time` on stderr and
   needs no path.

2. **Montage grids were scrambled on every platform.** `make_grids` sorted with
   `sort -t t -k2 -g`, which splits the *entire path* on the letter `t`. Any `t` in a parent
   directory (`/tmp/...`, `.../scratchpad/...`) shifted the sort key and silently degraded the
   order to lexicographic: `0, 10, 100, 110, ..., 190, 20, 200, ...`. The grid index still looked
   plausible, so the corruption was easy to miss. Now sorts numerically on the basename.

3. **`faster-whisper` was never detected.** The PyPI package ships **no console script**
   (verified on 1.2.1 — its `entry_points` list is empty), so `command -v faster-whisper` never
   matched and the script reported "no transcription tool found" while a working library sat
   installed. This is also why the old hint `pipx install faster-whisper` was wrong: pipx installs
   console scripts and this package has none. A new branch drives the library through Python,
   with `WHISPER_MODEL` / `WHISPER_LANG` overrides.

Also fixed: scene keyframes rounding to 0.1s could collide on rapid cuts and silently overwrite
each other (310 frames in, 286 out). Collisions now get a numeric suffix.

## Attribution

`video-analysis` and `system-builder` originated as third-party `.skill` archives; neither
recorded an author or a license. The `video-analysis` fixes above are the only modifications to
that skill; `system-builder` is unmodified. `orchestrate`, `rnd`, and `trading-rnd` are personal.

No license is asserted, because the upstream skills shipped without one. Confirm the original
terms before making this repository public or redistributing it.

## Line endings

`.gitattributes` forces LF. Git for Windows defaults to `core.autocrlf=true`, which would rewrite
the shell scripts to CRLF on clone; bash then fails with `$'\r': command not found`, which is
awkward to diagnose because the files look correct in an editor.
