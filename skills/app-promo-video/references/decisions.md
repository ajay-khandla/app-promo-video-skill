# Decisions to put to the person

Ask these in one message, each with a recommendation and the reason in a clause, before building. Skip any the inputs already answer. Number them so the reply can be "1B, rest as recommended".

| # | Decision | Options | Usual recommendation |
|---|---|---|---|
| 1 | **People on screen** (the script often calls for a farmer, a shop owner, a user) | A: real footage they shoot (no lip-sync needed — the voiceover carries the words) · B: product-led, no people: kinetic type + real screens + a drawn prop world for "the old way" · C: an illustrated character · D: AI-generated people (paid, can look fake to the audience) | **B** now; A dropped in later as clips if they can shoot. Avoid D for audiences that will judge authenticity. |
| 2 | **Formats** | 16:9 only · 16:9 + 9:16 cut (30–40 s) · + App Store preview (886×1920, ≤30 s) · + 1:1 | 16:9 master + 9:16 cut, made after the master is approved |
| 3 | **Screens** | Reuse existing screenshots · record new screen videos · both | Reuse what exists (check for an earlier trailer's `screens/` folder); capture only the missing ones. Screen recordings need a build with demo data. |
| 4 | **Music** | Their licensed track · HeyGen catalog (needs `heygen` sign-in) · local MusicGen · none | Their track; else HeyGen. Never ship a generated-in-code bed. Deliver without music if none, and say so. |
| 5 | **Numbers** | Real screen values · re-capture screens to match the script's example numbers | Real screen values |
| 6 | **Length** | Tighten pauses (cap ~0.5 s) · keep the recording as is | Tighten; report the real result (it is often longer than the script's estimate — speech sets it) |
| 7 | **Captions** | Burned-in in the voice's language · none | Burned in (most social viewing is muted) |
| 8 | **Platforms / links** | Which device frames; store links on the end card | Frames for the platforms you have screens for; both store badges on the end card; ask for the real links |

## Facts to collect, not ask

From the app's code or repo: brand colours (theme file), fonts (bundled font files), localized strings (the screen text in the film's language), which features are free vs paid, offline behaviour, bundle ids, any demo-data simulator noted in docs. From the folder: earlier trailers, screenshot sets, audio exports.

## When the person changes course

Drop the abandoned plan's files (e.g. a shot list for footage that is no longer wanted) and record the new decision in the brief. Don't keep two plans alive.
