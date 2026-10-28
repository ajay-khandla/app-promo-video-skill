# Example: Kheti Hisab Hindi trailer

A 2:01, 16:9 trailer for **Kheti Hisab** (farm accounting for Indian farmers, iOS + Android), built with this skill.

- **Input**: 11 ElevenLabs voiceover clips in Hindi (123 s raw), a 10-scene Hindi script, 130 real Hindi screenshots with demo data, the app icon, the official store badges, and the app's own fonts and colours.
- **Decisions**: product-led (no live action; the farmer's questions are captions over a drawn notebook-and-bills prop world), real screen numbers instead of the script's examples, pauses capped at 0.5 s (118.8 s voiceover), Hindi captions burned in, iPhone frames, both store badges.
- **Result**: 11 scenes, 21 screenshots, 56 caption groups, 12 sound effects; `check` 0 errors.

Files here:

- `build.py` — the complete shot data (scene windows, screenshot regions, anchor-word times, titles, numbers, captions, SFX) using `phone_kit.py`.
- `SPEC.md` — the director's brief: LOOK as numbers, one line per shot with its anchor word.
- `REVIEW.md` — the review notes: creative calls, what was measured, the weakest shots.

The screenshots, voiceover and brand files are not included (they belong to the app's owner), so `build.py` documents the method rather than rendering on its own. To adapt it: replace `SHOTS`, `COLORS`, `FONTS`, `SCENES`, the per-scene functions and `CAPS` with your film's.
