# app-promo-video — an agent skill for mobile app trailers

An [Agent Skill](https://docs.claude.com/en/docs/agents-and-tools/agent-skills) that turns a **voiceover**, your app's **real screenshots** and your **brand files** into a product trailer, rendered with [HyperFrames](https://github.com/heygen-com/hyperframes) (HTML → MP4).

It works in Claude Code, and in other coding agents that load skills, on top of the HyperFrames core skills. It adds three things: a method for app videos, the scripts that make that method fast, and a list of the failures already hit and how to avoid them.

```
voiceover clips ─► transcribe ─► tighten ─► voiceover.wav + timing.json (every word's time)
screenshots ─────► grid sheets ─► regions (x, y, w, h) in screenshot pixels
script + brand ──► SPEC.md (one line per shot, anchored to a spoken word)
                         │
                         ▼
              tools/build.py + phone_kit.py ─► HyperFrames compositions
                         │
                         ▼
        check ─► snapshot review ─► Studio preview ─► render 16:9 ─► 9:16 cut
```

## What the videos look like

- **The voice is the clock.** Each sentence gets the real screen that proves it, in a phone frame on a stage in your brand colour.
- **The camera does the explaining.** It zooms into the exact region the voice names, so text is readable on a phone. A focus outline, a big number or a short title lands **on the spoken word**.
- **The motion matches the app.** Opening a new screen uses the iOS push transition, a change on the same screen crossfades, and a tap shows as a press highlight. There are no click rings and no invented UI.
- **Titles have their own space.** They sit in a left-hand zone that the phone never enters.
- **Captions in the voice's language.** They use the script's wording, timed to what is actually said, and drop out where the same words are already a title.
- **Results lift out.** Each feature ends on one result moment: the real card (an amount, a balance) lifts out of the phone with a check badge while the number counts up. A brand-coloured shape sweeps across between worlds, and a finger dot shows every tap.
- **Transitions have a cause.** There are 3–5 kinds per film: whip, zoom-through a tapped tile into a colour flood, carry, iris from a tap, dip, and a flood into the end card.
- **The end card:** the phone shrinks into the app icon, the wordmark and tagline land in time with the voice, then the official App Store / Google Play badges appear.

## Install

**1. HyperFrames core skills.** Run this in your video project folder:

```bash
npx skills add heygen-com/hyperframes --skill hyperframes --skill hyperframes-cli --skill hyperframes-registry --skill media-use -a claude-code -y
```

**2. This skill.** Run it in the same folder:

```bash
npx skills add ajay-khandla/app-promo-video-skill -a claude-code -y
```

Or copy `skills/app-promo-video/` into `.claude/skills/` (project) or `~/.claude/skills/` (global).

**3. Optional: the `/new-video` slash command for Claude Code**

```bash
mkdir -p .claude/commands && curl -sL https://raw.githubusercontent.com/ajay-khandla/app-promo-video-skill/main/commands/new-video.md -o .claude/commands/new-video.md
```

**Requirements:** Node.js 22+, FFmpeg, Python 3.9+ (standard library only), and a coding agent that loads skills. A music bed needs either your own track or a HeyGen sign-in (`/media-use`).

## Use

```text
/new-video kheti-hisab
```

You can also ask directly: *"Make a 60-second trailer for our app from these voiceover clips and screenshots."*

The agent will:

1. **Take stock.** It inventories your inputs and looks for material that already exists: an earlier trailer, screenshot sets, and the app's code for colours, fonts, localized strings and paid features.
2. **Ask before deciding.** The open decisions come in one message, each with a recommendation ([decisions](skills/app-promo-video/references/decisions.md)): people on screen, formats, screen source, music, real or script numbers, length, captions and store links.
3. **Build the voiceover clock.** It transcribes and tightens the voiceover and reports the real length.
4. **Plan the shots.** It maps the screenshot regions and writes `SPEC.md`.
5. **Build and check.** It runs `check` until there are 0 errors, reviews the snapshot sheets and writes `REVIEW.md`.
6. **Show, then render.** It opens the Studio preview and waits for your approval before rendering.

### Style references (YouTube link or video file)

Share a video you like and say what you like about it. The agent reviews it on a small budget:

- **Overview:** `ref_review.py` writes a text summary (hard cuts, timings) plus at most 3 gridded contact sheets.
- **Motion:** at most 3 motion strips, for the zoom, transition or text entrance worth learning from.

From that it writes `REFERENCE.md`, which records:

- **Take:** the grammar, mapped to our settings: device size and position, zoom amount and ease, text size and entrance, rhythm, transitions.
- **Leave:** content that is not copied: their footage, colours, fonts, copy and music.

Everything taken is rebuilt in your own brand and screens. Links are downloaded at 720p with `fetch_ref.sh` (needs `yt-dlp`), only after you agree. Full guide: [reference-review.md](skills/app-promo-video/references/reference-review.md).

### Input folder

```
inputs/<app-slug>/
  brief.md          app, platforms, store links, formats, music, colours (templates/brief.md)
  script.md         the voiceover script, word for word
  audio/            voiceover: one file or one clip per scene (e.g. an ElevenLabs export); music/ optional
  brand/            app icon 1024 px, logo (SVG preferred), fonts/, store badge files
  refs/             optional style references (videos you like); not in git, never used as footage
  screens/ios/      real screenshots or screen recordings, numbered in order
  screens/android/  same for Android
```

## What's in the box

```
skills/app-promo-video/
  SKILL.md                     the work loop and the rules that matter most
  references/
    decisions.md               the questions to ask, with recommended defaults
    shot-grammar.md            stage, camera, screens, attention, transitions, captions, end card — in numbers
    lessons.md                 lint errors, visual bugs and environment traps already met, with fixes
    reference-review.md        take a reference video's grammar (not its content) in ~6 images
  scripts/
    transcribe_clips.sh        word timings for every clip (multilingual Whisper via `hyperframes transcribe`)
    tighten_voiceover.py       join clips, cap pauses, remap word times → voiceover.wav + timing.json
    grid_sheets.sh             gridded contact sheets for reading zoom regions off screenshots
    ref_review.py              low-token review of a reference video: cuts, gridded contact sheets, motion strips
    fetch_ref.sh               download a YouTube/other reference at ≤720p (yt-dlp), for review only
    phone_kit.py               the scene generator (camera, screens, taps, outlines, titles, numbers, lists,
                               transitions, captions, root composition)
  templates/
    brief.md, script.md        the per-app input files
    build_template.py          a two-scene starting point for tools/build.py
  examples/kheti-hisab/        a complete 2-minute Hindi trailer: build.py, SPEC.md, REVIEW.md
commands/new-video.md          Claude Code slash command
```

### Scripts

```bash
# 1. word timings per clip (use a multilingual model for non-English; *.en models translate)
scripts/transcribe_clips.sh inputs/my-app/audio/clips transcripts hi small

# 2. one tightened master + word timings on it
python3 scripts/tighten_voiceover.py inputs/my-app/audio/clips transcripts inputs/my-app/audio \
    --max-pause 0.5 --scene-gap 0.7 --keep-last

# 3. measuring sheets for zoom regions (1/3 scale; red line = 100 px, blue = 500 px)
scripts/grid_sheets.sh sheet-a.png screens/ios/01-home.png screens/ios/02-add.png
```

### phone_kit in brief

```python
import phone_kit as K
K.setup(root=ROOT, total=121.5, scenes=SCENES, shots=SHOTS, colors=COLORS, fonts=FONTS,
        font_main="'Noto Sans Devanagari', sans-serif", font_display="'Bricolage Grotesque', sans-serif")
from phone_kit import *

sc = Scene("s4")
sc.screen("owed", 37.0, 44.65, enter="push")          # real screenshot, iOS push
sc.open_on((48, 420, 1107, 210))                      # open on the full phone, then zoom in
sc.cam_to(38.55, cam(48, 420, 1107, 210))             # frame a region (screenshot px)
sc.ol(39.1, (90, 450, 495, 165))                      # outline lands on "लेना"
sc.lift("owed", 38.95, 42.5, (48, 420, 1107, 210))    # the result card lifts out of the phone, check badge
sc.amount("s4-a1", "लेना", "₹1,19,250", C["green"], 39.35, 42.6)
sc.write(phone_stage(sc))

K.build_captions(CAPS)                                # [(start, end, text)]
K.build_index(sfx=SFX, music="assets/audio/music.mp3")
```

All times are **absolute seconds on the voiceover**. All regions are in the **screenshot's own pixels**. The generator rewrites `index.html` and `compositions/*.html`, so once someone edits in HyperFrames Studio, make further changes by hand.

## Worked example

[`examples/kheti-hisab`](skills/app-promo-video/examples/kheti-hisab) is a 2:01 trailer in Hindi for a farm-accounting app, from a real production:

- **Inputs:** 11 voiceover clips and 130 real screenshots.
- **Output:** 11 scenes, 56 caption groups, and 0 errors from `check`.

Its `REVIEW.md` names the weakest shots and why. The app's screenshots, voice and brand files are not included.

## Principles

- **Real UI only.** Every screen shown is a real capture. A missing screen becomes a labelled placeholder.
- **Real numbers only.** On-screen amounts come from the screens, not from the script's examples.
- **The person's copy is theirs.** Captions use the script's wording, aligned to the recording.
- **Honest claims.** Paid features carry a "Pro" tag where they appear.
- **Ask, don't assume.** Every creative fork goes to the person with a recommendation.

## Credits

Built on [HyperFrames](https://github.com/heygen-com/hyperframes) by HeyGen (Apache-2.0) and its skills. Uses [GSAP](https://gsap.com) through HyperFrames. Bundled sound effects come from the HyperFrames `media-use` skill library and are not redistributed here.

## License

[MIT](LICENSE) © 2026 Ajay Khandla
