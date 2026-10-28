"""Kheti Hisab Hindi trailer — worked example for the app-promo-video skill.

Run from the project root:  python3 tools/build.py
Needs tools/phone_kit.py (copied from the skill's scripts/).

Shot data for an 11-scene, 121.5 s, 16:9 product trailer driven by a Hindi voiceover.
All times are absolute seconds on the voiceover clock (assets/audio/timing.json);
all regions are in the screenshot's own pixels (1206 x 2622).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import phone_kit as K  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
TOTAL = 121.5

COLORS = {
    # required by the kit
    "ground": "#F6EFE7", "patch": "#FBF7F1", "ink": "#1B2620", "ink2": "#5C6B62",
    "accent": "#E8A23A", "alert": "#C0412A", "brand": "#1F6B4B",
    # this film's own (from the app's theme file)
    "green": "#1F6B4B", "green2": "#184F39", "clay": "#C25A3A", "pending": "#B07908",
    "due": "#C0412A", "marigold": "#E8A23A", "desk": "#E9DCC6",
}

SCENES = [  # id, start, end (absolute seconds). s6 overlaps s5 by 0.35 s for the iris.
    ("s1", 0.0, 12.3), ("s2", 12.3, 22.6), ("s3", 22.6, 33.35), ("s4", 33.35, 44.65),
    ("s5", 44.65, 57.15), ("s6", 56.8, 68.6), ("s7", 68.6, 78.05), ("s8", 78.05, 88.15),
    ("s9", 88.15, 99.25), ("s10", 99.25, 109.4), ("s11", 109.4, TOTAL),
]

SHOTS = {
    "home": "01-home--01-home.png",
    "cat": "02-entries--21-add-expense-category-picker.png",
    "expfilled": "02-entries--23-add-expense-filled.png",
    "incfilled": "02-entries--13-add-income-filled.png",
    "incpending": "02-entries--14-add-income-pending-due-date.png",
    "exppending": "02-entries--24-add-expense-pending.png",
    "vendor": "04-parties--04-vendor-account.png",
    "owed": "08-reports--06-money-owed.png",
    "reports": "08-reports--01-reports.png",
    "pl": "08-reports--02-season-profit-and-loss.png",
    "register": "06-attendance--01-register.png",
    "markday": "06-attendance--04-mark-a-day.png",
    "calendar": "06-attendance--02-worker-calendar.png",
    "acttype": "07-activities--04-add-activity.png",
    "acts": "07-activities--01-activities.png",
    "actdetail": "07-activities--02-activity-detail.png",
    "contract": "05-contracts--02-contract-overview.png",
    "payments": "05-contracts--03-contract-payments.png",
    "offline": "10-cloud-sync--10-state-offline.png",
    "synced": "10-cloud-sync--02-cloud-sync-up-to-date.png",
    "start": "13-onboarding--02-start.png",
}

FONTS = [
    ("Noto Sans Devanagari", "NotoSansDevanagari-SemiBold.ttf", 600),
    ("Noto Sans Devanagari", "NotoSansDevanagari-Bold.ttf", 700),
    ("Noto Sans Devanagari", "NotoSansDevanagari-ExtraBold.ttf", 800),
    ("Bricolage Grotesque", "BricolageGrotesque-ExtraBold.ttf", 800),
    ("Kalam", "Kalam-Bold.ttf", 700),
]

K.setup(root=ROOT, total=TOTAL, scenes=SCENES, shots=SHOTS, colors=COLORS, fonts=FONTS, lang="hi",
        font_main="'Noto Sans Devanagari', sans-serif",
        font_display="'Bricolage Grotesque', 'Noto Sans Devanagari', sans-serif")
from phone_kit import *  # noqa: E402,F401,F403
C = COLORS


# =====================================================================================
# S1 — the notebook
# =====================================================================================
def build_s1():
    sc = Scene("s1")
    lines = [
        ("n1", 250, "बीज (गेहूं) – ₹ ???"),
        ("n2", 382, "खाद – किसान खाद भंडार – ₹6,400"),
        ("n3", 514, "मंडी – कपास 800 kg × ₹68 = ?"),
        ("n4", 646, "डीज़ल – ₹1,200 (दिया?)"),
        ("n5", 778, "गीता – 10 दिन मजदूरी – ?"),
        ("n6", 910, "मोहन – ₹2,000 दिए / नहीं?"),
    ]
    notes = "".join(f'<div id="s1-{i}" class="hand" style="top:{y-62}px">{t}</div>' for i, y, t in lines)
    strikes = ('<div class="strike" style="left:330px;top:858px;width:560px;transform:rotate(-2deg)"></div>'
               '<div class="strike" style="left:330px;top:592px;width:430px;transform:rotate(1.5deg)"></div>')
    circle = ('<svg id="s1-circ" class="circ" style="left:595px;top:150px" width="300" height="150" viewBox="0 0 300 150">'
              '<path d="M30 80 C 30 20, 270 15, 275 70 S 60 140, 40 70" fill="none" stroke="#C0412A" stroke-width="7" stroke-linecap="round"/></svg>')
    query = '<div id="s1-q" class="redq" style="left:1200px;top:318px">दिया?</div>'
    slip1 = ('<div id="s1-slip1" class="slip" style="left:1450px;top:170px">'
             '<div class="slip-h">किसान खाद भंडार</div><div>उर्वरक (DAP) – 2 बोरी</div><div>कुल ₹6,400</div>'
             '<div class="slip-due">बाकी: ______</div></div>')
    slip2 = ('<div id="s1-slip2" class="slip" style="left:1500px;top:600px">'
             '<div class="slip-h">मंडी पर्ची</div><div>कपास – 800 kg</div><div>भाव ₹68</div><div class="slip-due">मिले: ?</div></div>')
    sc.css.append(f"""
    @font-face {{ font-family:'Kalam'; src:url('assets/fonts/Kalam-Bold.ttf'); font-weight:700; }}
    #s1-desk {{ position:absolute; inset:0; background:{C['desk']}; }}
    #s1-cam {{ position:absolute; left:0; top:0; width:{W}px; height:{H}px; transform-origin:0 0; }}
    #s1-paper {{ position:absolute; left:0; top:0; width:2500px; height:1400px; background-color:#FAF5E8;
      background-image: linear-gradient(90deg, transparent 258px, rgba(192,65,42,0.45) 258px, rgba(192,65,42,0.45) 261px, transparent 261px),
        repeating-linear-gradient(180deg, transparent 0 64px, rgba(78,110,158,0.28) 64px 66px);
      background-position: 0 0, 0 186px; box-shadow: 0 40px 80px rgba(27,38,32,0.25); border-radius:6px; }}
    .hand {{ position:absolute; left:320px; font-family:'Kalam'; font-weight:700; font-size:60px; color:#23305C; white-space:nowrap; }}
    .strike {{ position:absolute; height:5px; background:#23305C; border-radius:3px; opacity:0.85; }}
    .circ {{ position:absolute; overflow:visible; }}
    .redq {{ position:absolute; font-family:'Kalam'; font-weight:700; font-size:62px; color:#C0412A; transform:rotate(-6deg); white-space:nowrap; }}
    .slip {{ position:absolute; width:440px; padding:34px 36px; background:#FFFDF7; font-family:'Kalam'; font-weight:700;
      font-size:42px; line-height:1.5; color:#2B2B2B; box-shadow:0 18px 40px rgba(27,38,32,0.22); border-top:10px dotted #E9DCC6; }}
    .slip-h {{ font-size:46px; border-bottom:3px solid #2B2B2B; margin-bottom:10px; }}
    .slip-due {{ color:#C0412A; }}
    #s1-title {{ position:absolute; left:120px; top:110px; width:900px; font-family:var(--font-main); font-weight:800;
      font-size:84px; line-height:1.25; color:{C['ink']}; opacity:0; }}
    #s1-cream {{ position:absolute; inset:0; background:{C['ground']}; opacity:0; }}
    """)
    stage = (f'<div id="s1-desk"></div><div id="s1-cam" data-layout-allow-overflow data-layout-allow-overlap data-layout-ignore><div id="s1-paper">{notes}{strikes}{circle}{query}</div>'
             f'{slip1}{slip2}</div><div id="s1-title">{sc.words_html("खेती का हिसाब इतना मुश्किल क्यों?")}</div><div id="s1-cream"></div>')
    # camera: paper coordinates -> frame
    sc.js.append("""
    const cam = '#s1-cam';
    tl.fromTo(cam, {x:-250, y:140, scale:1.22}, {x:-290, y:120, scale:1.26, duration:2.0, ease:'none'}, 0);
    tl.fromTo('#s1-circ path', {strokeDasharray:900, strokeDashoffset:900}, {strokeDashoffset:0, duration:0.7, ease:'power2.inOut'}, 0.9);
    tl.fromTo(cam, {x:-290, y:120, scale:1.26}, {x:-292, y:63, scale:1.1, duration:0.7, ease:'power2.inOut', immediateRender:false}, 2.0);
    tl.fromTo('#s1-slip1', {x:700, rotation:4}, {x:0, rotation:-6, duration:0.6, ease:'expo.out'}, 2.15);
    tl.fromTo('#s1-q', {opacity:0, scale:1.3}, {opacity:1, scale:1, duration:0.25, ease:'expo.out'}, 3.9);
    tl.fromTo(cam, {x:-292, y:63, scale:1.1}, {x:-220, y:-180, scale:1.0, duration:0.7, ease:'power2.inOut', immediateRender:false}, 5.45);
    tl.fromTo('#s1-slip2', {x:800, rotation:-3}, {x:0, rotation:5, duration:0.6, ease:'expo.out'}, 5.7);
    tl.fromTo(cam, {x:-220, y:-180, scale:1.0}, {x:600, y:345, scale:0.5, duration:0.9, ease:'power2.inOut', immediateRender:false}, 8.5);
    tl.set('#s1-title', {opacity:1}, 9.0);
    tl.fromTo('#s1-title .w', {opacity:0, filter:'blur(6px)'}, {opacity:1, filter:'blur(0px)', duration:0.13, stagger:0.067, ease:'power2.out'}, 9.0);
    tl.fromTo('#s1-title', {opacity:1, filter:'blur(0px)'}, {opacity:0, filter:'blur(8px)', duration:0.18, ease:'power2.in', immediateRender:false}, 11.62);
    tl.fromTo(cam, {x:600, y:345, scale:0.5, filter:'blur(0px)'}, {x:-1500, y:345, scale:0.5, filter:'blur(18px)', duration:0.4, ease:'power3.in', immediateRender:false}, 11.85);
    tl.fromTo('#s1-cream', {opacity:0}, {opacity:1, duration:0.3, ease:'power2.inOut'}, 11.95);
    """)
    sc.write(stage, ground=C["desk"])


# =====================================================================================
# S2 — the reveal
# =====================================================================================
def build_s2():
    sc = Scene("s2")
    sc.screen("home", 12.3, 22.6)
    sc.cam_set({**CENTER, "y": 760})
    sc.cam_to(12.3, CENTER, dur=0.6, ease="power3.out", blur=True)
    sc.cam_to(14.55, BASE, dur=0.6)
    sc.cam_to(16.95, cam(54, 400, 1101, 620), dur=0.6)
    sc.ol(17.4, (54, 400, 1101, 470))
    sc.ol(19.3)
    sc.cam_to(19.35, cam(54, 1065, 1101, 750), dur=0.6)
    sc.tap(21.45, 405, 1215, 150, 270)
    st = cam(405, 1215, 150, 270)
    z = st["scale"]
    sc.cam_to(21.75, {"x": st["x"] - 4.0 * z * (OX + S * 480), "y": st["y"] - 4.0 * z * (OY + S * 1350), "scale": z * 5}, dur=0.45, ease="power3.in")
    sc.flood(C["clay"], 22.05, 0.3, 0, 1)
    sc.html.append('<img id="s2-icon" class="icon" src="assets/brand/app-icon.png" alt="" style="left:120px;top:250px" />')
    sc.js.append(f"tl.fromTo('#s2-icon', {{opacity:0, scale:0.6}}, {{opacity:1, scale:1, duration:0.45, ease:'expo.out'}}, {sc.t(14.85)});"
                 f"tl.fromTo('#s2-icon', {{opacity:1}}, {{opacity:0, duration:0.18, immediateRender:false}}, {sc.t(21.5)});")
    sc.title("s2-name", "खेती हिसाब", 15.25, 21.7, y=440, size=120, color=C["green"])
    sc.title("s2-latin", "Kheti Hisab", 15.6, 21.7, y=600, size=60, font="display", style="line")
    sc.title("s2-tag", "हर किसान का अपना हिसाब", 19.5, 21.7, y=700, size=56, weight=700, style="grey", color=C["ink"])
    sc.write(phone_stage(sc))


# =====================================================================================
# S3 — expense
# =====================================================================================
def build_s3():
    sc = Scene("s3")
    sc.screen("cat", 22.6, 25.62)
    sc.screen("expfilled", 25.4, 31.75, enter="fade")
    sc.screen("vendor", 31.55, 33.35, enter="fade")
    sc.open_on((45, 810, 1110, 1425))
    sc.flood(C["clay"], 22.6, 0.35, 1, 0)
    sc.ol(22.8, (435, 825, 270, 435))
    sc.ol(23.75, (435, 1305, 270, 435))
    sc.ol(24.08, (810, 1305, 345, 435))
    sc.ol(24.62, (435, 1800, 270, 435))
    sc.ol(25.1, (435, 1305, 270, 435))
    sc.tap(25.2, 435, 1305, 270, 435)
    sc.ol(25.4)
    sc.cam_to(25.5, cam(45, 560, 1110, 760), dur=0.6)
    sc.ol(27.6, (60, 1110, 1080, 201))
    sc.cam_to(29.3, cam(45, 360, 1110, 420), dur=0.6)
    sc.ol(29.7, (45, 375, 1110, 150))
    sc.ol(30.6)
    sc.cam_to(30.6, BASE, dur=0.6)
    sc.tap(31.3, 45, 2175, 1110, 141)
    sc.cam_to(31.7, cam(45, 2100, 1125, 390), dur=0.6)
    sc.ol(32.3, (45, 2110, 1125, 370))
    sc.items("s3-l", [("खर्चा लिखो", 27.55), ("फसल से जोड़ो", 29.45), ("हिसाब साफ रखो", 31.45)], 33.0,
             y=330, size=78, font="main", style="blur")
    sc.css.append("#s3-l { font-weight:800; }")
    sc.ol(32.95)
    sc.whip_out()
    sc.write(phone_stage(sc))


# =====================================================================================
# S4 — income and dues
# =====================================================================================
def build_s4():
    sc = Scene("s4")
    sc.screen("incfilled", 33.35, 35.3)
    sc.screen("incpending", 35.08, 37.25, enter="fade")
    sc.screen("owed", 37.0, 44.65, enter="push")
    sc.open_on((54, 330, 1100, 960))
    sc.whip_in()
    sc.ol(33.9, (54, 1170, 1101, 100))
    sc.ol(35.1)
    sc.cam_to(35.1, cam(45, 855, 1080, 390), dur=0.55)
    sc.ol(35.8, (45, 1140, 1065, 90))
    sc.ol(36.9)
    sc.cam_to(36.95, BASE, dur=0.6)
    sc.cam_to(38.55, cam(48, 420, 1107, 210), dur=0.6)
    sc.ol(39.1, (90, 450, 495, 165))
    sc.ol(41.1, (615, 450, 510, 165))
    sc.ol(42.55)
    sc.cam_to(42.55, cam(48, 1240, 1110, 950), dur=0.6)
    sc.cam_to(44.0, BASE, dur=0.6)
    sc.amount("s4-a1", "लेना", "₹1,19,250", C["green"], 39.35, 42.6, y=250)
    sc.amount("s4-a2", "देना", "₹16,416", C["clay"], 41.35, 42.6, y=520)
    sc.write(phone_stage(sc))


# =====================================================================================
# S5 — labour
# =====================================================================================
def build_s5():
    sc = Scene("s5")
    sc.screen("owed", 44.65, 45.1, name="s5-prev")
    sc.screen("register", 44.68, 46.95, enter="push")
    sc.screen("markday", 46.85, 50.35, enter="fade")
    sc.screen("calendar", 50.1, 57.15, enter="push")
    sc.cam_set(BASE)
    sc.cam_to(45.2, cam(45, 765, 1110, 700), dur=0.6)
    sc.tap(46.65, 90, 1149, 1026, 105)
    sc.cam_to(46.9, cam(54, 360, 1101, 600), dur=0.55)
    sc.ol(47.15, (66, 804, 354, 111))
    sc.ol(49.1, (450, 804, 330, 111))
    sc.ol(50.05)
    sc.cam_to(50.15, cam(48, 465, 1107, 210), dur=0.6)
    sc.ol(50.75, (48, 465, 1107, 210))
    sc.ol(51.7)
    sc.amount("s5-a1", "बकाया", "₹2,400", C["due"], 50.65, 51.75, y=330)
    sc.cam_to(51.75, cam(48, 760, 1107, 1260), dur=0.65)
    sc.items("s5-l", [("Attendance", 52.2), ("मजदूरी", 53.35), ("बाकी भुगतान", 51.13 + 3.4)], 57.0,
             y=300, size=78, font="display", style="grey")
    sc.css.append("#s5-l .li:nth-child(n+2) { font-family:var(--font-main); font-weight:800; }")
    sc.cam_to(56.15, BASE, dur=0.55)
    sc.tap(56.7, 495, 2310, 240, 135)
    sc.write(phone_stage(sc))


# =====================================================================================
# S6 — farm work
# =====================================================================================
def build_s6():
    sc = Scene("s6")
    sc.screen("acttype", 56.8, 61.2)
    sc.screen("acts", 61.0, 62.75, enter="push")
    sc.screen("actdetail", 62.55, 68.6, enter="push")
    sc.open_on((45, 435, 1125, 1365), hold=0.45)
    sc.css.append(f"#s6-ir {{ position:absolute; inset:0; background:{C['ground']}; }}")
    sc.js.append("tl.fromTo('#s6-ir', {clipPath:'circle(0px at 1244px 837px)'}, {clipPath:'circle(2300px at 1244px 837px)', duration:0.4, ease:'power2.in'}, 0);")
    sc.ol(57.4, (54, 450, 342, 420))
    sc.ol(58.45, (816, 450, 345, 420))
    sc.ol(59.55, (435, 450, 345, 420))
    sc.ol(60.9)
    sc.cam_to(61.0, cam(45, 460, 1110, 820), dur=0.6)
    sc.cam_to(62.6, cam(48, 740, 1107, 360), dur=0.6)
    sc.ol(63.3, (48, 765, 1107, 315))
    sc.ol(64.45)
    sc.cam_to(64.5, BASE, dur=0.6)
    sc.items("s6-l", [("Spraying", 57.42), ("Irrigation", 58.47), ("Fertiliser", 59.6), ("Farm Work", 60.75)], 64.4,
             y=250, size=72, font="display", style="blur")
    sc.html.append('<div id="s6-pro" class="pro" style="left:120px;top:430px"><span class="pro-tag">PRO</span>'
                   '<span class="pro-t">नया काम और रिमाइंडर</span></div>')
    t = sc.t(65.0)
    sc.js.append(f"tl.fromTo('#s6-pro', {{opacity:0, filter:'blur(8px)'}}, {{opacity:1, filter:'blur(0px)', duration:0.2}}, {t});")
    sc.title("s6-t", "खेत का काम भी याद रखो", 64.6, 68.3, y=250, size=84)
    sc.whip_out()
    stage = phone_stage(sc)
    body = "\n".join(sc.html)
    sc.html = [f'<div id="s6-ir">{stage}{body}</div>']
    sc.write("", ground="transparent")


# =====================================================================================
# S7 — contract farming
# =====================================================================================
def build_s7():
    sc = Scene("s7")
    sc.screen("contract", 68.6, 72.0)
    sc.screen("payments", 71.75, 74.75, enter="fade")
    sc.screen("contract", 74.5, 78.05, enter="fade", name="s7-scr-back")
    sc.open_on((60, 1155, 1095, 850))
    sc.whip_in()
    sc.ol(70.6, (60, 1560, 1095, 90))
    sc.ol(71.7)
    sc.cam_to(71.75, cam(48, 600, 1116, 720), dur=0.55)
    sc.ol(72.05, (48, 900, 1116, 195))
    sc.ol(72.7, (435, 615, 345, 180))
    sc.ol(74.4)
    sc.cam_to(74.5, BASE, dur=0.6)
    sc.items("s7-l", [("Contract", 68.86), ("Advance", 70.57), ("Instalments", 71.76), ("Balance", 72.7)], 77.7,
             y=250, size=78, font="display", style="grey")
    sc.html.append('<div id="s7-dip" class="flood" style="background:#000"></div>')
    sc.js.append(f"tl.fromTo('#s7-dip', {{opacity:0}}, {{opacity:0.4, duration:0.1}}, {r(sc.dur-0.1)});")
    sc.write(phone_stage(sc))


# =====================================================================================
# S8 — offline
# =====================================================================================
def build_s8():
    sc = Scene("s8")
    sc.screen("exppending", 78.05, 81.25)
    sc.screen("offline", 81.0, 88.15, enter="push")
    sc.open_on((45, 330, 1110, 980))
    sc.ol(79.5, (96, 1140, 1008, 90))
    sc.ol(80.6)
    sc.cam_to(80.5, BASE, dur=0.45)
    sc.tap(80.95, 45, 2175, 1110, 141)
    sc.cam_to(81.3, cam(93, 420, 1032, 255), dur=0.6)
    sc.ol(82.6, (93, 420, 1032, 255))
    sc.ol(87.4)
    bars = "".join(f'<div class="bar" id="s8-b{i}" style="left:{i*46}px;height:{40+i*34}px"></div>' for i in range(4))
    sc.html.append(f'<div id="s8-sig" class="sig" style="left:130px;top:160px">{bars}<div id="s8-x" class="sig-x">×</div></div>')
    for i in range(4):
        sc.js.append(f"tl.fromTo('#s8-b{3-i}', {{opacity:1}}, {{opacity:0.15, duration:0.12}}, {sc.t(78.5 + i*0.35)});")
    sc.js.append(f"tl.fromTo('#s8-x', {{opacity:0, scale:1.6}}, {{opacity:1, scale:1, duration:0.25, ease:'expo.out'}}, {sc.t(80.0)});"
                 f"tl.set('#s8-sig', {{opacity:1}}, 0);"
                 f"tl.fromTo('#s8-sig', {{opacity:1}}, {{opacity:0, duration:0.18, immediateRender:false}}, {sc.t(81.8)});")
    sc.title("s8-t", "Works Offline", 82.0, None, y=300, size=110, font="display", color=C["green"], style="line")
    sc.title("s8-t2", "आपका हिसाब आपके फोन में रहता है", 85.2, None, y=470, size=60, weight=700, style="grey")
    sc.js.append(f"tl.fromTo('#s8-t, #s8-t2', {{opacity:1, filter:'blur(0px)'}}, {{opacity:0, filter:'blur(8px)', duration:0.18, immediateRender:false}}, {r(sc.dur-0.3)});")
    sc.cam_to(87.75, {"x": -460, "y": 0, "scale": 1.0}, dur=0.4, ease="power3.in")
    sc.write(phone_stage(sc))


# =====================================================================================
# S9 — cloud sync / new phone
# =====================================================================================
def build_s9():
    sc = Scene("s9")
    sc.screen("synced", 88.15, 95.0)
    st0 = cam(93, 435, 1032, 180)
    sc.open_on((93, 435, 1032, 180), hold=0.15, frm={"x": -460, "y": 0, "scale": 1.0})
    sc.ol(88.9, (93, 435, 1032, 180))
    sc.ol(93.9)
    sc.cam_to(93.95, BASE, dur=0.5)
    sc.js.append(f"tl.fromTo('#s9-cam', {{x:0}}, {{x:-1500, duration:0.45, ease:'power3.in', immediateRender:false}}, {sc.t(94.45)});")
    sc.title("s9-t", "Cloud Sync", 88.7, 94.6, y=300, size=110, font="display", color=C["green"], style="line")
    sc.html.append('<div id="s9-pro" class="pro" style="left:120px;top:460px"><span class="pro-tag">PRO</span>'
                   '<span class="pro-t">के साथ</span></div>')
    sc.js.append(f"tl.fromTo('#s9-pro', {{opacity:0, filter:'blur(8px)'}}, {{opacity:1, filter:'blur(0px)', duration:0.2}}, {sc.t(89.0)});"
                 f"tl.fromTo('#s9-pro', {{opacity:1}}, {{opacity:0, duration:0.18, immediateRender:false}}, {sc.t(94.4)});")
    # phone B
    b_screens = [{"name": "s9-b0", "key": "start", "tin": sc.t(94.4), "tout": sc.t(97.65)},
                 {"name": "s9-b1", "key": "home", "tin": sc.t(97.4), "tout": sc.dur}]
    olb = '<div id="s9-olb" class="ol"></div>'
    tapb = '<div id="s9-tapb" class="tap"></div>'
    phone_b = sc.phone_html(pid="s9-phoneB", screens=b_screens, extra=olb + tapb)
    sc.js.append(f"tl.fromTo('#s9-b1 img', {{opacity:0}}, {{opacity:1, duration:0.3}}, {sc.t(97.4)});")
    stb = cam(54, 666, 1101, 258)
    sc.js.append(f"tl.fromTo('#s9-camB', {{x:0, y:900, scale:1, opacity:0, filter:'blur(14px)'}}, {{x:0, y:0, scale:1, opacity:1, filter:'blur(0px)', duration:0.55, ease:'power3.out'}}, {sc.t(94.5)});"
                 f"tl.fromTo('#s9-camB', {{x:0, y:0, scale:1}}, {{...{json.dumps(stb)}, duration:0.6, ease:'power2.inOut', immediateRender:false}}, {sc.t(95.2)});"
                 f"tl.set('#s9-olb', {{left:{r(54*S-3)}, top:{r(666*S-3)}, width:{r(1101*S+6)}, height:{r(258*S+6)}}}, 0);"
                 f"tl.fromTo('#s9-olb', {{opacity:0, scale:1.08}}, {{opacity:1, scale:1, duration:0.3, ease:'expo.out'}}, {sc.t(95.65)});"
                 f"tl.fromTo('#s9-olb', {{opacity:1}}, {{opacity:0, duration:0.15, immediateRender:false}}, {sc.t(97.3)});"
                 f"tl.fromTo('#s9-camB', {json.dumps(stb)}, {{x:0, y:0, scale:1, duration:0.55, ease:'power2.inOut', immediateRender:false}}, {sc.t(97.4)});")
    home_tiles = cam(54, 1065, 1101, 750)
    sc.js.append(f"tl.fromTo('#s9-camB', {{x:0, y:0, scale:1}}, {{...{json.dumps(home_tiles)}, duration:0.55, ease:'power2.inOut', immediateRender:false}}, {sc.t(98.05)});"
                 f"tl.set('#s9-tapb', {{left:{r(915*S)}, top:{r(1215*S)}, width:{r(165*S)}, height:{r(270*S)}}}, 0);"
                 f"tl.fromTo('#s9-tapb', {{opacity:0}}, {{opacity:1, duration:0.06}}, {sc.t(98.65)});")
    zh = home_tiles["scale"]
    zt = {"x": home_tiles["x"] - 4.0 * zh * (OX + S * 997), "y": home_tiles["y"] - 4.0 * zh * (OY + S * 1350), "scale": zh * 5}
    sc.js.append(f"tl.fromTo('#s9-camB', {json.dumps(home_tiles)}, {{...{json.dumps(zt)}, duration:0.45, ease:'power3.in', immediateRender:false}}, {sc.t(98.8)});")
    sc.flood(C["ground"], 99.0, 0.25, 0, 1)
    sc.title("s9-t2", "नया फोन • वही हिसाब", 94.7, 98.0, y=330, size=70)
    stage = phone_stage(sc) + f'<div id="s9-camB" class="cam" data-layout-allow-overflow>{phone_b}</div>'
    sc.write(stage)


# =====================================================================================
# S10 — season report (payoff)
# =====================================================================================
def build_s10():
    sc = Scene("s10")
    sc.screen("reports", 99.25, 101.35)
    sc.screen("pl", 100.9, 109.4, enter="push")
    sc.open_on((48, 330, 1122, 1260))
    sc.flood(C["ground"], 99.25, 0.3, 1, 0)
    sc.ol(100.2, (48, 495, 1122, 189))
    sc.tap(100.6, 48, 495, 1122, 189)
    sc.ol(100.85)
    sc.cam_to(100.95, cam(54, 405, 1101, 540), dur=0.6)
    sc.ol(103.65, (225, 786, 255, 114))
    sc.ol(105.3, (735, 786, 255, 114))
    sc.ol(107.2)
    sc.amount("s10-a1", "Income", "₹2,92,250", C["green"], 103.7, 107.4, y=170, size=96)
    sc.amount("s10-a2", "Expense", "₹1,09,682", C["clay"], 105.35, 107.4, y=420, size=96)
    sc.cam_to(107.3, cam(330, 500, 540, 160, zmax=3.0), dur=0.55)
    sc.amount("s10-a3", "Profit", "₹1,82,568", C["green"], 107.7, 109.25, y=300, size=150)
    sc.html.append('<div id="s10-ul" class="ul" style="left:124px;top:560px"></div>')
    sc.js.append(f"tl.fromTo('#s10-ul', {{scaleX:0}}, {{scaleX:1, duration:0.45, ease:'expo.out'}}, {sc.t(107.95)});"
                 f"tl.fromTo('#s10-ul', {{opacity:1}}, {{opacity:0, duration:0.15, immediateRender:false}}, {sc.t(109.1)});")
    sc.flood(C["green"], 109.0, 0.4, 0, 1)
    sc.css.append("#s10-a1 .amt-l, #s10-a2 .amt-l, #s10-a3 .amt-l { font-family:var(--font-display); }")
    sc.write(phone_stage(sc))


# =====================================================================================
# S11 — end card
# =====================================================================================
def build_s11():
    sc = Scene("s11")
    sc.screen("home", 109.4, 121.5)
    sc.cam_set(BASE)
    sc.css.append(f"""
    #s11-g {{ position:absolute; inset:0; background: radial-gradient(ellipse 1400px 1000px at 40% 45%, {C['green']} 0%, {C['green2']} 100%); }}
    #s11-root-txt {{ position:absolute; inset:0; }}
    .s11-line {{ position:absolute; left:120px; width:820px; font-family:var(--font-main); font-weight:800; color:#F6EFE7; }}
    #s11-mark {{ position:absolute; left:470px; top:300px; width:250px; height:250px; border-radius:56px; box-shadow:0 30px 60px rgba(0,0,0,0.25); opacity:0; }}
    #s11-word {{ position:absolute; left:760px; top:300px; font-family:var(--font-main); font-weight:800; font-size:150px; color:#F6EFE7; line-height:1.15; opacity:0; white-space:nowrap; }}
    #s11-latin {{ position:absolute; left:770px; top:490px; font-family:var(--font-display); font-weight:800; font-size:64px; color:{C['marigold']}; opacity:0; }}
    #s11-tag {{ position:absolute; left:0; width:1920px; top:640px; text-align:center; font-family:var(--font-main); font-weight:800; font-size:78px; color:#F6EFE7; opacity:0; }}
    #s11-sub {{ position:absolute; left:0; width:1920px; top:760px; text-align:center; font-family:var(--font-main); font-weight:700; font-size:44px; color:rgba(246,239,231,0.82); opacity:0; }}
    #s11-badges {{ position:absolute; left:0; width:1920px; top:850px; display:flex; justify-content:center; gap:36px; opacity:0; }}
    #s11-badges img {{ height:84px; }}
    """)
    sc.js.append(f"tl.fromTo('#s11-cam', {{x:0, y:0, scale:1}}, {{x:0, y:0, scale:1, duration:0.01}}, 0);")
    sc.title("s11-l1", "खेती आपकी है…", 109.5, 112.85, y=330, size=96, color="#F6EFE7")
    sc.title("s11-l2", "तो हिसाब भी आपका होना चाहिए", 110.9, 112.85, y=470, size=72, color="#F6EFE7", weight=700)
    # phone shrinks into the app icon
    sc.js.append(f"tl.fromTo('#s11-cam', {{x:0, y:0, scale:1, opacity:1}}, {{x:{r(595 - 0.28*(PL+PW/2))}, y:{r(425 - 0.28*(PT+PH/2))}, scale:0.28, duration:0.6, ease:'power3.inOut', immediateRender:false}}, {sc.t(113.0)});"
                 f"tl.fromTo('#s11-cam', {{opacity:1}}, {{opacity:0, duration:0.2, immediateRender:false}}, {sc.t(113.45)});"
                 f"tl.fromTo('#s11-mark', {{opacity:0, scale:0.92}}, {{opacity:1, scale:1, duration:0.4, ease:'expo.out'}}, {sc.t(113.45)});"
                 f"tl.fromTo('#s11-word', {{opacity:1, clipPath:'inset(-40% 100% -40% 0)'}}, {{opacity:1, clipPath:'inset(-40% 0% -40% 0)', duration:0.5, ease:'power3.out'}}, {sc.t(113.9)});"
                 f"tl.fromTo('#s11-latin', {{opacity:0, filter:'blur(8px)'}}, {{opacity:1, filter:'blur(0px)', duration:0.2}}, {sc.t(114.3)});"
                 f"tl.set('#s11-tag', {{opacity:1}}, {sc.t(116.1)});"
                 f"tl.fromTo('#s11-tag .w', {{color:'rgba(246,239,231,0.22)'}}, {{color:'#F6EFE7', duration:0.12, stagger:0.45, ease:'none'}}, {sc.t(116.1)});"
                 f"tl.fromTo('#s11-sub', {{opacity:0, filter:'blur(8px)'}}, {{opacity:1, filter:'blur(0px)', duration:0.2}}, {sc.t(117.3)});"
                 f"tl.fromTo('#s11-badges', {{opacity:0, y:40}}, {{opacity:1, y:0, duration:0.45, ease:'expo.out'}}, {sc.t(117.7)});")
    stage = ('<div id="s11-g"></div>' + phone_stage(sc, patch=False)
             + '<img id="s11-mark" src="assets/brand/app-icon.png" alt="" />'
             + '<div id="s11-word">खेती हिसाब</div><div id="s11-latin">Kheti Hisab</div>'
             + f'<div id="s11-tag">{sc.words_html("हर किसान का अपना हिसाब")}</div>'
             + '<div id="s11-sub">अपनी खेती • अपना रिकॉर्ड • अपना हिसाब</div>'
             + '<div id="s11-badges"><img src="assets/brand/app-store.svg" alt="Download on the App Store" />'
             + '<img src="assets/brand/google-play.png" alt="Get it on Google Play" /></div>')
    sc.write(stage, ground=C["green"])


# =====================================================================================
# captions
# =====================================================================================
CAPS = [
    (0.15, 1.95, "बीज का खर्चा कहाँ लिखा था…?"), (2.0, 3.84, "खाद वाले के पैसे दिए"), (3.87, 5.4, "या अभी बाकी हैं?"),
    (5.45, 6.65, "और मंडी वाले से"), (6.68, 8.3, "कितने पैसे लेने हैं?"), (8.57, 9.84, "खेती संभालूँ…"),
    (9.87, 11.75, "या हिसाब ढूँढता रहूँ?"),
    (12.6, 14.75, "अब खेती का हिसाब होगा आसान।"), (14.8, 17.05, "ये है Kheti Hisab —"),
    (17.1, 19.45, "किसान की अपनी डिजिटल हिसाब किताब।"),
    (22.8, 23.7, "बीज खरीदा?"), (23.75, 25.08, "खाद, दवाई, डीज़ल"), (25.11, 27.3, "या कोई और खर्चा हुआ?"),
    (27.54, 29.35, "बस उसी समय entry करो।"), (29.4, 30.72, "और खर्चा सही फसल के"), (30.76, 32.8, "हिसाब में जुड़ जाएगा।"),
    (33.64, 35.0, "फसल बेच दी…"), (35.05, 37.05, "लेकिन पूरे पैसे अभी नहीं मिले?"), (37.11, 39.02, "Kheti Hisab बताता है —"),
    (39.07, 41.02, "किससे कितना लेना है,"), (41.06, 42.55, "किसको कितना देना है,"), (42.59, 44.2, "और कितना बाकी है।"),
    (44.86, 47.1, "आज खेत पर कौन-कौन काम करने आया?"), (47.14, 49.05, "किसकी पूरी मजदूरी,"), (49.09, 50.15, "किसकी आधी…"),
    (50.19, 51.72, "और किसका भुगतान बाकी है?"), (51.77, 54.22, "मजदूर की अटेंडेंस और मजदूरी"),
    (54.26, 56.4, "का हिसाब भी आसानी से संभालो।"),
    (57.37, 58.4, "कब spray किया?"), (58.44, 59.48, "कब सिंचाई हुई?"), (59.52, 62.3, "कौन-सी दवाई या खाद इस्तेमाल की?"),
    (62.53, 64.48, "और अगला काम कब करना है?"), (64.53, 66.3, "Kheti Hisab में,"), (66.35, 68.1, "खेत का काम भी याद रखो।"),
    (68.84, 70.5, "Contract farming करते हैं?"), (70.55, 71.7, "Advance मिला,"), (71.74, 72.32, "किस्त आई"),
    (72.36, 74.45, "या कितना पैसा अभी बाकी है…"), (74.49, 76.9, "उसका भी पूरा हिसाब एक जगह।"),
    (78.3, 80.66, "लेकिन खेत में network नहीं हो तो?"), (80.7, 81.96, "कोई दिक्कत नहीं।"),
    (82.0, 84.9, "Kheti Hisab offline भी काम करता है।"),
    (88.4, 90.36, "और Pro में Cloud Sync के साथ,"), (90.4, 92.28, "अपनी sync की गई book को"),
    (92.3, 94.25, "cloud में सुरक्षित रख सकते हैं।"), (94.3, 95.55, "नया फोन लिया?"),
    (95.6, 97.36, "अपनी sync की गई book"), (97.4, 98.7, "फिर से खोल सकते हैं।"),
    (99.45, 102.4, "सीजन खत्म होने पर सिर्फ अंदाज़ा क्यों?"), (102.83, 103.58, "देखिए —"),
    (103.62, 105.24, "कितनी आमदनी हुई,"), (105.28, 106.6, "कितना खर्चा हुआ"), (106.64, 108.5, "और आखिर में क्या बचा।"),
    (109.3, 110.86, "खेती आपकी है…"), (110.9, 112.96, "तो हिसाब भी आपका होना चाहिए।"), (113.0, 115.2, "आज ही डाउनलोड करें —"),
]



SFX = [  # id, file, abs time, volume
    ("sfx-w1", "whoosh-short.mp3", 11.85, 0.35), ("sfx-w2", "whoosh.mp3", 21.75, 0.3),
    ("sfx-w3", "whoosh-short.mp3", 33.0, 0.3), ("sfx-w4", "whoosh-short.mp3", 68.25, 0.3),
    ("sfx-w5", "whoosh.mp3", 98.8, 0.3), ("sfx-p1", "pop.mp3", 39.45, 0.3), ("sfx-p2", "pop.mp3", 41.45, 0.25),
    ("sfx-p3", "pop.mp3", 107.8, 0.35), ("sfx-c1", "click-soft.mp3", 21.45, 0.35), ("sfx-c2", "click-soft.mp3", 31.3, 0.35),
    ("sfx-c3", "click-soft.mp3", 80.95, 0.35), ("sfx-c4", "click-soft.mp3", 100.6, 0.35),
]



if __name__ == "__main__":
    for f in (build_s1, build_s2, build_s3, build_s4, build_s5, build_s6, build_s7, build_s8, build_s9, build_s10, build_s11):
        f()
    K.build_captions(CAPS)
    K.build_index(sfx=SFX)
    print("built", len(SCENES), "scenes + captions + index")
