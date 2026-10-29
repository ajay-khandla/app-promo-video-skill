# Shot grammar for app trailers

Numbers are for a 1920×1080 canvas at 30 fps with 1206×2622 iPhone screenshots shown at 0.33 (398×865 screen, 13 px bezel). `phone_kit.py` implements all of it.

## Stage

- Brand ground (solid), a lighter patch behind the phone (radial, ~60%), phone centred at x=1240, top 40 px, so the bottom 150 px stays free for captions.
- **Left zone** x 120–880 for titles, numbers and lists. The camera never lets the phone's left edge cross x≈905 (`TITLE_ZONE_RIGHT`).
- Worlds: the brand stage for product beats; a prop world for "the old way" (a notebook, bills, a spreadsheet — drawn props are fine because they don't claim to be the product); a brand-colour world for the end card.

## Camera

- One wrapper per scene, `transform-origin: 0 0`, tweened `x / y / scale`.
- **Every scene opens on the full phone** (zoom 1), holds ~0.4 s so the viewer sees which screen this is, then zooms in: `sc.open_on(rect)` (use `frm=` for a camera carried in from the previous scene). Whip-ins land on the full phone too. Never open a scene already zoomed in.
- `cam(x, y, w, h)` frames a screenshot region: zoom = min(2.9, 940/(w·0.33), 780/(h·0.33)); 2.9 keeps ~1 source px per screen px (sharp). Region centre lands at (≥1330, 470).
- Moves 0.6 s `power2.inOut`; start a move ~0.15–0.3 s **before** the anchor word so the region is settled when the word lands.
- Establish (zoom 1) → isolate (zoom on the region) → return (zoom 1) within a beat. A whole screen at zoom 1 is unreadable on a phone; it is for context only.
- Zoom-through: `zoom_through(state, cx, cy, 5)` in 0.45 s `power3.in` into a tapped tile, then a colour flood carries into the next scene.

## Screens

- Navigation (a real tap opens a new screen): `enter="push"` — new screen slides from 100% in 0.42 s `power3.out`, old one to −30% and 60% opacity.
- State change on the same screen (form filled, toggle flipped, sheet opened): `enter="fade"` 0.22 s.
- Don't imply navigation that the app doesn't do (save → a different account page is a fade "carry", not a push).

## Attention

- **Focus outline**: accent 2.2 px stroke, radius 9, around a region; lands with scale 1.08→1 in 0.3 s `expo.out` on the spoken word, previous one fades in 0.15 s. Use it for the one thing the sentence names.
- **Tap**: press highlight rgba(ink, 0.14) over the tapped region, 0.06 s in / 0.2 s out. No ripples or rings.
- **Numbers**: label 48 px + value 96–150 px in the display face, in the colour the app uses for that kind of number (income green, expense red/clay, due red); lands on the word, holds ≥ 0.5 s + 0.3 s/word (the payoff ≥ 1.4 s).
- **Lists that grow on the words** ("Spraying • Irrigation • Fertiliser"): one line per spoken word; vary the entrance between scenes (blur-in vs grey→ink) so it doesn't read as a template.

## Result moments (from the Groundswell / Property Toolbox reference review)

- **Lift**: once per feature, the result the voice names (an amount, a balance, a status card) lifts out of the phone: `sc.lift(key, t_in, t_out, rect, k=2.2)`. The real screenshot region is re-drawn sharp at k×, rises from its place in the phone to beside it (never into the title zone), holds while it is spoken, and settles back. The camera goes to the full phone first, by itself. A brand-green check badge pops on its corner (`check=True`).
- **Count-up**: the matching left-zone number counts up to the real value in 0.6 s with Indian digit grouping (`amount(..., count=True)`, the default).
- **Show the tap**: every `tap()` has a soft finger-tip dot that arrives 0.3 s early and presses with the highlight. It is a filled dot, not a ring.
- **One accent word per title**: `title(..., accent=("याद",))` in brand green, or clay for a problem word.

## Transitions (use 3–5 kinds, each caused by something on screen)

| Kind | Kit | Use |
|---|---|---|
| Whip | `whip_out()` / `whip_in()` | topic change |
| Zoom-through + flood | `zoom_through` + `flood(color, t, 0.3, 0, 1)`; next scene `flood(color, start, 0.35, 1, 0)` | a tap that opens the next feature |
| Carry | same phone continues, camera to zoom 1 at the seam | adjacent features |
| Iris from the tap | next host starts 0.35 s early (overlap in `SCENES`), root transparent, `clip-path: circle()` from the tap point | a button that opens a new section |
| Dip | `dip()` | a hard turn |
| Brand sweep | `sweep_out(brand)` at the end of one scene + `sweep_in(brand)` at the start of the next: a giant rounded brand shape crosses the frame diagonally (0.45 s in / 0.5 s out) | a change of world (prop world → app, feature group → feature group, last scene → end card) |
| Colour flood into the end card | `flood(brand, t, 0.4, 0, 1)` | the last seam |

## Captions

- One group at a time, 2–6 words, broken at punctuation and pauses ≥150 ms, timed from `timing.json` words. Text from the script (corrected to what is said), never Whisper's spelling.
- Bottom 52 px, main face 600 at 44 px, ink on a ground-coloured scrim sized to the text (`inline-block` inside a full-width `text-align:center` row — never `left:50%; translateX(-50%)`).
- Leave a caption out when the same words are already a title on screen (tagline, end card).

## End card

App icon (the phone can shrink into it), wordmark wipes in, Latin name, tagline lighting word by word on the voice, a sub-line, then the official App Store / Google Play badges. Hold ≥2.5 s after the last word.

## Vertical cut (9:16)

Made after the 16:9 master is approved, as a sibling project (`videos/<slug>-vertical/`). Example: `examples/kheti-hisab/build_vertical.py`.

- **Voiceover**: 30–40 s cut from the master's voiceover in a few voice-continuous pieces: a 2 s hook question, the name reveal, two feature beats that each end on a result, and the end card. Cut only at word gaps from `timing.json`; write `segments.json` (`orig_start`, `orig_end`, `v_start`) and map every master-clock time with `V(t)`, so the scene code keeps the master's word times.
- **Layout** (1080 × 1920): title zone at the top (y 120–410), one caption band under it (y ≈ 435–505, `build_captions(bottom=H-505)`), and the phone below at scale 0.5 (top 560). This keeps text out of the platform's bottom and right overlays.
- **Kit settings**: `setup(width=1080, height=1920, scale=0.5, bezel=20, phone_center_x=540, phone_top=560, screen_radius=88, title_zone_right=0, frame={"cx_min": 540, "cy": 1200, "max_w": 1000, "max_h": 1100, "right_max": 1060}, lift_box=(40, 620, 1040, 1500), lift_dy=-80)`; lifts at k ≈ 1.6–2.0.
- **Taps near the bottom** (save buttons): raise the phone ~130 px for the tap instead of zooming, as zooming the bottom of the screen pushes the phone under the title zone.
- **End card**: everything centred and stacked: icon, wordmark, Latin name, tagline, sub-line, badges.
