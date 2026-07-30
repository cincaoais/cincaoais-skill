#!/usr/bin/env bash
# extract_frames.sh — extract timestamp-named frames, scene keyframes, and montage grids.
# Usage:
#   extract_frames.sh <video> <outdir> short|medium|long
#   extract_frames.sh <video> <outdir> zoom <start-seconds> <end-seconds>
#
# Output:
#   <outdir>/tSSSS.S.jpg           interval frames (name = timestamp in seconds)
#   <outdir>/scene_tSSSS.S.jpg     scene-change keyframes (medium/long)
#   <outdir>/grid_NNN.jpg          3x3 montages (medium/long)
#   <outdir>/grid_index.txt        grid cell -> timestamp map (row-major)
set -euo pipefail

VIDEO="${1:?Usage: extract_frames.sh <video> <outdir> <tier>}"
OUTDIR="${2:?Usage: extract_frames.sh <video> <outdir> <tier>}"
TIER="${3:?tier must be one of: short|medium|long|zoom}"
mkdir -p "$OUTDIR"

command -v ffmpeg >/dev/null 2>&1 || { echo "ERROR: ffmpeg not found" >&2; exit 1; }

DURATION="$(ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 "$VIDEO")"
DURATION="${DURATION%.*}"; DURATION="${DURATION:-0}"

# Rename ffmpeg's sequential frames to timestamp names given a known interval.
rename_to_timestamps() { # $1=prefix-glob-dir $2=interval $3=offset $4=newprefix
  local dir="$1" interval="$2" offset="$3" prefix="$4" i=0 ts f
  for f in "$dir"/_seq_*.jpg; do
    [ -e "$f" ] || continue
    ts=$(python3 -c "print(f'{$offset + $i * $interval:.1f}')")
    mv "$f" "$dir/${prefix}t${ts}.jpg"
    i=$((i+1))
  done
}

extract_interval() { # $1=interval-seconds $2=scale-width $3=offset $4=end("" = full)
  local interval="$1" width="$2" offset="${3:-0}" end="${4:-}"
  local seek=() dur=()
  [ "$offset" != "0" ] && seek=(-ss "$offset")
  [ -n "$end" ] && dur=(-t "$(python3 -c "print($end - $offset)")")
  ffmpeg -v error "${seek[@]}" -i "$VIDEO" "${dur[@]}" \
    -vf "fps=1/${interval},scale=${width}:-2" -q:v 4 \
    "$OUTDIR/_seq_%05d.jpg"
  rename_to_timestamps "$OUTDIR" "$interval" "$offset" ""
}

extract_scenes() { # scene-change keyframes with real timestamps from ffmpeg showinfo
  local thresh="${1:-0.30}" log="$OUTDIR/_scene_log.txt"
  local i=0 f ts target k
  # Do NOT use metadata=print:file=<path> here. That path sits inside the
  # filtergraph string, which ffmpeg parses itself: ':' begins a new filter
  # option, and MSYS/Git-Bash does not rewrite /c/Users/... to C:/Users/...
  # inside a quoted argument. On Windows that fails with "Could not open ...".
  # showinfo prints pts_time to stderr instead — no path, portable everywhere.
  ffmpeg -hide_banner -v info -i "$VIDEO" \
    -vf "select='gt(scene,${thresh})',showinfo,scale=640:-2" \
    -vsync vfr -q:v 4 "$OUTDIR/_scene_%05d.jpg" 2> "$log" || true
  # pts_time lines pair 1:1 with emitted frames
  mapfile -t TIMES < <(grep -o 'pts_time:[0-9.]*' "$log" | cut -d: -f2)
  for f in "$OUTDIR"/_scene_*.jpg; do
    [ -e "$f" ] || continue
    ts="${TIMES[$i]:-0}"
    # Rounding to 0.1s makes collisions possible on rapid cuts; suffix rather
    # than overwrite, otherwise frames are silently lost.
    target="$(printf '%s/scene_t%.1f.jpg' "$OUTDIR" "$ts")"
    k=1
    while [ -e "$target" ]; do
      target="$(printf '%s/scene_t%.1f_%d.jpg' "$OUTDIR" "$ts" "$k")"
      k=$((k+1))
    done
    mv "$f" "$target"
    i=$((i+1))
  done
  rm -f "$log"
}

make_grids() { # tile interval frames into 3x3 montages; write grid_index.txt
  local files=() f n=0 g=1
  # Sort numerically on the timestamp in the BASENAME. The previous
  # `sort -t t -k2 -g` split the whole PATH on the letter 't', so any 't' in a
  # parent directory name (/tmp/..., .../scratchpad/...) shifted the key field
  # and the order silently degraded to lexicographic:
  #   t0.0, t1020.0, t1050.0, ..., t120.0, t1200.0, ...
  # which scrambles every grid while grid_index.txt still looks plausible.
  while IFS= read -r f; do files+=("$f"); done < <(
    for f in "$OUTDIR"/t*.jpg; do
      [ -e "$f" ] || continue
      b="$(basename "$f" .jpg)"
      printf '%s\t%s\n' "${b#t}" "$f"
    done | sort -g -k1,1 | cut -f2-
  )
  [ "${#files[@]}" -eq 0 ] && return 0
  : > "$OUTDIR/grid_index.txt"
  local batch=()
  for f in "${files[@]}"; do
    batch+=("$f"); n=$((n+1))
    if [ "${#batch[@]}" -eq 9 ] || [ "$n" -eq "${#files[@]}" ]; then
      local gid; gid=$(printf '%03d' "$g")
      local inputs=() b2
      for b2 in "${batch[@]}"; do inputs+=(-i "$b2"); done
      ffmpeg -v error "${inputs[@]}" \
        -filter_complex "concat=n=${#batch[@]}:v=1:a=0 [t]; [t] scale=426:-2, tile=3x3" \
        -frames:v 1 -q:v 4 "$OUTDIR/grid_${gid}.jpg"
      {
        echo "grid_${gid}.jpg (row-major, cell -> timestamp seconds):"
        local c=1 b
        for b in "${batch[@]}"; do
          echo "  cell $c: $(basename "$b" .jpg | sed 's/^t//')s"
          c=$((c+1))
        done
      } >> "$OUTDIR/grid_index.txt"
      batch=(); g=$((g+1))
    fi
  done
  echo "grids written: $((g-1)), index: $OUTDIR/grid_index.txt"
}

case "$TIER" in
  short)
    extract_interval 3 640 0 ""
    ;;
  medium)
    extract_interval 10 426 0 ""
    extract_scenes 0.30
    make_grids
    ;;
  long)
    extract_interval 30 426 0 ""
    extract_scenes 0.35
    make_grids
    ;;
  zoom)
    START="${4:?zoom mode: extract_frames.sh <video> <outdir> zoom <start-s> <end-s>}"
    END="${5:?zoom mode: extract_frames.sh <video> <outdir> zoom <start-s> <end-s>}"
    ffmpeg -v error -ss "$START" -i "$VIDEO" -t "$(python3 -c "print($END - $START)")" \
      -vf "fps=1,scale=800:-2" -q:v 3 "$OUTDIR/_seq_%05d.jpg"
    rename_to_timestamps "$OUTDIR" 1 "$START" "zoom_"
    ;;
  *)
    echo "ERROR: unknown tier '$TIER'" >&2; exit 1 ;;
esac

echo "frames in $OUTDIR: $(ls "$OUTDIR" | grep -c '\.jpg$' || true)"
