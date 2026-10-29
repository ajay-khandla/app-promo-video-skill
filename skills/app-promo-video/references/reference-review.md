# Reviewing a reference video (YouTube link or a file)

Someone shares a video they like ("make ours feel like this"). Take its **grammar**, never its **content**.

| Take (grammar) | Never copy (content) |
|---|---|
| Shot rhythm: hold lengths, cuts per minute, where it slows down | Their footage, screens, UI, illustrations or 3D models |
| Device size and placement: % of frame height, left/centre/right, one or several phones, flat or tilted | Their colours, fonts and logo — ours come from our app's theme |
| Zoom behaviour: how far it zooms, how long a move takes, the ease, what it zooms into | Their copy, slogans, voiceover or music |
| Text system: size as % of frame height, where it sits, how it enters and leaves, how many words at once | A frame-for-frame layout of one of their shots |
| Transition kinds and durations | Anything that makes ours look like their brand |
| End-card structure: what lands in what order | |

Everything taken is re-expressed in our brand: our colours, our fonts, our real screens, our voiceover clock.

## Getting the video

- **A downloaded file**: use it as it is. Put it in `inputs/<slug>/refs/` (keep refs out of git and out of `assets/`).
- **A YouTube (or other) link**: ask before downloading, then run `scripts/fetch_ref.sh <url> inputs/<slug>/refs/<name>`. It needs `yt-dlp` (`brew install yt-dlp`) and fetches 720p at most, which is enough to read layout and motion. If the person can't allow a download, ask them for the file.
- Several references: review each separately, then write one REFERENCE.md that says which grammar comes from which.

## The low-token loop

Budget: about **6 images per reference**. Text first, images only where text can't answer.

1. **Overview** (text + ≤3 images):
   `python3 scripts/ref_review.py inputs/<slug>/refs/<name>/ref.mp4 inputs/<slug>/refs/<name>/review`
   Read `summary.md` first (size, length, hard cuts with times, tile→time table), then the sheets. The sheets sample the whole video every 2–4 s with a red 10% grid. Product videos change shots with zooms and whips more than hard cuts, so the cut count alone understates the pace.
2. **Motion** (≤3 images): choose at most 3 moments worth learning from: a zoom-in, a transition, a text entrance. Read the times off the sheet and run
   `python3 scripts/ref_review.py <ref.mp4> <review_dir> --strip 12.0 13.2`
   (8 frames, 4 per row). Read the motion from where the frames bunch: bunched at the end means ease-out, bunched at both ends means ease-in-out, even spacing means linear. Measure the zoom from how much of the frame the region fills at the start and at the end.
3. **Only if a number is still unclear**: extract one full frame at that time (`ffmpeg -ss <t> -i ref.mp4 -frames:v 1 f.png`).

Don't: read the whole video frame by frame, re-read the sheets, transcribe or analyse its audio (unless asked about pacing to music: then `npx hyperframes beats`), or download above 720p.

## What to measure (use the 10% grid)

- **Device**: height as % of frame height (e.g. 85%); centre x as % of width; how many; tilt (flat or 3D); bezel and shadow treatment; whether it ever leaves the frame.
- **Zoom**: region width as % of frame at the end of a zoom (e.g. a card fills 50% of the width = roughly our `cam()` at 2.2×); duration (strip frames × spacing); ease; whether it opens wide first.
- **Text**: cap height as % of frame height; zone (left third, top, over the device); words on screen at once; entrance (blur, slide, per word, typewriter); hold length.
- **Rhythm**: hard cuts/min, typical hold between moves, where it pauses (payoff), total length.
- **Transitions**: kind (cut, whip, zoom-through, morph, flood, push) and duration.
- **Captions**: on or off, position, size, box or no box.
- **End card**: order of icon, name, tagline, CTA, badges; hold length.

Write numbers, and mark each one **measured** (read off a grid or strip) or **guessed**.

## Output: REFERENCE.md (in the project, next to SPEC.md)

```text
REFERENCE: <title> (<url or file>), <length>, reviewed with 3 sheets + 2 strips
TAKE   (grammar → our setting)
  - device 82% of frame height, centred right  → phone_kit setup(scale=0.30, phone_center_x=1260)   [measured]
  - zoom fills ~55% width, 0.5 s ease-out, always opens wide first → cam() zmax 2.4, cam_to dur 0.5, open_on   [measured]
  - per-word blur titles, ≤5 words, left third  → title(style="blur"), width 760   [measured]
  - a whip every ~8 s, zoom-through into features → whip_out/whip_in, zoom_through   [guessed]
LEAVE  (not copied)
  - their 3D tilted phones (our rule: product UI flat), their purple gradient, their music
CHANGES TO SPEC.md
  - LOOK: ...   MOTION: ...   SHOTS: S3 opens with ..., S7 transition becomes ...
```

Show the TAKE/LEAVE list to the person before rebuilding. After the build, compare one or two of our frames with the reference side by side (`npx hyperframes snapshot --at <t> --against <ref.mp4>`): the grammar should match and the content should not.

## Mapping to phone_kit

| Reference says | Set |
|---|---|
| Phone height H% of frame | `setup(scale=...)`: phone height ≈ 2622 × scale + 26 px; 0.33 → 891 px (82%) |
| Phone centre at X% of width | `setup(phone_center_x=X% × 1920)`, and move `title_zone_right` to keep text clear |
| Zooms go to a region filling F% of width | `cam(..., zmax=...)`: F% ≈ region width × 0.33 × zoom / 1920 |
| Moves take T s with ease E | `cam_to(dur=T, ease=E)` |
| Opens on the full screen first | `open_on(rect, hold=...)` |
| Text size P% of height | `title(size=P% × 1080)` |
| Transition kinds | `whip_*`, `zoom_through` + `flood`, iris overlap, `dip` |
