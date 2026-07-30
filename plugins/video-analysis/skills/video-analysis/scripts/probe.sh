#!/usr/bin/env bash
# probe.sh — print video metadata and suggest an extraction tier.
# Usage: probe.sh <video-file>
set -euo pipefail

VIDEO="${1:?Usage: probe.sh <video-file>}"
command -v ffprobe >/dev/null 2>&1 || { echo "ERROR: ffprobe not found (install ffmpeg)" >&2; exit 1; }

DURATION="$(ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 "$VIDEO")"
DURATION="${DURATION%.*}"; DURATION="${DURATION:-0}"

WIDTH="$(ffprobe -v error -select_streams v:0 -show_entries stream=width  -of default=nw=1:nk=1 "$VIDEO" || echo "?")"
HEIGHT="$(ffprobe -v error -select_streams v:0 -show_entries stream=height -of default=nw=1:nk=1 "$VIDEO" || echo "?")"
FPS="$(ffprobe -v error -select_streams v:0 -show_entries stream=avg_frame_rate -of default=nw=1:nk=1 "$VIDEO" || echo "?")"
HAS_AUDIO="$(ffprobe -v error -select_streams a -show_entries stream=codec_type -of default=nw=1:nk=1 "$VIDEO" | head -n1)"

MINS=$((DURATION / 60)); SECS=$((DURATION % 60))
echo "duration_seconds=$DURATION (${MINS}m${SECS}s)"
echo "resolution=${WIDTH}x${HEIGHT}"
echo "fps=$FPS"
echo "has_audio=$([ -n "$HAS_AUDIO" ] && echo yes || echo NO_AUDIO_STREAM)"

if   [ "$DURATION" -lt 240 ];  then TIER="short"
elif [ "$DURATION" -le 1200 ]; then TIER="medium"
else TIER="long"; fi
echo "suggested_tier=$TIER"

case "$TIER" in
  short)  EST=$((DURATION / 3 + 1)); echo "estimate: ~$EST individual frames" ;;
  medium) EST=$((DURATION / 10 + 1)); echo "estimate: ~$EST frames -> ~$(( (EST+8)/9 )) grids + scene keyframes" ;;
  long)   EST=$((DURATION / 30 + 1)); echo "estimate: ~$EST frames -> ~$(( (EST+8)/9 )) grids + scene keyframes" ;;
esac
if [ -z "$HAS_AUDIO" ]; then
  echo "NOTE: no audio stream — skip transcription, analysis will be visual-only."
fi
