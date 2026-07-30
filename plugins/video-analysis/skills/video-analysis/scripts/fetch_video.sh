#!/usr/bin/env bash
# fetch_video.sh — acquire a video from a URL or local path into a workdir.
# Usage: fetch_video.sh "<url-or-path>" <workdir>
# On success prints: VIDEO_PATH=<path> and writes <workdir>/metadata.json
# Also downloads captions when available (*.vtt / *.srt in workdir).
set -uo pipefail

INPUT="${1:?Usage: fetch_video.sh <url-or-path> <workdir>}"
WORKDIR="${2:?Usage: fetch_video.sh <url-or-path> <workdir>}"
mkdir -p "$WORKDIR"

die() { echo "ERROR: $*" >&2; exit 1; }

command -v ffprobe >/dev/null 2>&1 || die "ffprobe not found. Install: (mac) brew install ffmpeg | (debian/ubuntu) sudo apt install ffmpeg"

# ---------- Local file ----------
if [ -e "$INPUT" ]; then
  ffprobe -v error -show_format "$INPUT" >/dev/null 2>&1 \
    || die "File exists but is not a readable video: $INPUT"
  # Use the file in place; no copy needed.
  ABS="$(cd "$(dirname "$INPUT")" && pwd)/$(basename "$INPUT")"
  printf '{"source":"local","input":"%s"}\n' "$ABS" > "$WORKDIR/metadata.json"
  echo "VIDEO_PATH=$ABS"
  exit 0
fi

# ---------- URL ----------
case "$INPUT" in
  http://*|https://*) : ;;
  *) die "Input is neither an existing file nor a URL: $INPUT" ;;
esac

command -v yt-dlp >/dev/null 2>&1 \
  || die "yt-dlp not found. Install: pipx install yt-dlp  (or: pip install -U yt-dlp / brew install yt-dlp)"

PLATFORM="generic"
case "$INPUT" in
  *douyin.com*)                       PLATFORM="douyin" ;;
  *xiaohongshu.com*|*xhslink.com*)    PLATFORM="rednote" ;;
  *youtube.com*|*youtu.be*)           PLATFORM="youtube" ;;
  *tiktok.com*)                       PLATFORM="tiktok" ;;
  *bilibili.com*|*b23.tv*)            PLATFORM="bilibili" ;;
esac
echo "Platform detected: $PLATFORM"

# Common flags: cap at 720p (frames don't need more), prefer mp4,
# grab manual+auto subtitles in original language(s) + en/zh.
COMMON_ARGS=(
  -f "bv*[height<=720]+ba/b[height<=720]/b"
  --merge-output-format mp4
  --write-subs --write-auto-subs
  --sub-langs "en.*,zh.*,-live_chat"
  --no-playlist
  -o "$WORKDIR/video.%(ext)s"
  --print-to-file "%(.{id,title,uploader,duration,webpage_url,upload_date})j" "$WORKDIR/metadata.json"
)

run_ytdlp() {
  yt-dlp "${COMMON_ARGS[@]}" "$@" "$INPUT"
}

echo "Attempt 1: plain yt-dlp..."
if ! run_ytdlp; then
  echo ""
  echo "Attempt 1 failed."
  if [ "$PLATFORM" = "douyin" ] || [ "$PLATFORM" = "rednote" ] || [ "$PLATFORM" = "bilibili" ]; then
    echo "Attempt 2: retrying with browser cookies (needed for many CN platforms)..."
    for BROWSER in chrome edge firefox safari; do
      echo "  trying --cookies-from-browser $BROWSER"
      if run_ytdlp --cookies-from-browser "$BROWSER" 2>/dev/null; then
        break 2>/dev/null || true
      fi
    done
  fi
fi

VIDEO_FILE="$(find "$WORKDIR" -maxdepth 1 -name 'video.*' \
  ! -name '*.vtt' ! -name '*.srt' ! -name '*.json' ! -name '*.part' | head -n1)"

if [ -z "$VIDEO_FILE" ]; then
  echo "" >&2
  echo "DOWNLOAD FAILED for platform: $PLATFORM" >&2
  echo "Next steps — read references/sources.md for the full fallback ladder." >&2
  case "$PLATFORM" in
    rednote)
      echo "RedNote/小红书 quick fallback: yt-dlp support is unreliable for this site." >&2
      echo "  1. Update yt-dlp first: yt-dlp -U" >&2
      echo "  2. If the link is a share short-link (xhslink.com), open it in a browser" >&2
      echo "     and retry with the full xiaohongshu.com URL it redirects to." >&2
      echo "  3. Otherwise ask the user to save the video locally (share sheet ->" >&2
      echo "     save, or a downloader tool) and re-run this script with the local path." >&2
      ;;
    douyin)
      echo "Douyin/抖音 quick fallback:" >&2
      echo "  1. Update yt-dlp: yt-dlp -U (Douyin breaks often, fixes ship fast)" >&2
      echo "  2. Short links (v.douyin.com/xxxx) usually work; strip any extra share text." >&2
      echo "  3. Retry with cookies from a browser logged into douyin.com." >&2
      ;;
    *)
      echo "  1. Update yt-dlp: yt-dlp -U" >&2
      echo "  2. Retry with --cookies-from-browser chrome (age/region-locked content)" >&2
      ;;
  esac
  exit 2
fi

CAPS="$(find "$WORKDIR" -maxdepth 1 \( -name '*.vtt' -o -name '*.srt' \) | head -n3)"
[ -n "$CAPS" ] && echo "Captions downloaded:" && echo "$CAPS"

echo "VIDEO_PATH=$VIDEO_FILE"
