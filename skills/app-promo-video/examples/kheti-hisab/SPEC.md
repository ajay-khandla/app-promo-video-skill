# SPEC — Kheti Hisab Hindi trailer (16:9 master)

GOAL:    A farmer watching on their phone sees their own messy notebook replaced by real Kheti Hisab screens, scene by scene, and ends knowing the name, the tagline and where to download it.
OUTPUT:  HyperFrames, 1920 × 1080, 30 fps.
TIME:    121.5 s × 30 = 3645 frames. The voiceover is the clock (`assets/audio/voiceover.wav`, 118.76 s, word timings in `assets/audio/timing.json`). No music yet (no track supplied, no HeyGen sign-in).

LOOK:    Brand-native, taken from the app's code (lib/theme/app_colors.dart).
         - Ground: cream #F6EFE7 solid, with a lighter patch #FBF7F1 at 60% behind the phone. S1 desk ground #E9DCC6. S11 green #1F6B4B → #184F39 radial.
         - Ink #1B2620, secondary #5C6B62. Semantic accents only where the app uses them: income/profit green #1F6B4B, expense clay #C25A3A, pending marigold #B07908, due red #C0412A. Marigold #E8A23A only for the focus outline and the Pro tag.
         - Type: Hindi display Noto Sans Devanagari ExtraBold 800, 84 px (7.8% of the height), tracking 0. Amounts: Bricolage Grotesque ExtraBold 800, 132 px. Latin words inside Hindi lines use Bricolage. Captions: Noto Sans Devanagari SemiBold 44 px.
         - Medium: real product UI. An iPhone is a 13 px #111 bezel, a 58 px screen radius and a contact shadow 0 30 px 60 px rgba(27,38,32,0.18) around the real 1206 × 2622 screenshot at 0.33 (398 × 865). S1 only: ruled notebook paper #FAF5E8, blue rules rgba(78,110,158,0.28) every 66 px, red margin line, Kalam Bold handwriting in #23305C ink, paper bill slips.

OBJECTS: The farmer's notebook (khata) and bills (S1). One iPhone carrying real Kheti Hisab screens (S2–S10). A second phone (S9 "new phone"). App icon, wordmark and the official App Store / Google Play badges (S11).

MOTION:  - Camera = one wrapper per scene: `scale` + `x/y` with origin 0 0. Moves 0.6 s `power2.inOut`; zoom-through 0.45 s `power3.in`.
         - Screen changes: navigation 0.42 s push (in `power3.out`, out to −30%); state change 0.22 s crossfade.
         - Tap: an iOS press highlight, rgba(27,38,32,0.14), 0.06 s in and 0.2 s out. No click rings.
         - Focus outline: one marigold 2.2 px stroke per scene that travels from target to target (0.35 s `expo.out`).
         - Titles land and hold dead still. Entrances vary: per-word blur 6 px → 0 at 0.067 s stagger; per-word grey → ink; whole-line blur 8 → 0. Amounts land with blur 10 → 0 and y 24 → 0 in 0.3 s `expo.out`. Exits are blur out in 0.18 s.

         - From REFERENCE.md (2026-10-29): every scene opens on the full phone, then zooms; one result per feature lifts out of the phone (0.5 s expo.out up, 0.35 s power2.in back, check badge 0.3 s back.out) while its number counts up (0.6 s); a finger dot leads every tap by 0.3 s; brand-green sweeps at 11.85, 77.6 and 108.95.

SHOTS (absolute seconds; anchor word in quotes):
  S1  0.0–12.3  Desk world. The camera drifts over the notebook: "बीज" line circled in red (1.0), the "खाद" bill slip slides in (2.0), "मंडी" line (5.5). Pull back to the whole desk at 8.6. Title "खेती का हिसाब इतना मुश्किल क्यों?" lands at 9.0. Notebook whips off left at 11.85.
  S2 12.3–22.6  The phone rises (home screen). "ये है Kheti Hisab" (14.8): phone moves right, icon + "खेती हिसाब" + "Kheti Hisab" land left. "डिजिटल हिसाब किताब" (17.1): punch to the season card. Tagline at 19.5. Punch to quick actions; tap the खर्च tile (21.4) and zoom through into a clay flood.
  S3 22.6–33.35 The clay flood clears onto the category picker. Outline travels बीज → उर्वरक → कीटनाशक → बिजली/डीज़ल on the spoken words. Tap उर्वरक → filled form (₹6,400). "entry करो" (27.5): the amount. "सही फसल" (29.4): the crop row. Save (31.3) → the ₹6,400 उर्वरक entry in the Krishna Agro Store account. Left lines on 27.5 / 29.4 / 31.4: "खर्चा लिखो • फसल से जोड़ो • हिसाब साफ रखो". Whip out.
  S4 33.35–44.65 Whip in on the sale form (800 kg × ₹68 = ₹54,400). "पूरे पैसे नहीं मिले" (35.05): pending state, बाकी ₹54,400. "बताता है" (37.1): Money-owed report. "लेना" (39.07): outline + left "लेना ₹1,19,250". "देना" (41.06): left "देना ₹16,416". "बाकी" (42.59): the list. Pull back.
  S5 44.65–57.15 Carry (same stage): push to the attendance register. Tap Geeta's हाजिरी → day sheet; outline हाजिर (47.14) → आधा दिन (49.09). "भुगतान बाकी" (50.19): Ramu's बकाया ₹2,400 + left amount. "अटेंडेंस" (51.77): calendar; left list "Attendance • मजदूरी • बाकी भुगतान". Tap हाजिरी लगाएँ → iris.
  S6 56.8–68.6  The iris opens on the activity type grid; outline छिड़काव → सिंचाई → खाद, and the left list "Spraying • Irrigation • Fertiliser • Farm Work" grows on the words. History (61.0). "अगला काम" (62.53): the activity detail repeat/reminder card. Pull back; Pro tag "नया काम और रिमाइंडर — Pro". Whip out.
  S7 68.6–78.05 Whip in on contract overview money table. The left list grows on the words: "Contract" (68.84), "Advance" (70.55, पेशगी row), "Instalments" (71.74, payments tab किस्त row), "Balance" (72.68, ₹82,000 लेने हैं). "एक जगह" (74.49): back to the overview, pull back. Dip cut.
  S8 78.05–88.15 Left: a signal-bars pictogram loses its bars (78.3–80.0). The phone shows the pending expense form; "कोई दिक्कत नहीं" save tap (80.9) → Cloud Sync "इंटरनेट का इंतज़ार — 3 बदलाव इसी फ़ोन में सहेजे हैं". Title "Works Offline" (82.0). Line "आपका हिसाब आपके फोन में रहता है" (85.2). Carry out.
  S9 88.15–99.25 Cloud Sync "सिंक पूरा" card; title "Cloud Sync with Pro" (88.7). "नया फोन लिया?" (94.3): phone A slides out left, phone B rises on onboarding "पहले खेती हिसाब इस्तेमाल किया है?"; outline "क्लाउड सिंक से मेरी बुक लाएँ" (95.6); title "नया फोन • वही हिसाब". "फिर से खोल" (97.4): the book opens on home. Tap रिपोर्ट → zoom through.
  S10 99.25–109.0 Reports list; tap सीज़न मुनाफ़ा-नुकसान (100.6) → Season P&L. "आमदनी" (103.62): outline बिक्री, left "Income ₹2,92,250". "खर्चा" (105.28): "Expense ₹1,09,682". Hold 0.4 s, then "बचा" (107.68): punch to the profit, left "Profit ₹1,82,568" — the payoff. Green flood.
  S11 109.0–121.5 Green world. The phone (home screen) sits right; on "डाउनलोड" (113.0) it shrinks into the app icon, which lands left of centre. Wordmark "खेती हिसाब" wipes in (113.9), "Kheti Hisab" (114.2), tagline "हर किसान का अपना हिसाब" grey→cream on the words (115.3–118.0), "अपनी खेती • अपना रिकॉर्ड • अपना हिसाब" (117.2), badges rise (117.6). Hold to 121.5.
  CAPTIONS: Hindi, one group at a time, bottom 56 px on a cream scrim sized to the text. Off where the same words are a title (S2 tagline, S8 last line, S11 from 115.3).

LIFTS:   27.6 ₹6,400 (S3) · 38.95 लेना/देना (S4) · 50.55 बकाया (S5) · 72.7 ₹82,000 लेने हैं (S7) · 82.4 offline card (S8) · 107.55 profit card (S10).
BANNED:  dark void; glow, particles, gradients as decoration; serif display or mono labels; pill chips; three cards in a row; a title over a dimmed screenshot; the logo docked in a corner; click rings; floating or breathing loops; drawn or invented app UI (every screen is a real screenshot); invented numbers (all amounts come from the screens); phone UI tilted in 3D.

QA:      1.0 (bills circled, not empty frame), 9.5 (title readable over the desk), 15.5 (lockup + phone), 23.5 (outline on बीज), 39.6 (लेना amount readable), 47.5 (हाजिर outlined), 58.5 (list + outline), 72.0 (Instalments), 83.0 (Works Offline + offline card), 95.8 (new phone), 107.9 (profit payoff), 119 (end card complete). Phone width 360 px: every amount readable.
