"""Kheti Hisab — 9:16 Reels/Shorts cut (36.1 s) of the Hindi trailer.

Run from the project root:  python3 tools/build.py   (needs tools/phone_kit.py)

The voiceover is five voice-continuous pieces of the 16:9 master (assets/audio/segments.json).
Times below are written on the MASTER clock and mapped with V(), so they match the master's
timing.json word times; regions are screenshot pixels (1206 x 2622). Portrait layout: title and
caption at the top, a large phone (scale 0.5) below, clear of the platform's bottom-right buttons.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import phone_kit as K  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
SEG = json.loads((ROOT / "assets/audio/segments.json").read_text())
TOTAL = SEG["total"]


def V(t):
    """Master-clock seconds -> vertical-clock seconds."""
    for s in SEG["segments"]:
        if s["orig_start"] - 0.001 <= t <= s["orig_end"] + 0.001:
            return round(t - s["orig_start"] + s["v_start"], 3)
    raise ValueError(f"{t} is not in any segment")


COLORS = {
    "ground": "#F6EFE7", "patch": "#FBF7F1", "ink": "#1B2620", "ink2": "#5C6B62",
    "accent": "#E8A23A", "alert": "#C0412A", "brand": "#1F6B4B",
    "green": "#1F6B4B", "green2": "#184F39", "clay": "#C25A3A", "desk": "#E9DCC6",
}
B = [s["v_start"] for s in SEG["segments"]] + [TOTAL]
SCENES = [("v1", B[0], B[1]), ("v2", B[1], B[2]), ("v3", B[2], B[3]), ("v4", B[3], B[4]), ("v5", B[4], B[5])]
SHOTS = {
    "home": "01-home--01-home.png",
    "cat": "02-entries--21-add-expense-category-picker.png",
    "walk": "rec--expense-walk.mp4",
    "exp6400": "rec--expense-6400.png",
    "offentry": "rec--offline-entry.mp4",
    "offhome": "rec--offline-home.png",
}
FONTS = [
    ("Noto Sans Devanagari", "NotoSansDevanagari-SemiBold.ttf", 600),
    ("Noto Sans Devanagari", "NotoSansDevanagari-Bold.ttf", 700),
    ("Noto Sans Devanagari", "NotoSansDevanagari-ExtraBold.ttf", 800),
    ("Bricolage Grotesque", "BricolageGrotesque-ExtraBold.ttf", 800),
    ("Kalam", "Kalam-Bold.ttf", 700),
]
W, H = 1080, 1920
K.setup(root=ROOT, total=TOTAL, scenes=SCENES, shots=SHOTS, colors=COLORS, fonts=FONTS, lang="hi",
        font_main="'Noto Sans Devanagari', sans-serif",
        font_display="'Bricolage Grotesque', 'Noto Sans Devanagari', sans-serif",
        width=W, height=H, scale=0.5, bezel=20, phone_center_x=540, phone_top=560, screen_radius=88,
        title_zone_right=0, frame={"cx_min": 540, "cy": 1200, "max_w": 1000, "max_h": 1100, "right_max": 1060},
        lift_box=(40, 620, 1040, 1500), lift_dy=-80)
from phone_kit import *  # noqa: E402,F401,F403
C = COLORS
TX, TW = 80, 920   # title zone: x, width (y 120-410); caption band y ~435-505


# =====================================================================================
# v1 — hook: the notebook (master 0.0-1.98)
# =====================================================================================
def build_v1():
    sc = Scene("v1")
    lines = ["बीज (गेहूं) – ₹ ???", "खाद – ₹6,400 – दिया?", "मंडी – कपास 800 kg × ₹68 = ?", "डीज़ल – ₹1,200 (दिया?)", "गीता – 10 दिन मजदूरी – ?"]
    notes = "".join(f'<div class="hand" style="top:{620 + i * 120}px">{t}</div>' for i, t in enumerate(lines))
    sc.css.append(f"""
    @font-face {{ font-family:'Kalam'; src:url('assets/fonts/Kalam-Bold.ttf'); font-weight:700; }}
    #v1-paper {{ position:absolute; inset:0; background-color:#FAF5E8;
      background-image: linear-gradient(90deg, transparent 98px, rgba(192,65,42,0.45) 98px, rgba(192,65,42,0.45) 101px, transparent 101px),
        repeating-linear-gradient(180deg, transparent 0 118px, rgba(78,110,158,0.28) 118px 120px);
      background-position: 0 0, 0 60px; }}
    #v1-cam {{ position:absolute; left:0; top:0; width:{W}px; height:{H}px; transform-origin:0 0; }}
    .hand {{ position:absolute; left:130px; font-family:'Kalam'; font-weight:700; font-size:66px; color:#23305C; white-space:nowrap; }}
    #v1-circ {{ position:absolute; left:455px; top:600px; overflow:visible; }}
    #v1-circ path {{ stroke-dasharray:900; stroke-dashoffset:900; }}
    #v1-slip {{ position:absolute; left:560px; top:1290px; width:420px; padding:30px 34px; background:#FFFDF7; font-family:'Kalam';
      font-weight:700; font-size:44px; line-height:1.5; color:#2B2B2B; box-shadow:0 18px 40px rgba(27,38,32,0.22); opacity:0; }}
    """)
    stage = (f'<div id="v1-cam" data-layout-allow-overflow data-layout-allow-overlap data-layout-ignore><div id="v1-paper"></div>{notes}'
             '<svg id="v1-circ" width="320" height="160" viewBox="0 0 300 150"><path d="M30 80 C 30 20, 270 15, 275 70 S 60 140, 40 70" '
             'fill="none" stroke="#C0412A" stroke-width="7" stroke-linecap="round"/></svg>'
             '<div id="v1-slip">किसान खाद भंडार<br/>कुल ₹6,400<br/><span style="color:#C0412A">बाकी: ____</span></div></div>')
    sc.js.append("""
    tl.fromTo('#v1-cam', {scale:1.0, x:0, y:0}, {scale:1.06, x:-30, y:-40, duration:1.98, ease:'none'}, 0);
    tl.fromTo('#v1-circ path', {strokeDashoffset:900}, {strokeDashoffset:0, duration:0.55, ease:'power2.inOut'}, 0.45);
    tl.fromTo('#v1-slip', {x:500, rotation:4, opacity:0}, {x:0, rotation:-6, opacity:1, duration:0.5, ease:'expo.out'}, 0.85);
    """)
    sc.sweep_out(C["green"])
    sc.write(stage, ground="#FAF5E8")


# =====================================================================================
# v2 — the reveal (master 12.3-17.05)
# =====================================================================================
def build_v2():
    sc = Scene("v2")
    T = lambda t: V(t)  # noqa: E731
    sc.screen("home", T(12.3), T(17.05))
    sc.cam_set({"x": 0, "y": 900, "scale": 1})
    sc.cam_to(T(12.3), BASE, dur=0.6, ease="power3.out", blur=True)
    sc.sweep_in(C["green"])
    sc.html.append(f'<img id="v2-icon" class="icon" src="assets/brand/app-icon.png" alt="" style="left:{TX}px;top:150px;width:150px;height:150px" />')
    sc.js.append(f"tl.fromTo('#v2-icon', {{opacity:0, scale:0.6}}, {{opacity:1, scale:1, duration:0.45, ease:'expo.out'}}, {sc.t(T(14.85))});")
    sc.title("v2-name", "खेती हिसाब", T(15.2), None, x=260, y=135, size=110, color=C["green"])
    sc.title("v2-latin", "Kheti Hisab", T(15.55), None, x=266, y=285, size=54, font="display", style="line")
    sc.tap(T(16.45), 405, 1215, 150, 270)
    sc.cam_to(T(16.6), zoom_through(BASE, 480, 1350, 4.0), dur=0.4, ease="power3.in")
    sc.flood(C["clay"], T(16.75), 0.3, 0, 1)
    sc.write(phone_stage(sc))


# =====================================================================================
# v3 — expense, the real recording (master 22.6-33.35)
# =====================================================================================
def build_v3():
    sc = Scene("v3")
    T = V
    sc.screen("cat", T(22.6), T(25.65))
    sc.screen("walk", T(25.4), T(33.35), enter="fade")
    sc.cam_set(BASE)
    sc.cam_to(T(23.0), cam(45, 810, 1110, 1425), dur=0.6)
    sc.flood(C["clay"], T(22.6), 0.35, 1, 0)
    sc.ol(T(22.8), (435, 825, 270, 435))
    sc.ol(T(23.75), (435, 1305, 270, 435))
    sc.ol(T(24.08), (810, 1305, 345, 435))
    sc.ol(T(24.62), (435, 1800, 270, 435))
    sc.ol(T(25.1), (435, 1305, 270, 435))
    sc.tap(T(25.2), 435, 1305, 270, 435)
    sc.ol(T(25.4))
    sc.cam_to(T(25.5), cam(45, 560, 1110, 760), dur=0.6)
    sc.tap(T(27.5), 60, 1110, 1080, 201)
    sc.lift("exp6400", T(28.3), T(29.6), (60, 1110, 1080, 201), k=1.6)
    sc.cam_to(T(29.65), cam(45, 360, 1110, 420), dur=0.6)
    sc.ol(T(29.95), (45, 375, 1110, 150))
    sc.ol(T(30.6))
    sc.cam_to(T(30.6), {"x": 0, "y": -130, "scale": 1}, dur=0.6)   # raise the save button above the platform's bottom overlay
    sc.tap(T(31.3), 45, 2175, 1110, 141)
    sc.cam_to(T(31.75), cam(54, 400, 1101, 470), dur=0.6)
    sc.ol(T(32.3), (600, 630, 510, 170))
    sc.ol(T(32.9))
    sc.items("v3-l", [("खर्चा लिखो", T(27.55)), ("फसल से जोड़ो", T(29.45)), ("हिसाब साफ रखो", T(31.45))], T(33.0),
             x=TX, y=110, size=66, gap=1.4, font="main", style="blur")
    sc.css.append("#v3-l { font-weight:800; }")
    sc.sweep_out(C["green"])
    sc.write(phone_stage(sc))


# =====================================================================================
# v4 — offline, the real no-network recording (master 78.05-88.15)
# =====================================================================================
def build_v4():
    sc = Scene("v4")
    T = V
    sc.screen("offentry", T(78.05), T(88.15))
    sc.open_on((800, 40, 350, 110), hold=0.55)
    sc.sweep_in(C["green"])
    sc.cam_to(T(80.2), {"x": 0, "y": -130, "scale": 1}, dur=0.5)
    sc.tap(T(80.85), 45, 2175, 1110, 141)
    sc.lift("offhome", T(82.4), T(87.3), (600, 630, 510, 170), k=2.0)
    bars = "".join(f'<div class="bar" id="v4-b{i}" style="left:{i*46}px;height:{40+i*34}px"></div>' for i in range(4))
    sc.html.append(f'<div id="v4-sig" class="sig" style="left:{TX + 10}px;top:200px">{bars}<div id="v4-x" class="sig-x">×</div></div>')
    for i in range(4):
        sc.js.append(f"tl.fromTo('#v4-b{3-i}', {{opacity:1}}, {{opacity:0.15, duration:0.12}}, {sc.t(T(78.5 + i*0.35))});")
    sc.js.append(f"tl.fromTo('#v4-x', {{opacity:0, scale:1.6}}, {{opacity:1, scale:1, duration:0.25, ease:'expo.out'}}, {sc.t(T(80.0))});"
                 f"tl.set('#v4-sig', {{opacity:1}}, 0);"
                 f"tl.fromTo('#v4-sig', {{opacity:1}}, {{opacity:0, duration:0.18, immediateRender:false}}, {sc.t(T(81.8))});")
    sc.title("v4-t", "Works Offline", T(82.0), None, x=TX, y=120, size=104, font="display", color=C["green"], style="line", width=TW)
    sc.title("v4-t2", "आपका हिसाब आपके फोन में रहता है", T(85.2), None, x=TX, y=270, size=50, weight=700, style="grey", width=TW)
    sc.sweep_out(C["green"])
    sc.write(phone_stage(sc))


# =====================================================================================
# v5 — end card (master 112.95-121.5)
# =====================================================================================
def build_v5():
    sc = Scene("v5")
    T = V
    sc.screen("home", T(112.95), T(121.5))
    sc.cam_set(BASE)
    s_end = 260 / PW
    pcx, pcy = PL + PW / 2, PT + PH / 2
    sc.js.append(f"tl.fromTo('#v5-cam', {{x:0, y:0, scale:1, opacity:1}}, {{x:{r(540 - s_end * pcx)}, y:{r(560 - s_end * pcy)}, scale:{r(s_end)}, duration:0.6, ease:'power3.inOut', immediateRender:false}}, {sc.t(T(113.05))});"
                 f"tl.fromTo('#v5-cam', {{opacity:1}}, {{opacity:0, duration:0.2, immediateRender:false}}, {sc.t(T(113.5))});"
                 f"tl.fromTo('#v5-mark', {{opacity:0, scale:0.92}}, {{opacity:1, scale:1, duration:0.4, ease:'expo.out'}}, {sc.t(T(113.5))});"
                 f"tl.fromTo('#v5-word', {{opacity:1, clipPath:'inset(-40% 100% -40% 0)'}}, {{opacity:1, clipPath:'inset(-40% 0% -40% 0)', duration:0.5, ease:'power3.out'}}, {sc.t(T(113.95))});"
                 f"tl.fromTo('#v5-latin', {{opacity:0, filter:'blur(8px)'}}, {{opacity:1, filter:'blur(0px)', duration:0.2}}, {sc.t(T(114.35))});"
                 f"tl.set('#v5-tag', {{opacity:1}}, {sc.t(T(116.1))});"
                 f"tl.fromTo('#v5-tag .w', {{color:'rgba(246,239,231,0.22)'}}, {{color:'#F6EFE7', duration:0.12, stagger:0.45, ease:'none'}}, {sc.t(T(116.1))});"
                 f"tl.fromTo('#v5-sub', {{opacity:0, filter:'blur(8px)'}}, {{opacity:1, filter:'blur(0px)', duration:0.2}}, {sc.t(T(117.3))});"
                 f"tl.fromTo('#v5-badges', {{opacity:0, y:40}}, {{opacity:1, y:0, duration:0.45, ease:'expo.out'}}, {sc.t(T(117.7))});")
    sc.css.append(f"""
    #v5-g {{ position:absolute; inset:0; background: radial-gradient(ellipse 1300px 1800px at 50% 40%, {C['green']} 0%, {C['green2']} 100%); }}
    #v5-mark {{ position:absolute; left:410px; top:430px; width:260px; height:260px; border-radius:58px; box-shadow:0 30px 60px rgba(0,0,0,0.25); opacity:0; }}
    .v5-c {{ position:absolute; left:0; width:{W}px; text-align:center; opacity:0; }}
    #v5-word {{ top:740px; font-family:var(--font-main); font-weight:800; font-size:132px; color:#F6EFE7; line-height:1.2; }}
    #v5-latin {{ top:935px; font-family:var(--font-display); font-weight:800; font-size:60px; color:{C['accent']}; }}
    #v5-tag {{ top:1080px; font-family:var(--font-main); font-weight:800; font-size:72px; color:#F6EFE7; }}
    #v5-sub {{ top:1200px; font-family:var(--font-main); font-weight:700; font-size:42px; color:rgba(246,239,231,0.82); }}
    #v5-badges {{ top:1320px; display:flex; justify-content:center; gap:30px; }}
    #v5-badges img {{ height:92px; }}
    """)
    stage = ('<div id="v5-g"></div>' + phone_stage(sc, patch=False)
             + '<img id="v5-mark" src="assets/brand/app-icon.png" alt="" />'
             + '<div id="v5-word" class="v5-c">खेती हिसाब</div><div id="v5-latin" class="v5-c">Kheti Hisab</div>'
             + f'<div id="v5-tag" class="v5-c">{sc.words_html("हर किसान का अपना हिसाब")}</div>'
             + '<div id="v5-sub" class="v5-c">अपनी खेती • अपना रिकॉर्ड • अपना हिसाब</div>'
             + '<div id="v5-badges" class="v5-c"><img src="assets/brand/app-store.svg" alt="Download on the App Store" />'
             + '<img src="assets/brand/google-play.png" alt="Get it on Google Play" /></div>')
    sc.write(stage, ground=C["green"])


CAPS_MASTER = [
    (0.15, 1.95, "बीज का खर्चा कहाँ लिखा था…?"),
    (12.6, 14.75, "अब खेती का हिसाब होगा आसान।"), (14.8, 17.0, "ये है Kheti Hisab —"),
    (22.8, 23.7, "बीज खरीदा?"), (23.75, 25.08, "खाद, दवाई, डीज़ल"), (25.11, 27.3, "या कोई और खर्चा हुआ?"),
    (27.54, 29.35, "बस उसी समय entry करो।"), (29.4, 30.72, "और खर्चा सही फसल के"), (30.76, 32.8, "हिसाब में जुड़ जाएगा।"),
    (78.3, 80.66, "लेकिन खेत में network नहीं हो तो?"), (80.7, 81.96, "कोई दिक्कत नहीं।"),
    (82.0, 84.9, "Kheti Hisab offline भी काम करता है।"),
]
SFX = [
    ("sfx-w1", "whoosh-short.mp3", round(B[1] - 0.45, 2), 0.3), ("sfx-c1", "click-soft.mp3", V(16.45), 0.35),
    ("sfx-c2", "click-soft.mp3", V(25.2), 0.3), ("sfx-c3", "click-soft.mp3", V(31.3), 0.35),
    ("sfx-p1", "pop.mp3", V(28.35), 0.3), ("sfx-w2", "whoosh-short.mp3", round(B[3] - 0.45, 2), 0.3),
    ("sfx-c4", "click-soft.mp3", V(80.85), 0.35), ("sfx-p2", "pop.mp3", V(82.45), 0.3),
    ("sfx-w3", "whoosh-short.mp3", round(B[4] - 0.45, 2), 0.3),
]

if __name__ == "__main__":
    for f in (build_v1, build_v2, build_v3, build_v4, build_v5):
        f()
    K.build_captions([(V(a), V(b), txt) for a, b, txt in CAPS_MASTER], bottom=H - 505, size=46)
    # "Fretless" by Kevin MacLeod (incompetech.com), CC BY 4.0. Enters on a bar line with the reveal (v2),
    # ducked under the voice, lifts after the last word for the end card.
    m0 = B[1]
    last_word = V(118.76) - m0
    K.build_index(sfx=SFX, vo_volume=0.85, music="assets/audio/music-fretless.mp3", music_start=m0, music_media_start=16.8,
                  music_lane=[(0, 0), (0.35, 0.17), (round(last_word, 2), 0.17), (round(last_word + 0.7, 2), 0.42)], music_fade_out=1.4)
    print("built", len(SCENES), "scenes, total", TOTAL)
