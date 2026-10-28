# Shot grammar for app trailers

Numbers are for a 1920×1080 canvas at 30 fps with 1206×2622 iPhone screenshots shown at 0.33 (398×865 screen, 13 px bezel). `phone_kit.py` implements all of it.

## Stage

- Brand ground (solid), a lighter patch behind the phone (radial, ~60%), phone centred at x=1240, top 40 px, so the bottom 150 px stays free for captions.
- **Left zone** x 120–880 for titles, numbers and lists. The camera never lets the phone's left edge cross x≈905 (`TITLE_ZONE_RIGHT`).
- Worlds: the brand stage for product beats; a prop world for "the old way" (a notebook, bills, a spreadsheet — drawn props are fine because they don't claim to be the product); a brand-colour world for the end card.

## Camera

- One wrapper per scene, `transform-origin: 0 0`, tweened `x / y / scale`.
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

## Transitions (use 3–5 kinds, each caused by something on screen)

| Kind | Kit | Use |
|---|---|---|
| Whip | `whip_out()` / `whip_in()` | topic change |
| Zoom-through + flood | `zoom_through` + `flood(color, t, 0.3, 0, 1)`; next scene `flood(color, start, 0.35, 1, 0)` | a tap that opens the next feature |
| Carry | same phone continues, camera to zoom 1 at the seam | adjacent features |
| Iris from the tap | next host starts 0.35 s early (overlap in `SCENES`), root transparent, `clip-path: circle()` from the tap point | a button that opens a new section |
| Dip | `dip()` | a hard turn |
| Colour flood into the end card | `flood(brand, t, 0.4, 0, 1)` | the last seam |

## Captions

- One group at a time, 2–6 words, broken at punctuation and pauses ≥150 ms, timed from `timing.json` words. Text from the script (corrected to what is said), never Whisper's spelling.
- Bottom 52 px, main face 600 at 44 px, ink on a ground-coloured scrim sized to the text (`inline-block` inside a full-width `text-align:center` row — never `left:50%; translateX(-50%)`).
- Leave a caption out when the same words are already a title on screen (tagline, end card).

## End card

App icon (the phone can shrink into it), wordmark wipes in, Latin name, tagline lighting word by word on the voice, a sub-line, then the official App Store / Google Play badges. Hold ≥2.5 s after the last word.
