#!/usr/bin/env bash
# Transcribe every voiceover clip in a folder to word-level timings, one folder per clip.
#
#   transcribe_clips.sh <clips_dir> <out_dir> [language=hi] [model=small]
#
# Writes <out_dir>/<clip stem>/transcript.json for tighten_voiceover.py.
# Use a multilingual model (small, medium, large-v3) for non-English speech: the *.en models
# translate into English instead. Whisper often garbles spelling (Hindi especially); the
# timings are what matter, the caption text comes from the script.
set -euo pipefail
clips=${1:?clips dir}; out=${2:?out dir}; lang=${3:-hi}; model=${4:-small}
mkdir -p "$out"
for f in "$clips"/*; do
  lower=$(printf "%s" "$f" | tr "[:upper:]" "[:lower:]")
  case "$lower" in *.mp3|*.wav|*.m4a|*.aac|*.flac|*.ogg) ;; *) continue ;; esac
  stem=$(basename "${f%.*}")
  mkdir -p "$out/$stem"
  if npx --yes hyperframes transcribe "$f" -d "$out/$stem" -m "$model" -l "$lang" --engine whisper --json \
      > "$out/$stem.json" 2> "$out/$stem.err"; then
    echo "ok   $stem"
  else
    echo "FAIL $stem (see $out/$stem.err)"
  fi
done
