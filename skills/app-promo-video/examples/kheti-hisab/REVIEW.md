# REVIEW — Kheti Hisab Hindi trailer, 16:9 (2026-10-29, restyled from REFERENCE.md)

## Creative calls
- Product-led, no live action. The farmer's lines are voiceover + Hindi captions; his messy notebook and bills (S1) stand in for "the old way". Every app picture is a real screenshot from `kheti-hisab-trailer/screens`.
- Brand-native look: cream #F6EFE7 stage, the app's green / clay / marigold used the way the app uses them; Noto Sans Devanagari + Bricolage Grotesque from the app's own fonts.
- Amounts are the real screen values, not the script's examples: लेना ₹1,19,250 / देना ₹16,416 (Money-owed report), बकाया ₹2,400, Profit ₹1,82,568 (Season P&L).
- The voiceover is the clock: every outline, title and amount lands on its spoken word (`assets/audio/timing.json`).
- Transitions: brand-green sweep (S1→2, S7→8, S10→11), whip (S3→4, S6→7), zoom-through + colour flood (S2→3, S9→10), carry (S4→5, S8→9), iris from the tap (S5→6).

## Measured vs looked at
- `check`: 0 errors. Kept warnings: the captions file has 56 groups (one per spoken phrase, by design); S5 has 4 screens; S7 shows the contract overview twice (before and after the payments tab).
- Looked at: all 22 beat frames, 11 seams, the phone sheet, and spot frames at 1, 3.5, 6.8, 9.8, 45.5, 53.5, 69.5, 73, 83.1, 90, 96, 108.3, 119 s.
- Not checked by anyone: the sound. The voiceover and 12 effects (whoosh, click, pop from the bundled library) were placed by time, not heard. No music bed (no track supplied).

## Weakest shots
- S1 is drawn props (notebook, bills); it reads clearly, but a real photo of a khata would be stronger.
- S3 category grid is zoomed less (1.7×) because all three rows are named in one line; the tile labels are small, the icons carry it.
- S8 claims "no network" while the screenshot's status bar shows Wi-Fi; the zoom keeps the status bar out of frame, but a real no-signal capture would be better.
- S9 "new phone" uses the real onboarding choice screen with "नई बुक शुरू करें" selected; the outline points at "क्लाउड सिंक से मेरी बुक लाएँ". A capture with the cloud option selected (needs a Pro sign-in) would be exact.

## To do
- Music: a soft folk/acoustic bed at ~0.14 under the voice once a track is supplied.
- Store links for the end card (badges are there, no URL text).
- 9:16 Reels/Shorts cut after this cut is approved.
- Generator: `tools/build.py` rewrites index.html and compositions/*.html — edit the data there, or stop using it once hand edits start in Studio.

## 2026-10-29 restyle
- Style picked from three references (REFERENCE.md): Property Toolbox's step-by-step walkthrough plus Groundswell's result lifts, check badges, count-ups and brand sweeps. Wellio was left out (stock people, glass/mesh gradients).
- Added: full-phone-first openings; six result lifts; count-up amounts; finger dots on every tap; three green sweeps; one accent word in the S1, S6 and S9 titles.
- Fixed: render frame 0, wrapped S6 title, the "दिया?" overlap, voice loudness (MP4 measured, not heard).
- Real captures (after upgrading Flutter to 3.47.8): the app was built from a scratch copy for the iPhone 17 simulator, set up as a fresh Hindi book (Green Valley Farm, कपास), and two flows were recorded — S3 now plays the real add-expense walkthrough (₹6400 typed, saved, home updates to ₹12,800) and S8 the same flow with no Wi-Fi or mobile signal in the status bar (saved, home shows खर्च ₹15,300). Raw takes: inputs/kheti-hisab/screens/ios/recordings/.
- Still open: the restore-on-new-phone screen with the cloud option selected (needs a Pro sign-in).
