# Lessons — failures already met, and their fixes

## Voiceover and timing
- **Per-scene clips have padding.** An ElevenLabs export of 11 clips was 123 s raw; capping internal pauses at 0.5 s and joining with 0.7 s gaps gave 118.8 s. Most of the length is speech, so tightening saves little — report the real length, don't promise the script's estimate.
- **Whisper `*.en` models translate.** For Hindi (or any non-English) use `-m small -l hi` or larger.
- **Whisper drops words.** One clip came back with half its sentence missing; `-m medium` recovered it. Compare each clip's last word time with its last non-silent time (`silencedetect`).
- **Recordings drift from the script.** Lines get added or reworded in the studio. Captions follow the audio, spelled as in the script.

## HyperFrames lint/check errors we hit
| Error | Cause | Fix |
|---|---|---|
| `gsap_non_transform_motion` | Moving one outline box by tweening `left/top` | One fixed box per target, cross-faded (`Scene.ol`) |
| `gsap_repeated_fromto_without_baseline` | A screen image tweened in (push) and later out | `immediateRender:false` on every fromTo after the first for a target |
| `gsap_cold_seek_hidden_fromto_missing_reveal` | A hidden element revealed by `clip-path` only | Add `opacity:1` to the destination vars |
| `duplicate_audio_track` | Several SFX on one track index | One track per SFX |
| `content_overlap` / `text_below_floor` on props | A drawn notebook with bills on top, shrunk in a pull-back | `data-layout-allow-overlap data-layout-ignore` on the prop's camera wrapper |
| `line_unread` | Payoff number on screen 1.0 s | Move the next scene's start so it holds ≥1.4 s |

## Bugs the frames showed (check can't)
- **Lists visible from frame 0**: a "grey→ink" reveal that started at opacity 1. Start at opacity 0.
- **Second phone peeking in**: a `fromTo` with immediateRender put it at y=900 from t=0. Include `opacity:0` in its from-vars.
- **Iris that didn't reveal anything**: the incoming scene's root had a solid background. Root transparent, ground inside the clipped wrapper.
- **Phone touching a title**: keep the phone's left edge right of the title zone (`TITLE_ZONE_RIGHT`), cap title width 760 px.
- **Devanagari (and other scripts with marks above the line) cut off at the top by a wipe**: `clip-path: inset(0 100% 0 0)` clips to the text box, and vowel signs like ि ी rise above it at a tight line-height. Use negative vertical insets: `inset(-40% 100% -40% 0)` → `inset(-40% 0% -40% 0)`.
- **Scenes opening already zoomed in** read as a jump cut into a detail; viewers asked for the full screen first. Open with `open_on(rect)`, and make `whip_in()` land on the full phone (it uses `open_state`), or the camera snaps back out when the zoom starts.
- **Frame 0 of the render showing end states** (slips already placed, circle already drawn) although preview snapshots looked right: the renderer's first frame can show the authored CSS before GSAP's immediate from-states apply. Give every element that animates in later its starting state in CSS too (`opacity:0`, `stroke-dashoffset`, `clip-path`), and include `opacity` in its tween. Always look at frame 0 of the MP4 — it is the thumbnail.
- **Text wrapping into the next element**: a 2-line Hindi title pushed into the Pro tag under it. Place the next element below two lines, or check width.
- **Finger dots missing**: `phone_stage()` moved tap elements into the phone by matching `class="tap"` exactly, so `class="tap finger"` stayed on the stage at screen coordinates. Match the prefix `class="tap`.
- **Prop camera aimed at the wrong place**: compute the camera from the prop's own coordinates (`ty = targetY − scale × propY`) instead of guessing.

## Sound
- A mono voiceover measured alone reads ~3 LU quieter than the rendered stereo mix. Normalize the voice with two-pass `loudnorm` (I=-16, TP=-1.5) — `normalize-audio` only changes gain and would clip — then set `vo_volume` ≈ 0.85 so the MP4 lands near -15 LUFS. Measure the MP4 with `ffmpeg -af ebur128=peak=true`.
- Check that normalizing didn't shift timing: compare `silencedetect` times before and after.

## Environment
- macOS ships Python 3.9 (no backslashes inside f-string expressions) and bash 3.2 (no `${var,,}`).
- Homebrew ffmpeg may lack `drawtext`; `grid_sheets.sh` uses `drawgrid` only.
- `hyperframes preview` stamps `data-hf-id` attributes into the HTML. Ignore them when diffing; regenerating removes them.
- `npx hyperframes init` with `--skip-transcribe`; transcribe per clip yourself (language model choice matters).

## Content honesty
- A screenshot's status bar may contradict the line (Wi-Fi icon in the "no network" scene). Keep it out of the zoom, or capture with `xcrun simctl status_bar <udid> override --wifiBars 0 --cellularBars 0 --dataNetwork hide`.
- Screens that need a paid sign-in (cloud restore) may only exist in a nearby state; outline the right option and say so in REVIEW.md.
- Paid features shown in the film get a small "Pro" tag where they appear.
- Don't use a simulator that holds the owner's real data; look for a documented marketing/demo simulator, and ask.
