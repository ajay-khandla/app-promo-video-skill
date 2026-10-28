#!/usr/bin/env bash
# Contact sheet of screenshots with a measuring grid, for reading zoom regions by eye.
#
#   grid_sheets.sh <out.png> <shot1.png> [shot2.png ...]     (up to ~4 per sheet reads well)
#
# Each screenshot is scaled to 1/3 with a thin red line every 100 source px and a thick
# blue line every 500 source px. Read a region off the sheet, multiply by 3, and pass it
# to cam()/ol()/tap() in source pixels. (Uses drawgrid only; drawtext is often missing
# from Homebrew ffmpeg builds.)
set -euo pipefail
out=${1:?out.png}; shift
tmp=$(mktemp -d)
args=(); i=0
for f in "$@"; do
  ffmpeg -v error -y -i "$f" -vf "drawgrid=w=100:h=100:t=2:c=red@0.3,drawgrid=w=500:h=500:t=6:c=blue@0.7,scale=iw/3:-1" "$tmp/$i.png"
  args+=(-i "$tmp/$i.png"); i=$((i+1))
done
if [ "$i" -eq 1 ]; then cp "$tmp/0.png" "$out"; else ffmpeg -v error -y "${args[@]}" -filter_complex "hstack=inputs=$i" "$out"; fi
rm -rf "$tmp"
echo "$out"
