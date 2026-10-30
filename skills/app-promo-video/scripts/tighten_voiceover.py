#!/usr/bin/env python3
"""Join per-scene voiceover clips into one tightened master and remap word timings onto it.

    python3 tighten_voiceover.py <clips_dir> <transcripts_dir> <out_dir>
        [--max-pause 0.5] [--scene-gap 0.7] [--keep-last]

- <clips_dir>: one audio file per scene (mp3/wav/m4a), sorted by name = film order
  (e.g. an ElevenLabs project export: 00_Chapter_1.mp3, 01_Scene_02.mp3, ...).
- <transcripts_dir>/<clip stem>/transcript.json: word timings from
  `npx hyperframes transcribe <clip> -d <transcripts_dir>/<stem> -m small -l <lang> --engine whisper`
  (see transcribe_clips.sh). Re-run a weak clip with `-m medium` into the same folder.
- Pauses inside a clip longer than --max-pause are shortened to it; each clip's tail is
  trimmed; clips are joined with --scene-gap of silence. --keep-last leaves the final clip's
  pauses alone (a slow tagline delivery).

Writes <out_dir>/voiceover.wav (48 kHz) and <out_dir>/timing.json:
  {"total": s, "scenes": [{scene, file, start, end, length, source_length}], "words": [{scene, text, start, end}]}
Prints each scene's window and its transcript so you can plan shots against it.

Needs ffmpeg/ffprobe on PATH. Python 3.9+.
"""
import argparse
import json
import re
import subprocess
from pathlib import Path

AUDIO = {".mp3", ".wav", ".m4a", ".aac", ".flac", ".ogg"}


def silences(f):
    err = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(f), "-af",
                          "silencedetect=noise=-40dB:d=0.35", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    s = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", err)]
    e = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", err)]
    return list(zip(s, e))


def hard_stop(f):
    """True when a clip ends in pure digital silence right after loud speech, i.e. the generator cut the last
    word off (the clip has no room tone and stops dead). Re-generate such a clip; a fade can't bring words back."""
    tail = subprocess.run(["ffmpeg", "-v", "error", "-sseof", "-2", "-i", str(f), "-af",
                           "asetnsamples=n=2205,astats=metadata=1:reset=1,ametadata=print:key=lavfi.astats.Overall.RMS_level:file=/dev/stdout",
                           "-ar", "44100", "-f", "null", "-"], capture_output=True, text=True).stdout
    lv = [float(x) if x not in ("-inf", "inf") else -999.0 for x in re.findall(r"RMS_level=(-?inf|[-\d.]+)", tail)]
    for i in range(len(lv) - 8):   # loud, then dead (below room tone, ~-86 dB) within 150 ms
        if lv[i] > -30 and all(v < -120 for v in lv[i + 3:i + 8]):
            return True
    return False


def duration(f):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                          "-of", "csv=p=0", str(f)]).decode())


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("clips")
    ap.add_argument("transcripts")
    ap.add_argument("out")
    ap.add_argument("--max-pause", type=float, default=0.5)
    ap.add_argument("--scene-gap", type=float, default=0.7)
    ap.add_argument("--edge", type=float, default=0.06, help="silence kept after the last word of a clip")
    ap.add_argument("--keep-last", action="store_true")
    a = ap.parse_args()

    clips = sorted(p for p in Path(a.clips).iterdir() if p.suffix.lower() in AUDIO)
    if not clips:
        raise SystemExit(f"no audio files in {a.clips}")
    segments, scenes, words, t = [], [], [], 0.0
    for f in clips:
        if hard_stop(f):
            print(f"WARNING {f.name}: ends in digital silence right after speech — the last word is probably cut off. "
                  f"Re-generate it before building the video.")
    for i, f in enumerate(clips):
        d, last = duration(f), i == len(clips) - 1
        keep, cur = [], 0.0
        for s, e in silences(f):
            if e >= d - 0.01:  # tail silence
                keep.append((cur, min(d, s + a.edge)))
                cur = None
                break
            if not (last and a.keep_last) and e - s > a.max_pause:
                keep.append((cur, s + a.max_pause / 2))
                cur = e - a.max_pause / 2
        if cur is not None:
            keep.append((cur, d))
        start = t

        def remap(x, keep=keep, base=start):
            acc = base
            for k0, k1 in keep:
                if x <= k1:
                    return acc + max(0.0, x - k0)
                acc += k1 - k0
            return acc

        tj = Path(a.transcripts) / f.stem / "transcript.json"
        if tj.exists():
            w = json.loads(tj.read_text())
            w = w if isinstance(w, list) else w.get("words", [])
            for x in w:
                words.append({"scene": i + 1, "text": x["text"], "start": round(remap(x["start"]), 2),
                              "end": round(remap(x["end"]), 2)})
        else:
            print(f"warning: no transcript for {f.name} at {tj}")
        for k0, k1 in keep:
            segments.append((f, k0, k1))
            t += k1 - k0
        scenes.append({"scene": i + 1, "file": f.name, "start": round(start, 2), "end": round(t, 2),
                       "length": round(t - start, 2), "source_length": round(d, 2)})
        if not last:
            segments.append((None, 0, a.scene_gap))
            t += a.scene_gap

    inputs, filters, labels = [], [], []
    for n, (f, k0, k1) in enumerate(segments):
        if f is None:
            filters.append(f"anullsrc=r=44100:cl=mono,atrim=0:{k1:.3f}[s{n}]")
        else:
            inputs += ["-i", str(f)]
            k = len(inputs) // 2 - 1
            length = k1 - k0
            filters.append(f"[{k}:a]atrim={k0:.3f}:{k1:.3f},asetpts=PTS-STARTPTS,aformat=sample_rates=44100:channel_layouts=mono,"
                           f"afade=t=in:d=0.01,afade=t=out:st={max(0, length - 0.01):.3f}:d=0.01[s{n}]")
        labels.append(f"[s{n}]")
    filters.append("".join(labels) + f"concat=n={len(labels)}:v=0:a=1[out]")
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", ";".join(filters),
                    "-map", "[out]", "-ar", "48000", str(out / "voiceover.wav")], check=True)
    (out / "timing.json").write_text(json.dumps({"total": round(t, 2), "scenes": scenes, "words": words},
                                                ensure_ascii=False, indent=1))
    print(f"total {t:.2f}s -> {out / 'voiceover.wav'}")
    for s in scenes:
        line = " ".join(f"{x['text']}@{x['start']:.1f}" for x in words if x["scene"] == s["scene"])
        print(f"S{s['scene']:>2} {s['start']:7.2f}-{s['end']:7.2f} ({s['length']:5.2f}s, was {s['source_length']}) {line}")


if __name__ == "__main__":
    main()
