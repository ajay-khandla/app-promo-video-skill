#!/usr/bin/env bash
# Download a reference video (YouTube or any yt-dlp-supported link) for review only.
#
#   fetch_ref.sh <url> <out_dir>
#
# Gets at most 720p MP4 (enough to read layout and motion, a fraction of the size), plus the
# title/duration in <out_dir>/ref.info.txt. Ask the person before downloading, keep refs out of
# git and out of the render: they are studied for grammar, never reused as footage.
# Needs yt-dlp (brew install yt-dlp, or pipx install yt-dlp) and ffmpeg.
set -euo pipefail
url=${1:?url}; out=${2:?out dir}
if ! command -v yt-dlp >/dev/null 2>&1; then
  echo "yt-dlp is not installed. Install it with:  brew install yt-dlp   (or: pipx install yt-dlp)" >&2
  exit 2
fi
mkdir -p "$out"
yt-dlp --no-playlist -f "bv*[height<=720][ext=mp4]+ba[ext=m4a]/b[height<=720][ext=mp4]/b[height<=720]" \
  --merge-output-format mp4 -o "$out/ref.%(ext)s" \
  --print-to-file "%(title)s | %(duration_string)s | %(uploader)s | %(webpage_url)s" "$out/ref.info.txt" "$url"
ls -la "$out"
