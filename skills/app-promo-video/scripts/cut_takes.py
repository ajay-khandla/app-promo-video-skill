"""Cut a long simulator take into one clip per scene, each event landing on its spoken word.

A clip is described by anchors [(film_t, take_t, play)]: at film time film_t the clip shows take time take_t,
plays `play` seconds of the take from there (the tap's animation), then holds that frame until the next anchor.
The first anchor's film_t is the clip's start. Screens are static between taps, so the jump from a held frame
to the next event is invisible.

    cut(take, anchors, end, out)   -> writes out (30 fps, 1206 x 2622, h264), skipped when unchanged
"""
import hashlib
import json
import subprocess
from pathlib import Path

FPS = 30


def pieces(anchors, end):
    out = []
    for i, (m, t, play) in enumerate(anchors):
        nxt = anchors[i + 1][0] if i + 1 < len(anchors) else end
        span = nxt - m
        p = max(1 / FPS, min(play, span))
        out.append((t, t + p, span - p))  # play t..t+p, then hold the last frame for the rest
    return out


def cut(take, anchors, end, out):
    out = Path(out)
    key = hashlib.md5(json.dumps([str(take), anchors, end]).encode()).hexdigest()[:12]
    stamp = out.with_suffix(".key")
    if out.exists() and stamp.exists() and stamp.read_text() == key:
        return
    ps = pieces(anchors, end)
    n = len(ps)
    chains = [f"[0:v]fps={FPS},split={n}" + "".join(f"[s{i}]" for i in range(n))]
    for i, (a, b, hold) in enumerate(ps):
        chains.append(f"[s{i}]trim=start={a:.3f}:end={b:.3f},setpts=PTS-STARTPTS,"
                      f"tpad=stop_mode=clone:stop_duration={max(0, hold):.3f}[p{i}]")
    chains.append("".join(f"[p{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=0,fps={FPS},format=yuv420p[v]")
    total = end - anchors[0][0]
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(take), "-filter_complex", ";".join(chains),
                    "-map", "[v]", "-t", f"{total:.3f}", "-c:v", "libx264", "-preset", "medium", "-crf", "14",
                    "-g", "30", "-movflags", "+faststart", str(out)], check=True)
    stamp.write_text(key)
