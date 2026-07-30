#!/usr/bin/env bash
# get_transcript.sh — produce <workdir>/transcript.txt with [mm:ss] timestamps.
# Priority: existing captions (.vtt/.srt in workdir) > local Whisper transcription.
# Usage: get_transcript.sh <video-file> <workdir>
set -euo pipefail

VIDEO="${1:?Usage: get_transcript.sh <video-file> <workdir>}"
WORKDIR="${2:?Usage: get_transcript.sh <video-file> <workdir>}"
OUT="$WORKDIR/transcript.txt"
mkdir -p "$WORKDIR"

# ---------- 1. Captions already downloaded? ----------
CAP="$(find "$WORKDIR" -maxdepth 1 \( -name '*.vtt' -o -name '*.srt' \) | sort | head -n1)"
if [ -n "$CAP" ]; then
  echo "Using captions: $CAP"
  python3 - "$CAP" "$OUT" <<'PY'
import re, sys
src, out = sys.argv[1], sys.argv[2]
text = open(src, encoding="utf-8", errors="replace").read()
lines, last = [], None
ts_re = re.compile(r"(\d+):(\d+):(\d+)[.,]\d+\s*-->")
for raw in text.splitlines():
    m = ts_re.match(raw.strip())
    if m:
        h, mnt, s = map(int, m.groups())
        cur = f"[{h*60+mnt:02d}:{s:02d}]"
        last = cur if cur != last else None
        continue
    line = re.sub(r"<[^>]+>", "", raw).strip()
    if not line or line.isdigit() or line.startswith(("WEBVTT", "NOTE", "Kind:", "Language:")):
        continue
    if lines and lines[-1].split("] ", 1)[-1] == line:  # dedupe rolling captions
        continue
    lines.append(f"{last + ' ' if last else ''}{line}")
    last = None
open(out, "w", encoding="utf-8").write("\n".join(lines) + "\n")
print(f"transcript: {out} ({len(lines)} lines)")
PY
  exit 0
fi

# ---------- 2. Audio present? ----------
HAS_AUDIO="$(ffprobe -v error -select_streams a -show_entries stream=codec_type -of default=nw=1:nk=1 "$VIDEO" | head -n1)"
if [ -z "$HAS_AUDIO" ]; then
  echo "NO_AUDIO_STREAM: video has no audio; skipping transcription." | tee "$OUT"
  exit 0
fi

WAV="$WORKDIR/audio16k.wav"
echo "Extracting audio..."
ffmpeg -v error -y -i "$VIDEO" -vn -ac 1 -ar 16000 "$WAV"

# ---------- 3. Whichever Whisper is installed ----------
WHISPER_MODEL="${WHISPER_MODEL:-small}"

if command -v faster-whisper >/dev/null 2>&1; then
  echo "Transcribing with faster-whisper..."
  faster-whisper "$WAV" --model "$WHISPER_MODEL" --output_dir "$WORKDIR" --output_format srt
  mv "$WORKDIR/$(basename "$WAV" .wav).srt" "$WORKDIR/whisper.srt" 2>/dev/null || true
elif PY="$(command -v python3 || command -v python || true)" && [ -n "$PY" ] \
     && "$PY" -c 'import faster_whisper' >/dev/null 2>&1; then
  # The faster-whisper PyPI package ships NO console script — verified on 1.2.1,
  # where importlib.metadata reports an empty entry_points list. So the
  # `command -v faster-whisper` branch above never matches on a normal
  # `pip install faster-whisper`, and the script used to fall through to
  # "no transcription tool found" while a perfectly usable library sat installed.
  # Drive the library directly instead.
  echo "Transcribing with faster-whisper (Python library, model: $WHISPER_MODEL)..."
  "$PY" - "$WAV" "$WORKDIR/whisper.srt" "$WHISPER_MODEL" "${WHISPER_LANG:-}" <<'PYEOF'
import sys
from faster_whisper import WhisperModel

audio, out, model_name = sys.argv[1], sys.argv[2], sys.argv[3]
lang = (sys.argv[4] or None) if len(sys.argv) > 4 else None

def ts(sec):
    ms = int(round(sec * 1000))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

model = WhisperModel(model_name, device="cpu", compute_type="int8")
segments, info = model.transcribe(audio, language=lang, vad_filter=True, beam_size=5)
print(f"detected language: {info.language} (p={info.language_probability:.2f}), "
      f"duration: {info.duration:.0f}s", file=sys.stderr)

n = 0
with open(out, "w", encoding="utf-8") as fh:
    for seg in segments:                      # generator: transcription streams here
        text = seg.text.strip()
        if not text:
            continue
        n += 1
        fh.write(f"{n}\n{ts(seg.start)} --> {ts(seg.end)}\n{text}\n\n")
        if n % 50 == 0:
            print(f"  ...{n} segments ({seg.end:.0f}s)", file=sys.stderr)
print(f"wrote {out} ({n} segments)", file=sys.stderr)
PYEOF
elif command -v whisper >/dev/null 2>&1; then
  echo "Transcribing with openai-whisper (model: $WHISPER_MODEL)..."
  whisper "$WAV" --model "$WHISPER_MODEL" --output_dir "$WORKDIR" --output_format srt --verbose False
  mv "$WORKDIR/$(basename "$WAV" .wav).srt" "$WORKDIR/whisper.srt" 2>/dev/null || true
elif command -v whisper-cli >/dev/null 2>&1; then
  echo "Transcribing with whisper.cpp..."
  MODEL="${WHISPER_CPP_MODEL:-$HOME/.cache/whisper.cpp/ggml-small.bin}"
  [ -f "$MODEL" ] || { echo "ERROR: whisper.cpp model not found at $MODEL. Download a ggml model or set WHISPER_CPP_MODEL." >&2; exit 1; }
  whisper-cli -m "$MODEL" -f "$WAV" -osrt -of "$WORKDIR/whisper"
elif command -v mlx_whisper >/dev/null 2>&1; then
  echo "Transcribing with mlx_whisper (Apple Silicon)..."
  mlx_whisper "$WAV" --output-dir "$WORKDIR" --output-format srt
  mv "$WORKDIR/$(basename "$WAV" .wav).srt" "$WORKDIR/whisper.srt" 2>/dev/null || true
else
  cat >&2 <<'EOF'
ERROR: no transcription tool found and no captions available.
Install ONE of (first is recommended):
  pip install faster-whisper         # fast, CPU-friendly — LIBRARY ONLY, no CLI;
                                     # this script drives it via Python directly.
                                     # Do NOT use pipx: it installs console
                                     # scripts, and this package ships none.
  pipx install openai-whisper        # reference implementation (has a CLI)
  brew install whisper-cpp           # mac, then download a ggml model
  pipx install mlx-whisper           # Apple Silicon GPU
Then re-run this script.
Override the model size with WHISPER_MODEL=medium (default: small).
EOF
  exit 3
fi

SRT="$(find "$WORKDIR" -maxdepth 1 -name 'whisper.srt' | head -n1)"
[ -z "$SRT" ] && SRT="$(find "$WORKDIR" -maxdepth 1 -name '*.srt' ! -name 'video*' | head -n1)"
[ -z "$SRT" ] && { echo "ERROR: transcription produced no .srt output" >&2; exit 4; }
exec bash "$0" "$VIDEO" "$WORKDIR"   # re-run: caption branch will now pick up the .srt
