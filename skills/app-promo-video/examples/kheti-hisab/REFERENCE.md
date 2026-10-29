# REFERENCE — style review for the Kheti Hisab trailer (2026-10-29)

Reviewed with `ref_review.py`: 6 contact sheets + 3 motion strips (files in `inputs/kheti-hisab/refs/*/review/`).

| # | Video | Length | What it is |
|---|---|---|---|
| 1 | Groundswell – App Explainer (Vidico) | 0:59 | Large phone on off-white; a giant brand-green rounded shape sweeps in as a transition; key UI cards pop out of the phone beside it with a check badge; the balance number counts up; two-line bold titles with one accent word; dark-green end card with store badges |
| 2 | Wellio – SaaS explainer (Pixelblue) | 0:43 | Glass cards and green/yellow mesh blur, stock photos of people, fast cuts (9.7/min), extreme crops |
| 3 | Property Toolbox – app walkthrough | 1:27 | Step-by-step walkthrough of real screens: one action per beat, big phone cropped by the frame, list rows lift out of the phone and grow past the bezel, two-line titles with one bold green word, no hard cuts (all moves) |

## Pick for Kheti Hisab

**Base: #3's walkthrough grammar + #1's brand moves.** Farmers need to see *what to tap and what happens*, one step at a time (#3). #1 adds warmth and clear "result" moments without clutter. #2 is left out: stock people and glass/mesh gradients say "generic SaaS", not "my farm".

## TAKE (grammar → our setting)

| From | Grammar | Our version | |
|---|---|---|---|
| #3, #1 | Key UI element **lifts out of the phone**, ~1.2–1.5× bigger, breaking past the bezel, soft shadow, 0.5–0.6 s ease-out with blur at the fastest frame | `lift()`: the real screenshot region is re-drawn crisp at ~2.3×, rises from its place in the phone, holds while the voice names it, then settles back. Used once per feature for its result: amount, लेना/देना, बकाया, contract balance, offline card, profit | measured |
| #1 | A **check badge** pops on the lifted card's corner | Small brand-green check on the lifted card, 0.25 s pop | measured |
| #1 | The key number **counts up** | Left-zone amounts count up to the real value (₹1,19,250 …) in 0.6 s, Indian digit grouping | measured |
| #1 | A **giant rounded brand shape sweeps** across the frame as the transition (~0.6 s, diagonal) | `sweep_out()` / `sweep_in()` in brand green #1F6B4B at the big world changes: notebook → app, attendance → farm work, contract → offline, report → end card | measured |
| #3 | **Show the tap**: the pointer travels to the control and presses it | A soft finger-tip dot (not a ring) arrives 0.3 s before each tap and presses with the iOS highlight | measured (theirs is a desktop cursor) |
| #3, #1 | Two-line titles, **one keyword in brand colour** | `title(..., accent=[...])`: one word per title in green (or clay for a problem word) | measured |
| #3 | Phone large, may be cropped by the frame | Already: phone 82% of height, zooms crop it | measured |
| #1 | Dark-green end card: mark, name, tagline, both store badges | Already | measured |

## LEAVE (not copied)

- #2's stock people, glass cards and mesh gradients; any tilted/3D phones (our UI stays flat and readable).
- #3's yellow/green corner glows and desktop cursor; #1's off-white/teal palette.
- Their copy, music, logos, layouts — every colour, font and word comes from Kheti Hisab.

## Changes to SPEC.md

- MOTION: add lift (0.5 s `expo.out` up, 0.35 s `power2.in` back), check pop 0.25 s, count-up 0.6 s `power2.out`, sweep 0.45 s `power2.in` out / 0.5 s `power2.out` in, finger dot 0.3 s lead.
- SHOTS: lifts at 27.6 (₹6,400), 39.1 (लेना/देना), 50.7 (बकाया ₹2,400), 72.7 (₹82,000 बाकी), 82.6 (offline card), 107.6 (profit). Sweeps at 11.9, 57.0, 77.8, 109.0.
