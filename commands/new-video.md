---
description: Make a product trailer for one of our iOS/Android apps with HyperFrames, from the voiceover/script, screenshots and brand assets we provide
argument-hint: <app-name or inputs/<slug> folder> [--format 16:9|9:16|1:1|all] [--no-stops]
---

# /new-video

Make a product trailer for a mobile app (iOS and/or Android).

Arguments: `$ARGUMENTS`

Load the `/app-promo-video` skill and follow its work loop; it builds on `/hyperframes` (read first), `/hyperframes-cli`, `/hyperframes-registry` and `/media-use`.

## Folders

- Inputs: `inputs/<slug>/` — copy from `inputs/_template/` (the skill's `templates/brief.md` and `script.md`): `brief.md`, `script.md`, `audio/` (voiceover clips or one file, optional `music/`), `brand/` (icon, logo, fonts), `screens/ios/`, `screens/android/`.
- Project: `videos/<slug>/` (variants `videos/<slug>-vertical/`, `videos/<slug>-square/`).
- Final files: `exports/<slug>/<slug>-<format>-<YYYY-MM-DD>.mp4`.

## Steps

1. Work out the slug from the arguments. If `inputs/<slug>/` is missing, create it from the template, say exactly what to drop where, and stop.
2. Inventory the inputs and look for existing material (an earlier trailer project, screenshot sets, the app's code for colours, fonts, localized strings and paid features). Report what you have, what is missing, and what you'll do about each gap.
3. Put the open decisions to the person in one message with recommendations (skill: `references/decisions.md`). Stop until they answer, unless `--no-stops` was passed.
4. Voiceover → `voiceover.wav` + `timing.json` (skill: `scripts/transcribe_clips.sh`, `scripts/tighten_voiceover.py`). Report the real length.
5. Map screenshot regions (`scripts/grid_sheets.sh`), write `SPEC.md`, build with `tools/build.py` + `phone_kit.py`.
6. `npx hyperframes check --json` to 0 errors, `snapshot --review`, fix, write `REVIEW.md`.
7. `npx hyperframes preview --background`, share the URL, and wait for approval. Then `npx hyperframes render --quality delivery` and copy to `exports/`.
8. `--format all`: after the 16:9 master is approved, build the 9:16 and 1:1 cuts as sibling projects.

Rules: real screens and real numbers only; the script's wording in captions, timed to what the voice actually says; paid features marked; never regenerate over edits made in Studio.
