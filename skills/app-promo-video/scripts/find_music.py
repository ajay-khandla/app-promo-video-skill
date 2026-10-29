#!/usr/bin/env python3
"""Find free music that may be used in a commercial app trailer, and its beat grid.

    python3 find_music.py search --feel bright,uplifting --instruments guitar,ukulele --bpm 90-125
    python3 find_music.py search --openverse "indian instrumental"
    python3 find_music.py grid <track.mp3> --bpm 100

search (Incompetech): Kevin MacLeod's catalogue (CC BY 4.0 — free for commercial use with a credit line).
  Filters the public pieces.json by feel words, instruments and tempo, and prints title, feel, BPM, length,
  instruments and the download URL. Skips feels that rarely suit a product film (aggressive, silly, humorous…).
search --openverse: Openverse audio (Freesound, Jamendo, ccMixter…) limited to CC0 and CC BY, 60 s or longer.
  Don't add category=music to that API: it drops most results. Expect many field recordings and loops;
  produced tracks are usually from Jamendo.
grid: beat phase from `npx hyperframes audio <file> --json` onsets: prints the beat length, where beats fall
  (mod one beat), the most likely bar phase, and the track's steepest/peak moments — a good media-start for
  the bed is a bar line at or after "steepest".

Never use NC, ND or SA licences for a trailer. Keep the credit line in the export folder (CREDITS.txt) and
put it in the store/YouTube description. Needs curl, ffmpeg and npx hyperframes.
"""
import argparse
import collections
import json
import subprocess
import urllib.parse

SKIP_FEELS = ("aggressive", "silly", "humorous", "dark", "scary", "unnerving", "eerie", "somber")


def incompetech(feel, instruments, bpm):
    raw = subprocess.check_output(["curl", "-s", "-m", "60", "https://incompetech.com/music/royalty-free/pieces.json"])
    pieces = json.loads(raw)
    lo, hi = (int(x) for x in bpm.split("-")) if bpm else (0, 999)
    out = []
    for p in pieces:
        f = str(p.get("feel") or "").lower()
        ins = str(p.get("instruments") or "").lower()
        try:
            b = int(p.get("bpm") or 0)
        except ValueError:
            b = 0
        if feel and not any(w in f for w in feel):
            continue
        if instruments and not any(w in ins for w in instruments):
            continue
        if any(w in f for w in SKIP_FEELS) or not (lo <= b <= hi):
            continue
        out.append(p)
    for p in out:
        url = "https://incompetech.com/music/royalty-free/mp3-royaltyfree/" + urllib.parse.quote(p["filename"])
        print(f"{p['title']:28s} | {p.get('feel')} | {p.get('bpm')} bpm | {p.get('length')} | {str(p.get('instruments'))[:50]} | {url}")
    print(f"{len(out)} tracks — CC BY 4.0, credit: \"<title>\" Kevin MacLeod (incompetech.com), CC BY 4.0")


def openverse(q):
    url = f"https://api.openverse.org/v1/audio/?q={urllib.parse.quote(q)}&license=cc0,by&page_size=40"
    d = json.loads(subprocess.check_output(["curl", "-s", "-m", "90", url]))
    for r in d.get("results", []):
        dur = (r.get("duration") or 0) / 1000
        if dur >= 60:
            print(f"{r['license']}-{r.get('license_version')} | {round(dur)} s | {r['title'][:50]} | {r.get('creator')} | "
                  f"{r.get('source')} | {r.get('foreign_landing_url')} | {r.get('url')}")


def grid(track, bpm):
    d = json.loads(subprocess.check_output(["npx", "hyperframes", "audio", track, "--json"], stderr=subprocess.DEVNULL))
    it = d["items"][0]
    beat = 60 / bpm
    strong = [e["t"] for e in it["onsets"]["events"] if e["strength"] > 0.35]
    ph = collections.Counter(round((t % beat) / 0.02) * 0.02 for t in strong)
    bar = collections.Counter(round((t % (beat * 4)) / 0.05) * 0.05 for t in strong)
    print(f"beat {beat:.3f} s, bar {beat * 4:.3f} s")
    print("beat phase (s mod beat):", ph.most_common(3))
    print("bar phase (s mod bar):", bar.most_common(4))
    print("moments:", it.get("moments"))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("search")
    s.add_argument("--feel", default="bright,uplifting")
    s.add_argument("--instruments", default="")
    s.add_argument("--bpm", default="90-125")
    s.add_argument("--openverse")
    g = sub.add_parser("grid")
    g.add_argument("track")
    g.add_argument("--bpm", type=float, required=True)
    a = ap.parse_args()
    if a.cmd == "grid":
        grid(a.track, a.bpm)
    elif a.openverse:
        openverse(a.openverse)
    else:
        incompetech([w for w in a.feel.lower().split(",") if w], [w for w in a.instruments.lower().split(",") if w], a.bpm)


if __name__ == "__main__":
    main()
