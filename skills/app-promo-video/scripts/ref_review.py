#!/usr/bin/env python3
"""Low-token review of a reference video: cuts, shot lengths, gridded contact sheets, motion strips.

    python3 ref_review.py <video> <out_dir> [--threshold 0.3] [--max-sheets 3]
    python3 ref_review.py <video> <out_dir> --strip 12.0 13.2 [--frames 8]

Overview mode writes, into <out_dir>:
  summary.md     size, fps, length, hard-cut times and rate, and a table mapping each tile to its time
  shots.json     the same data as JSON
  sheet-N.png    frames sampled evenly through the video (every ~2-4 s), 4 x 3 tiles per sheet, 480 px
                 wide each, with a 10% grid (every line = 10% of width/height) for measuring positions and
                 sizes; never more than --max-sheets sheets (36 tiles)
Hard cuts are found with ffmpeg scene detection and listed with times; zooms, whips and pushes inside
a shot don't count as cuts, which is why the sheets sample time rather than shots.

Strip mode writes strip-<a>-<b>.png: --frames evenly spaced frames between two times, 4 per row,
480 px wide each, with the same 10% grid. Use it on 2-3 key moves to read zoom amount, travel,
easing (where the frames bunch up) and how text enters.

Read summary.md first, then the sheets, then strips only for the moves worth copying the grammar of.
Never read full-resolution frames unless a sheet can't answer the question. Needs ffmpeg/ffprobe.
"""
import argparse
import json
import re
import statistics
import subprocess
import tempfile
from pathlib import Path

GRID = "drawgrid=w=iw/10:h=ih/10:t=1:c=red@0.45"


def probe(video):
    out = subprocess.check_output(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                                   "stream=width,height,r_frame_rate:format=duration", "-of", "json", str(video)])
    d = json.loads(out)
    st = d["streams"][0]
    num, den = st["r_frame_rate"].split("/")
    return int(st["width"]), int(st["height"]), round(int(num) / int(den), 3), float(d["format"]["duration"])


def cuts(video, threshold):
    err = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(video), "-an", "-vf",
                          f"scale=320:-2,select='gt(scene,{threshold})',showinfo", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    return [float(t) for t in re.findall(r"pts_time:([\d.]+)", err)]


def frame(video, t, out, width, extra=""):
    vf = f"scale={width}:-2,{GRID}" + (f",{extra}" if extra else "")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.3f}", "-i", str(video), "-frames:v", "1",
                    "-vf", vf, str(out)], check=True)


def tile(frames, cols, rows, out):
    with tempfile.TemporaryDirectory() as tmp:
        for i, f in enumerate(frames):
            Path(f).rename(Path(tmp) / f"f{i:03d}.png")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", "1", "-i", str(Path(tmp) / "f%03d.png"),
                        "-vf", f"tile={cols}x{rows}:padding=4:color=black", "-frames:v", "1", str(out)], check=True)


def overview(a):
    video, out = Path(a.video), Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    w, h, fps, dur = probe(video)
    cs = [c for c in cuts(video, a.threshold) if 0.1 < c < dur - 0.1]
    bounds = [0.0] + cs + [dur]
    shots = [{"index": i + 1, "start": round(s, 2), "length": round(e - s, 2)}
             for i, (s, e) in enumerate(zip(bounds, bounds[1:])) if e - s > 0.05]
    lengths = [s["length"] for s in shots]
    # Product videos change shots with moves (whips, zooms, pushes) more than hard cuts, so tiles
    # sample the timeline evenly (about every 2-4 s) instead of one per detected shot.
    cap = 12 * a.max_sheets
    n = min(cap, max(12, int(dur // 2)))
    times = [round(dur * (i + 0.5) / n, 2) for i in range(n)]

    def shot_at(t):
        return next(s["index"] for s in reversed(shots) if s["start"] <= t)

    picked = [{"time": t, "shot": shot_at(t)} for t in times]
    with tempfile.TemporaryDirectory() as tmp:
        files = []
        for k, p_ in enumerate(picked):
            f = Path(tmp) / f"s{k:03d}.png"
            frame(video, p_["time"], f, 480)
            files.append(f)
        sheets = []
        for k in range(0, len(files), 12):
            sheet = out / f"sheet-{k // 12 + 1}.png"
            tile(files[k:k + 12], 4, 3, sheet)
            sheets.append(sheet.name)
    summary = {
        "video": video.name, "width": w, "height": h, "fps": fps, "duration": round(dur, 2),
        "hard_cuts": [round(c, 2) for c in cs], "shots": len(shots), "cuts_per_minute": round(len(cs) / dur * 60, 1),
        "shot_length": {"mean": round(statistics.mean(lengths), 2), "median": round(statistics.median(lengths), 2),
                        "min": min(lengths), "max": max(lengths)},
        "sheets": sheets, "tiles": picked, "shot_list": shots,
    }
    (out / "shots.json").write_text(json.dumps(summary, indent=1))
    lines = [f"# Reference: {video.name}", "",
             f"- {w}x{h} @ {fps} fps, {dur:.1f} s",
             f"- {len(cs)} hard cuts ({summary['cuts_per_minute']}/min) at: {', '.join(f'{c:.1f}' for c in cs) or 'none'}",
             f"- between hard cuts: mean {summary['shot_length']['mean']} s, median {summary['shot_length']['median']} s, "
             f"range {min(lengths)}-{max(lengths)} s (moves/whips inside a shot are not counted)",
             f"- sheets: {', '.join(sheets)} — {n} tiles every {dur / n:.1f} s, 4 x 3 per sheet, left to right, "
             "top to bottom; red grid = 10% of width/height", "",
             "| tile | time | shot |", "|---|---|---|"]
    lines += [f"| {k + 1} | {p_['time']} | {p_['shot']} |" for k, p_ in enumerate(picked)]
    (out / "summary.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines[:6]))
    print(f"wrote {out / 'summary.md'}, {len(sheets)} sheet(s)")


def strip(a):
    video, out = Path(a.video), Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    t0, t1 = a.strip
    n = a.frames
    with tempfile.TemporaryDirectory() as tmp:
        files = []
        for i in range(n):
            t = t0 + (t1 - t0) * i / (n - 1)
            f = Path(tmp) / f"t{i:03d}.png"
            frame(video, t, f, 480)
            files.append(f)
        name = out / f"strip-{t0:g}-{t1:g}.png"
        cols = min(4, n)
        tile(files, cols, -(-n // cols), name)
    step = (t1 - t0) / (n - 1)
    print(f"{name}  ({n} frames, {step:.3f} s apart, from {t0:g} s)")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("video")
    ap.add_argument("out")
    ap.add_argument("--threshold", type=float, default=0.3, help="scene-change sensitivity (lower finds more cuts)")
    ap.add_argument("--max-sheets", type=int, default=3)
    ap.add_argument("--strip", type=float, nargs=2, metavar=("START", "END"))
    ap.add_argument("--frames", type=int, default=8)
    a = ap.parse_args()
    strip(a) if a.strip else overview(a)


if __name__ == "__main__":
    main()
