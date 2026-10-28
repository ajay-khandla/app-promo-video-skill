"""Build script skeleton for an app trailer. Copy to <project>/tools/build.py next to phone_kit.py.

Fill SCENES from timing.json (one scene per sentence group), SHOTS with your screenshot files
(copied into assets/screens/), and write one build_sN() per scene. All times are absolute
seconds on the voiceover; all regions are screenshot pixels (read them off grid_sheets.sh).
Full worked example: examples/kheti-hisab/build.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import phone_kit as K  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
TOTAL = 30.0  # voiceover length + ~2.5 s end-card hold

COLORS = {
    "ground": "#F6EFE7",   # stage background
    "patch": "#FBF7F1",    # lighter patch behind the phone
    "ink": "#1B2620",      # text
    "ink2": "#5C6B62",     # secondary text (number labels)
    "accent": "#E8A23A",   # focus outline, Pro tag
    "alert": "#C0412A",    # warnings / due amounts
    "brand": "#1F6B4B",    # brand colour (end card, underline)
}

SCENES = [  # (id, start, end)
    ("s1", 0.0, 10.0),
    ("s2", 10.0, TOTAL),
]

SHOTS = {  # key -> file in assets/screens/
    "home": "home.png",
    "detail": "detail.png",
}

FONTS = [  # (family, file in assets/fonts/, weight)
    ("Inter", "Inter-Bold.ttf", 700),
    ("Inter", "Inter-ExtraBold.ttf", 800),
]

K.setup(root=ROOT, total=TOTAL, scenes=SCENES, shots=SHOTS, colors=COLORS, fonts=FONTS, lang="en",
        font_main="'Inter', sans-serif", font_display="'Inter', sans-serif")
from phone_kit import *  # noqa: E402,F401,F403


def build_s1():
    sc = Scene("s1")
    sc.screen("home", 0.0, 6.0)
    sc.screen("detail", 5.8, 10.0, enter="push")
    sc.cam_set({**CENTER, "y": 760})
    sc.cam_to(0.0, CENTER, dur=0.6, ease="power3.out", blur=True)      # phone rises
    sc.cam_to(1.8, BASE)                                                # phone to the right
    sc.title("s1-t", "Your app name", 2.0, 5.5, size=110, color=COLORS["brand"])
    sc.cam_to(3.0, cam(54, 400, 1100, 600))                             # punch into a card
    sc.ol(3.4, (54, 400, 1100, 600))                                    # on the spoken word
    sc.ol(5.5)
    sc.tap(5.6, 400, 1200, 300, 200)                                    # tap that opens 'detail'
    sc.cam_to(6.0, cam(54, 300, 1100, 500))
    sc.amount("s1-a", "Saved this month", "$1,240", COLORS["brand"], 7.0, 9.6)
    sc.whip_out()
    sc.write(phone_stage(sc))


def build_s2():
    sc = Scene("s2")
    sc.screen("home", 10.0, TOTAL)
    sc.open_on((54, 1000, 1100, 800))   # full phone first, then zoom into the region
    sc.whip_in()                         # lands on the full phone
    sc.title("s2-t", "Download today", 11.0, None, size=96)
    sc.write(phone_stage(sc))


CAPTIONS = [  # (start, end, text) from timing.json words; leave out lines that are titles
    (0.2, 2.0, "First caption line"),
]

SFX = [  # (id, file in assets/sfx/, time, volume)
    ("sfx-w1", "whoosh-short.mp3", 9.65, 0.3),
]

if __name__ == "__main__":
    build_s1()
    build_s2()
    K.build_captions(CAPTIONS)
    K.build_index(sfx=SFX)  # music="assets/audio/music.mp3" when there is a track
    print("built", len(SCENES), "scenes")
