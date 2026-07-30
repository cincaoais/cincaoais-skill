# Platform Playbook & Fallback Ladders

Read this when a download fails or before starting on Douyin/RedNote links.
General rule for every platform: the single most effective fix is updating
yt-dlp (`yt-dlp -U` or `pip install -U yt-dlp`) — CN-platform extractors break
and get fixed on a weekly cadence.

## YouTube (youtube.com, youtu.be)

- Most reliable platform. Auto-captions exist for nearly everything → the
  transcript step is usually free (no Whisper needed).
- Age-restricted / member content: `--cookies-from-browser chrome`.
- For very long videos, consider asking the user whether they want the whole
  thing or a time range; a 2-hour video at full analysis is expensive.

## TikTok (tiktok.com)

- Works with plain yt-dlp including share short-links (vm.tiktok.com).
- No usable captions in most regions → expect the Whisper path.
- Downloaded video may carry a moving watermark; harmless for analysis.

## Douyin 抖音 (douyin.com, v.douyin.com)

Fallback ladder, in order:
1. Strip share clutter. Users paste text like
   `8.63 fJx:/ 复制打开抖音，看看...  https://v.douyin.com/xxxx/`.
   Extract only the URL before running the script.
2. Plain yt-dlp (the script's attempt 1). Short links redirect fine.
3. `yt-dlp -U`, retry.
4. Cookies: `--cookies-from-browser chrome` with a browser session that has
   visited douyin.com (login not always required, but a session cookie often
   is). The fetch script tries this automatically.
5. If still failing: ask the user to save the video via the Douyin app's
   share → 保存到相册 (works when the creator allows downloads), then provide
   the local path.

Notes: Douyin videos are usually < 3 min → tier `short`. Speech is often fast
zh with background music; if Whisper output looks garbled, retry with
`--model medium` and language forced to zh.

## RedNote / Xiaohongshu 小红书 (xiaohongshu.com, xhslink.com)

The least reliable platform — set expectations with the user early.
Fallback ladder:
1. Expand short links first: xhslink.com share URLs sometimes fail in yt-dlp
   while the full xiaohongshu.com/explore/... URL works. Get the redirect
   target (`curl -sIL <url> | grep -i location`, or open in browser) and retry
   with that.
2. `yt-dlp -U`, retry. Extractor support for XHS comes and goes by version.
3. Cookies from a logged-in browser: `--cookies-from-browser chrome`.
4. Manual: user saves the video from the app (share → 保存, when permitted) or
   via screen recording as last resort, then provides the local path.

Notes: Many XHS posts are image carousels, not videos. If yt-dlp reports no
video formats, ask the user whether the post is a video — if it's images,
download the images instead and analyze them directly (no pipeline needed).

## Bilibili (bilibili.com, b23.tv)

- yt-dlp works; 1080p+ often needs `--cookies-from-browser` with a logged-in
  session, but ≤720p (all we need) usually works anonymously.
- Multi-part videos (分P): `--no-playlist` grabs only the linked part; ask the
  user if they want all parts.
- CC subtitles exist on some videos → check for captions before Whisper.

## Local files

- Any container ffmpeg reads is fine (.mp4 .mov .mkv .webm .avi .flv .ts).
- If ffprobe fails on a file the user insists is video, it may be HEVC in a
  broken container — try remuxing: `ffmpeg -i in.x -c copy out.mp4`.

## Transcription troubleshooting

- Wrong language detected → force it: `WHISPER_LANG=zh bash scripts/get_transcript.sh ...`
  — common for zh videos with English intro music lyrics.
- Model size is set with `WHISPER_MODEL` (default `small`), e.g.
  `WHISPER_MODEL=medium bash scripts/get_transcript.sh ...`. Both env vars work
  across the faster-whisper and openai-whisper paths.
- Note: the `faster-whisper` PyPI package is a LIBRARY with no console script.
  Install it with `pip`, not `pipx` — the script imports it from Python directly.
- Heavy BGM drowning speech → extract audio with a highpass filter first:
  `ffmpeg -i video.mp4 -vn -ac 1 -ar 16000 -af "highpass=f=200,lowpass=f=3000" audio16k.wav`
- Model too slow on user's machine → `--model base` is 4-5× faster than
  `small` and usually adequate for clear speech; go `medium` only when
  accuracy visibly suffers.

## Ethics & limits

Only fetch content the user can legitimately access. Don't help bypass
paywalls or DRM. Region-locked and login-walled content is fetched with the
user's own credentials/cookies, which is fine — that's their access.
