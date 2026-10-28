---
name: app-promo-video
description: Make a product trailer or promo video for a mobile app (iOS/Android) with HyperFrames, from a voiceover (or script), real app screenshots, and the brand's logo, icon and fonts. Use when someone asks for an app trailer, app promo, app store preview video, product video for their app, or runs /new-video. Turns per-scene voiceover clips into a tightened master with word timings, frames real screens with a camera that punches into the part the voice is talking about, adds word-timed titles, numbers and captions, and renders 16:9 plus a vertical cut.
---

# App promo video

A workflow on top of the HyperFrames skills for one job: a 30 s–2 min trailer for a mobile app, driven by a voiceover, built from the app's **real** screens.

**Requires** the HyperFrames core skills (`npx skills add heygen-com/hyperframes --skill hyperframes --skill hyperframes-cli --skill hyperframes-registry --skill media-use`), Node 22+, FFmpeg, Python 3.9+. Read `/hyperframes` first and follow its contract; this skill adds the app-video method, scripts and lessons.

## The method in one paragraph

The voiceover is the clock. Each sentence gets the real screen that proves it, shown in a phone frame on a brand-coloured stage; the camera zooms into the exact region (in screenshot pixels) the voice names, so text is ≥28 px on a phone, and a focus outline, a big number or a short title lands **on the spoken word**. Navigation is an iOS push, state changes crossfade, taps are a press highlight (never click rings). Titles live in a left zone the phone never enters. Captions carry the voice; they drop out where the same words are a title. Every number on screen comes from a real screenshot.

## Work loop

1. **Inventory** the inputs (`templates/brief.md` layout): voiceover clips or one file, the script, screenshots / recordings per platform, icon, logo, fonts, colours, store links, music. Look for an existing trailer project and existing screenshots before asking for new ones. Read the app's code for brand colours, fonts, Hindi/locale strings and which features are paid — facts, not guesses.
2. **Ask, don't assume.** Put the open decisions to the person in one message, each with a recommendation (`references/decisions.md`): people/footage, formats, screens source, music, real vs script numbers, length, captions, platforms, store links. Stop until they answer.
3. **Voiceover → clock.** `scripts/transcribe_clips.sh` (multilingual model for non-English), then `scripts/tighten_voiceover.py` → `voiceover.wav` + `timing.json` with every word's time on the master. Re-transcribe any clip whose words are missing with `-m medium`. Report the real length; it is set by the speech, not the script's estimate.
4. **Map regions.** `scripts/grid_sheets.sh` makes gridded contact sheets; read each zoom target as `(x, y, w, h)` in source pixels.
5. **Spec.** Write `SPEC.md` (HyperFrames `references/spec.md`): LOOK from the brand, then one line per shot with its anchor word and time. `references/shot-grammar.md` has the grammar.
6. **Build.** `npx hyperframes init videos/<slug> --resolution landscape --non-interactive --skip-transcribe`, copy assets, copy `scripts/phone_kit.py` to `tools/` and write `tools/build.py` from `templates/build_template.py` (full example: `examples/kheti-hisab/build.py`). One scene per sentence group, 8–12 s each.
7. **Check and review.** `npx hyperframes lint` → `check --json` (0 errors) → `snapshot --review`; read the beat sheet, seams and phone sheet; fix P0/P1; write `REVIEW.md`. `references/lessons.md` lists the failures already met and their fixes.
8. **Preview, then render.** `npx hyperframes preview --background`, give the URL, wait for approval. Then `render --quality delivery`, copy to `exports/<slug>/`. Vertical/square cuts are sibling projects made after the master is approved.

## Rules that matter most

- Real UI only: every phone screen is a real screenshot or recording. A missing screen is a labelled placeholder, never drawn UI. iOS screens in iPhone frames, Android in Android frames.
- Real numbers only: amounts, counts and dates come from the screens, not from the script's examples. Say so when they differ.
- The person's script is their copy: captions use the script's wording aligned to what the voice actually says (recordings drift from scripts; follow the audio).
- Honest feature claims: if a feature is paid ("Pro"), the film says so where it shows it.
- No regeneration over Studio edits: the build script rewrites the HTML; once someone edits in Studio, change by hand or port their edits first.
