# Music bed and final export

## Finding a track (free for a commercial trailer)

Licence first: **CC0 or CC BY only**. Never NC (non-commercial), ND or SA for a store/YouTube trailer. Keep the credit line.

| Source | How | Notes |
|---|---|---|
| The person's own licensed track | `inputs/<slug>/audio/music/` | Always first |
| Incompetech (Kevin MacLeod) | `scripts/find_music.py search --feel bright,uplifting --instruments guitar,ukulele --bpm 90-125` | CC BY 4.0, 1,400+ tracks with feel/BPM/instrument metadata; the overused ones ("Carefree", "Life of Riley") are best avoided |
| Openverse (Jamendo, Freesound, ccMixter) | `scripts/find_music.py search --openverse "indian instrumental"` | CC0/BY filter; mostly field recordings and loops, a few produced Jamendo tracks |
| HeyGen catalogue | `/media-use` (`bgm`) | Needs a `heygen` sign-in |

Pick by the film's feel, not its subject: a narrated product film wants a steady, warm, uncluttered bed (no vocals, moderate energy, 90–125 BPM). You cannot listen: measure each candidate's loudness and energy contour (a 4-second RMS strip shows intros, drops and breaks) and say in the delivery note that the pick was measured, not heard — and name the runners-up so the person can swap.

Put the credit in `exports/<slug>/CREDITS.txt`, e.g. `Music: "Fretless" by Kevin MacLeod (incompetech.com), CC BY 4.0, https://creativecommons.org/licenses/by/4.0/`.

## Placing it

- **Story placement**: leave the "old way" opening under voice only, and bring the music in with the product reveal; it lifts after the last word for the end card.
- **Enter on a bar line**: `scripts/find_music.py grid <track> --bpm <bpm>` gives the beat phase and the track's steepest moment. Choose a `music_media_start` on a bar at or after it, and put `music_start` on the reveal, so every beat afterwards falls on the film's grid.
- **Duck**: a `volume` lane in clip seconds — `[(0, 0), (0.35, 0.17), (last_word, 0.17), (last_word + 0.7, 0.42)]` — with `data-volume="1"`, and `data-fade-out` 1.4–2 s at the end. ~0.17 sits a mono voice at about −16 LUFS clearly on top.
- Kit: `K.build_index(sfx=SFX, vo_volume=0.85, music="assets/audio/music.mp3", music_start=12.3, music_media_start=16.8, music_lane=[...], music_fade_out=1.6)`.
- Measure the render: integrated −16 to −14 LUFS, true peak below −1 dB (`ffmpeg -af ebur128=peak=true`).

## Export

- 4K masters (largest, sharpest): `npx hyperframes render --quality delivery --resolution landscape-4k --crf 12 --output renders/<slug>-16x9-4k.mp4` (`portrait-4k` for 9:16). Screenshots are 3× captures, so at 4K the phone stays sharp until a zoom passes ~2×.
- 1080p copies for quick sharing: `--quality delivery` without `--resolution`.
- Copy to `exports/<slug>/<slug>-<format>[-4k]-<date>.mp4` with `CREDITS.txt` next to them. Check each file: duration equals the root `data-duration`, resolution, loudness, and frame 0.
