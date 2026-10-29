"""phone_kit — generate HyperFrames scenes that show real app screenshots in a phone,
with a camera that punches into the part of the screen the voiceover is talking about.

Usage (from a project's tools/build.py):

    import phone_kit as K
    K.setup(root=ROOT, total=121.5, scenes=SCENES, shots=SHOTS, colors=COLORS, fonts=FONTS)
    from phone_kit import *          # Scene, cam, phone_stage, BASE, CENTER, S, OX, OY, ...

    sc = Scene("s2")
    sc.screen("home", 12.3, 22.6)                     # screenshot key, absolute in/out
    sc.cam_set(CENTER)
    sc.cam_to(17.0, cam(54, 400, 1101, 620))          # frame a region given in screenshot pixels
    sc.ol(17.4, (54, 400, 1101, 470))                 # focus outline on a region
    sc.tap(21.45, 405, 1215, 150, 270)                # iOS press highlight
    sc.title("s2-name", "Kheti Hisab", 15.2, 21.7, size=120)
    sc.write(phone_stage(sc))

    K.build_captions(CAPTIONS)
    K.build_index(sfx=SFX)

All times you pass are ABSOLUTE seconds on the film's clock (the voiceover). Regions are in
the screenshot's own pixels (e.g. 1206 x 2622 for an iPhone 6.3" capture).

The generator rewrites index.html and compositions/*.html. Once someone edits those files in
HyperFrames Studio, stop regenerating (or move their edits into the build script first).
"""
import json
from pathlib import Path

# ---- defaults, replaced by setup() -------------------------------------------------
ROOT = Path(".")
W, H = 1920, 1080
TOTAL = 30.0
LANG = "en"
SCENES = []          # [(id, start, end)] absolute seconds; overlap two hosts for an iris/overlap transition
SHOT = {}            # key -> file name in assets/screens/
FONTS = []           # [(family, file in assets/fonts/, weight)]
C = {}               # palette, see REQUIRED_COLORS
FONT_MAIN = "sans-serif"
FONT_DISPLAY = "sans-serif"

REQUIRED_COLORS = ("ground", "patch", "ink", "ink2", "accent", "alert", "brand")

S = 0.33
SW = SH = BEZ = PW = PH = PL = PT = OX = OY = 0.0
SCREEN_RADIUS = 58
TITLE_ZONE_RIGHT = 905
# where cam() puts a framed region and where lift() may place a card (landscape defaults; see setup())
FRAME = {"cx_min": 1330, "cy": 470, "max_w": 940, "max_h": 780, "right_max": 1850}
LIFT_BOX = (925, 70, 1870, 900)
LIFT_DY = 0
BASE = {"x": 0.0, "y": 0.0, "scale": 1.0}
CENTER = {"x": 0.0, "y": 0.0, "scale": 1.0}


def setup(root, total, scenes, shots, colors, fonts, font_main, font_display, lang="en",
          screen_px=(1206, 2622), scale=0.33, bezel=13, phone_center_x=1240, phone_top=40,
          screen_radius=58, title_zone_right=905, width=1920, height=1080, frame=None, lift_box=None, lift_dy=0):
    """Landscape defaults put titles left and the phone right. For portrait (1080 x 1920) pass e.g.
    phone_center_x=540, phone_top=560, scale=0.5, title_zone_right=0,
    frame={"cx_min": 540, "cy": 1180, "max_w": 1000, "max_h": 1100, "right_max": 1040},
    lift_box=(40, 600, 1040, 1500), lift_dy=-80."""
    """Configure the kit for one film. Call before `from phone_kit import *`."""
    g = globals()
    missing = [k for k in REQUIRED_COLORS if k not in colors]
    if missing:
        raise ValueError(f"colors is missing {missing}")
    sw, sh = screen_px[0] * scale, screen_px[1] * scale
    pw, ph = sw + 2 * bezel, sh + 2 * bezel
    pl = phone_center_x - pw / 2
    g.update(ROOT=Path(root), TOTAL=total, SCENES=list(scenes), SHOT=dict(shots), C=dict(colors),
             FONTS=list(fonts), FONT_MAIN=font_main, FONT_DISPLAY=font_display, LANG=lang,
             W=width, H=height, S=scale, SW=sw, SH=sh, BEZ=bezel, PW=pw, PH=ph, PL=pl, PT=phone_top,
             OX=pl + bezel, OY=phone_top + bezel, SCREEN_RADIUS=screen_radius,
             TITLE_ZONE_RIGHT=title_zone_right,
             FRAME=frame or {"cx_min": 1330, "cy": 470, "max_w": 940, "max_h": 780, "right_max": width - 70},
             LIFT_BOX=lift_box or (title_zone_right + 20, 70, width - 50, 900), LIFT_DY=lift_dy,
             CENTER={"x": width / 2 - phone_center_x, "y": 0.0, "scale": 1.0})
    (Path(root) / "compositions").mkdir(exist_ok=True)


def r(v):
    return round(v, 3)


def cam(rx, ry, rw, rh, zmax=2.9):
    """Camera state that frames a screenshot region (source px) to the right of the title zone.

    The zoom is the largest that keeps the region within ~940 x 780 px, capped at zmax (at
    scale 0.33, zmax 2.9 is ~0.96 source px per screen px, so the capture stays sharp). The
    phone's left edge is kept right of TITLE_ZONE_RIGHT so left-side titles never collide.
    """
    cx, cy = rx + rw / 2, ry + rh / 2
    z = min(zmax, FRAME["max_w"] / (rw * S), FRAME["max_h"] / (rh * S))
    z = max(z, 1.0)
    while True:
        px = max(FRAME["cx_min"], TITLE_ZONE_RIGHT + z * S * cx)
        if px + z * S * rw / 2 <= FRAME["right_max"] or z <= 1.0:
            break
        z -= 0.05
    py = FRAME["cy"]
    return {"x": round(px - z * (OX + S * cx), 2), "y": round(py - z * (OY + S * cy), 2),
            "scale": round(z, 3)}


def zoom_through(state, cx, cy, factor=5.0):
    """A camera state `factor` times closer than `state`, keeping screenshot point (cx, cy) fixed."""
    z = state["scale"]
    k = factor - 1.0
    return {"x": state["x"] - k * z * (OX + S * cx), "y": state["y"] - k * z * (OY + S * cy), "scale": z * factor}


def font_family(font):
    return "var(--font-main)" if font == "main" else "var(--font-display)"


class Scene:
    def __init__(self, sid):
        self.id = sid
        self.start, self.end = next((a, b) for i, a, b in SCENES if i == sid)
        self.dur = r(self.end - self.start)
        self.html, self.js, self.css = [], [], []
        self.cam_state = dict(BASE)
        self.screens = []
        self.ol_state = None
        self.ol_html = []
        self.n_ol = 0
        self.n_lift = 0
        self.lift_html = []

    def t(self, abs_t):
        return r(abs_t - self.start)

    # ---- camera -------------------------------------------------------------
    def cam_set(self, state):
        self.cam_state = dict(state)
        self.js.append(f"tl.set('#{self.id}-cam', {json.dumps(state)}, 0);")

    def cam_to(self, abs_t, state, dur=0.6, ease="power2.inOut", blur=False):
        a = dict(self.cam_state)
        b = dict(state)
        if blur:
            self.js.append(
                f"tl.fromTo('#{self.id}-cam', {{filter:'blur(0px)'}}, {{filter:'blur(6px)', duration:{r(dur/2)}, ease:'power2.in', immediateRender:false}}, {self.t(abs_t)});"
                f"tl.fromTo('#{self.id}-cam', {{filter:'blur(6px)'}}, {{filter:'blur(0px)', duration:{r(dur/2)}, ease:'power2.out', immediateRender:false}}, {r(self.t(abs_t)+dur/2)});")
        self.js.append(
            f"tl.fromTo('#{self.id}-cam', {json.dumps(a)}, {{...{json.dumps(b)}, duration:{dur}, ease:'{ease}', immediateRender:false}}, {self.t(abs_t)});")
        self.cam_state = b

    def open_on(self, rect, hold=0.4, dur=0.6, frm=None):
        """Open the scene on the full phone (zoom 1), hold, then zoom into rect (screenshot px).
        frm: a camera state carried in from the previous scene; it settles to the full phone first."""
        self.open_state = dict(BASE)
        if frm is not None:
            self.cam_set(frm)
            self.cam_to(self.start, BASE, dur=0.5)
            at = self.start + 0.5 + hold
        else:
            self.cam_set(BASE)
            at = self.start + hold
        self.cam_to(at, cam(*rect), dur=dur)

    # ---- phone screens --------------------------------------------------------
    def screen(self, key, abs_in, abs_out, enter="none", name=None):
        name = name or f"{self.id}-scr{len(self.screens)}"
        tin, tout = max(0.0, self.t(abs_in)), min(self.dur, self.t(abs_out))
        prev = self.screens[-1] if self.screens else None
        self.screens.append({"name": name, "key": key, "tin": tin, "tout": tout})
        if SHOT[key].endswith(".mp4"):
            # a recording is its own timed clip: fade the clip itself, never move it
            if enter != "none":
                self.js.append(f"tl.fromTo('#{name}', {{opacity:0}}, {{opacity:1, duration:0.22, ease:'power1.inOut'}}, {tin});")
            return name
        if enter == "push":
            self.js.append(f"tl.fromTo('#{name} img', {{xPercent:100}}, {{xPercent:0, duration:0.42, ease:'power3.out'}}, {tin});")
            if prev:
                self.js.append(f"tl.fromTo('#{prev['name']} img', {{xPercent:0, opacity:1}}, {{xPercent:-30, opacity:0.6, duration:0.42, ease:'power3.out', immediateRender:false}}, {tin});")
        elif enter == "fade":
            self.js.append(f"tl.fromTo('#{name} img', {{opacity:0}}, {{opacity:1, duration:0.22, ease:'power1.inOut'}}, {tin});")
        return name

    def phone_html(self, pid=None, screens=None, left=None, extra=""):
        pid = pid or f"{self.id}-phone"
        left = PL if left is None else left  # read after setup(), not at import
        screens = self.screens if screens is None else screens
        def one(i, s):
            src = SHOT[s["key"]]
            timing = f'data-start="{s["tin"]}" data-duration="{r(s["tout"]-s["tin"])}" data-track-index="2" style="z-index:{i+1}"'
            if src.endswith(".mp4"):
                return f'<video id="{s["name"]}" class="clip shot" src="assets/screens/{src}" {timing} muted playsinline></video>'
            return f'<div id="{s["name"]}" class="clip shot" {timing}><img src="assets/screens/{src}" alt="" /></div>'
        imgs = "\n".join(one(i, s) for i, s in enumerate(screens))
        return (f'<div id="{pid}" class="phone" style="left:{r(left)}px;top:{PT}px">'
                f'<div class="screen">{imgs}{extra}</div></div>')

    def tap(self, abs_t, rx, ry, rw, rh):
        n_taps = sum('class="tap"' in h for h in self.html)  # counts highlights only, not finger dots
        tid = f"{self.id}-tap{n_taps}"
        self.html.append(f'<div id="{tid}" class="tap" style="left:{r(rx*S)}px;top:{r(ry*S)}px;width:{r(rw*S)}px;height:{r(rh*S)}px"></div>')
        t = self.t(abs_t)
        self.js.append(f"tl.fromTo('#{tid}', {{opacity:0}}, {{opacity:1, duration:0.06}}, {t});"
                       f"tl.fromTo('#{tid}', {{opacity:1}}, {{opacity:0, duration:0.2, immediateRender:false}}, {r(t+0.12)});")
        # finger-tip dot: arrives 0.3 s early, presses with the highlight (sized to stay ~46 px on screen at the current zoom)
        d = r(46 / max(1.0, self.cam_state["scale"]))
        fx, fy = r((rx + rw / 2) * S - d / 2), r((ry + rh / 2) * S - d / 2)
        self.html.append(f'<div id="{tid}f" class="tap finger" style="left:{fx}px;top:{fy}px;width:{d}px;height:{d}px"></div>')
        self.js.append(f"tl.fromTo('#{tid}f', {{opacity:0, scale:1.5}}, {{opacity:1, scale:1, duration:0.25, ease:'power2.out'}}, {r(max(0, t-0.35))});"
                       f"tl.fromTo('#{tid}f', {{scale:1}}, {{scale:0.8, duration:0.08, ease:'power2.in', immediateRender:false}}, {t});"
                       f"tl.fromTo('#{tid}f', {{scale:0.8, opacity:1}}, {{scale:1, opacity:0, duration:0.3, ease:'power2.out', immediateRender:false}}, {r(t+0.1)});")

    # ---- focus outline ----------------------------------------------------------
    def ol(self, abs_t, rect=None):
        """Focus outline. Each target gets its own fixed box (animating left/top fails lint);
        the previous one fades as the next lands. ol(t) with no rect just hides the current one."""
        t = self.t(abs_t)
        if self.ol_state is not None:
            self.js.append(f"tl.fromTo('#{self.ol_state}', {{opacity:1}}, {{opacity:0, duration:0.15, immediateRender:false}}, {t});")
            self.ol_state = None
        if rect is None:
            return
        x, y, w, h = rect
        oid = f"{self.id}-ol{self.n_ol}"
        self.n_ol += 1
        self.ol_html.append(f'<div id="{oid}" class="ol" style="left:{r(x*S-3)}px;top:{r(y*S-3)}px;width:{r(w*S+6)}px;height:{r(h*S+6)}px"></div>')
        self.js.append(f"tl.fromTo('#{oid}', {{opacity:0, scale:1.08}}, {{opacity:1, scale:1, duration:0.3, ease:'expo.out'}}, {t});")
        self.ol_state = oid

    # ---- left-zone text -------------------------------------------------------
    def words_html(self, text, cls="w", accent=(), accent_color=None):
        accent_color = accent_color or C["brand"]
        return " ".join(f'<span class="{cls}"' + (f' style="color:{accent_color}"' if w in accent else "") + f'>{w}</span>'
                        for w in text.split(" "))

    def title(self, tid, text, abs_in, abs_out, x=120, y=380, size=84, color=None, style="blur",
              font="main", weight=800, width=760, extra_css="", accent=(), accent_color=None):
        """A title in the left zone. style: blur (per word) | grey (per word, grey to ink) | line (whole line)."""
        color = color or C["ink"]
        self.html.append(
            f'<div id="{tid}" class="ttl" style="left:{x}px;top:{y}px;width:{width}px;font-family:{font_family(font)};'
            f'font-weight:{weight};font-size:{size}px;color:{color};{extra_css}">{self.words_html(text, accent=accent, accent_color=accent_color)}</div>')
        t, to = self.t(abs_in), self.t(abs_out) if abs_out else None
        sel = f"#{tid} .w"
        if style == "blur":
            self.js.append(f"tl.fromTo('{sel}', {{opacity:0, filter:'blur(6px)'}}, {{opacity:1, filter:'blur(0px)', duration:0.13, stagger:0.067, ease:'power2.out'}}, {t});")
        elif style == "grey":
            self.js.append(f"tl.fromTo('{sel}', {{opacity:1, color:'rgba(27,38,32,0.18)'}}, {{color:'{color}', duration:0.1, stagger:0.085, ease:'none'}}, {t});")
        elif style == "line":
            self.js.append(f"tl.fromTo('#{tid}', {{opacity:0, filter:'blur(8px)'}}, {{opacity:1, filter:'blur(0px)', duration:0.18, ease:'power2.out'}}, {t});")
        if style != "line":
            self.js.append(f"tl.set('#{tid}', {{opacity:1}}, {t});")
        if to is not None:
            self.js.append(f"tl.fromTo('#{tid}', {{opacity:1, filter:'blur(0px)'}}, {{opacity:0, filter:'blur(8px)', duration:0.18, ease:'power2.in', immediateRender:false}}, {r(to-0.18)});")

    def amount(self, tid, label, value, color, abs_in, abs_out, x=120, y=360, size=132, count=True):
        self.html.append(
            f'<div id="{tid}" class="amt" style="left:{x}px;top:{y}px">'
            f'<div class="amt-l">{label}</div><div class="amt-v" style="color:{color};font-size:{size}px">{value}</div></div>')
        t, to = self.t(abs_in), self.t(abs_out)
        self.js.append(f"tl.fromTo('#{tid} .amt-l', {{opacity:0, filter:'blur(6px)'}}, {{opacity:1, filter:'blur(0px)', duration:0.16, ease:'power2.out'}}, {t});"
                       f"tl.fromTo('#{tid} .amt-v', {{opacity:0, y:24, filter:'blur(10px)'}}, {{opacity:1, y:0, filter:'blur(0px)', duration:0.3, ease:'expo.out'}}, {r(t+0.08)});"
                       f"tl.set('#{tid}', {{opacity:1}}, {t});"
                       f"tl.fromTo('#{tid}', {{opacity:1, filter:'blur(0px)'}}, {{opacity:0, filter:'blur(8px)', duration:0.18, ease:'power2.in', immediateRender:false}}, {r(to-0.18)});")
        if count:
            n = int("".join(ch for ch in value if ch.isdigit()))
            prefix = value[:next(i for i, ch in enumerate(value) if ch.isdigit())]
            self.js.append(f"(() => {{ const el = document.querySelector('#{tid} .amt-v'); const o = {{v:0}};"
                           f" tl.fromTo(o, {{v:0}}, {{v:{n}, duration:0.6, ease:'power2.out',"
                           f" onUpdate:() => {{ el.textContent = '{prefix}' + Math.round(o.v).toLocaleString('en-IN'); }} }}, {r(t+0.08)}); }})();")

    def items(self, lid, entries, abs_out, x=120, y=300, size=64, gap=1.45, style="blur", font="display", color=None):
        """A list that grows one line per spoken word: entries = [(text, abs_time), ...]."""
        color = color or C["ink"]
        rows = "".join(f'<div class="li" id="{lid}-{i}">{txt}</div>' for i, (txt, _) in enumerate(entries))
        self.html.append(f'<div id="{lid}" class="lst" style="left:{x}px;top:{y}px;font-family:{font_family(font)};font-size:{size}px;line-height:{gap};color:{color}">{rows}</div>')
        self.js.append(f"tl.set('#{lid}', {{opacity:1}}, 0);")
        for i, (_, at) in enumerate(entries):
            t = self.t(at)
            if style == "blur":
                self.js.append(f"tl.fromTo('#{lid}-{i}', {{opacity:0, filter:'blur(8px)'}}, {{opacity:1, filter:'blur(0px)', duration:0.16, ease:'power2.out'}}, {t});")
            else:
                self.js.append(f"tl.fromTo('#{lid}-{i}', {{opacity:0, color:'rgba(27,38,32,0.16)'}}, {{opacity:1, color:'{color}', duration:0.28, ease:'power1.out'}}, {t});")
        if abs_out:
            self.js.append(f"tl.fromTo('#{lid}', {{opacity:1, filter:'blur(0px)'}}, {{opacity:0, filter:'blur(8px)', duration:0.18, ease:'power2.in', immediateRender:false}}, {r(self.t(abs_out)-0.18)});")

    def lift(self, key, abs_in, abs_out, rect, k=2.2, check=True):
        """Lift a real screenshot region out of the phone: re-drawn crisp at k x, rising beside the phone,
        held while the voice names it, then settling back. Moves the camera to the full phone first."""
        if self.cam_state != BASE:
            self.cam_to(abs_in - 0.55, BASE, dur=0.5)
        x, y, w, h = rect
        lid = f"{self.id}-lift{self.n_lift}"
        self.n_lift += 1
        bw, bh = w * S * k, h * S * k
        cx0, cy0 = OX + (x + w / 2) * S, OY + (y + h / 2) * S
        x0, y0, x1, y1 = LIFT_BOX
        tx = min(max(cx0, x0 + bw / 2), x1 - bw / 2)
        ty = min(max(cy0 + LIFT_DY, y0 + bh / 2), y1 - bh / 2)
        badge = '<div class="lift-ok">✓</div>' if check else ""
        self.lift_html.append(
            f'<div id="{lid}" class="lift" style="left:{r(cx0-bw/2)}px;top:{r(cy0-bh/2)}px;width:{r(bw)}px;height:{r(bh)}px;'
            f'background-image:url(assets/screens/{SHOT[key]});background-size:{r(SW*k)}px {r(SH*k)}px;'
            f'background-position:{r(-x*S*k)}px {r(-y*S*k)}px">{badge}</div>')
        t, to = self.t(abs_in), self.t(abs_out)
        self.js.append(
            f"tl.fromTo('#{lid}', {{opacity:0, scale:{r(1/k)}, x:0, y:0}}, {{opacity:1, duration:0.08}}, {t});"
            f"tl.fromTo('#{lid}', {{scale:{r(1/k)}, x:0, y:0, filter:'blur(0px)'}}, {{scale:1, x:{r(tx-cx0)}, y:{r(ty-cy0)}, duration:0.5, ease:'expo.out', immediateRender:false}}, {t});"
            f"tl.fromTo('#{lid}', {{scale:1, x:{r(tx-cx0)}, y:{r(ty-cy0)}}}, {{scale:{r(1/k)}, x:0, y:0, duration:0.35, ease:'power2.in', immediateRender:false}}, {r(to-0.4)});"
            f"tl.fromTo('#{lid}', {{opacity:1}}, {{opacity:0, duration:0.05, immediateRender:false}}, {r(to-0.05)});")
        if check:
            self.js.append(f"tl.fromTo('#{lid} .lift-ok', {{scale:0, opacity:0}}, {{scale:1, opacity:1, duration:0.3, ease:'back.out(2)'}}, {r(t+0.45)});")

    def sweep_out(self, color, dur=0.45):
        """A giant rounded brand shape sweeps in from the bottom right and covers the frame at the scene's end."""
        self.html.append(f'<div id="{self.id}-swo" class="sweep" style="background:{color};opacity:0"></div>')
        self.js.append(f"tl.fromTo('#{self.id}-swo', {{x:2700, y:1500, opacity:1}}, {{x:0, y:0, opacity:1, duration:{dur}, ease:'power2.in'}}, {r(self.dur-dur)});")

    def sweep_in(self, color, dur=0.5):
        """The covering shape continues off to the top left, revealing this scene."""
        self.html.append(f'<div id="{self.id}-swi" class="sweep" style="background:{color}"></div>')
        self.js.append(f"tl.fromTo('#{self.id}-swi', {{x:0, y:0}}, {{x:-2700, y:-1500, duration:{dur}, ease:'power2.out'}}, 0);")

    # ---- transitions ------------------------------------------------------------
    def whip_in(self):
        a = dict(getattr(self, "open_state", None) or self.cam_state)
        b = dict(a)
        a["x"] = a["x"] + 1100
        self.js.append(f"tl.fromTo('#{self.id}-cam', {{...{json.dumps(a)}, filter:'blur(18px)'}}, {{...{json.dumps(b)}, filter:'blur(0px)', duration:0.38, ease:'power3.out'}}, 0);")

    def whip_out(self):
        a = dict(self.cam_state)
        b = dict(a)
        b["x"] = a["x"] - 1100
        self.js.append(f"tl.fromTo('#{self.id}-cam', {{...{json.dumps(a)}, filter:'blur(0px)'}}, {{...{json.dumps(b)}, filter:'blur(18px)', duration:0.35, ease:'power3.in', immediateRender:false}}, {r(self.dur-0.35)});")
        self.cam_state = b

    def flood(self, color, abs_in, dur, frm, to, fid=None):
        """Full-frame colour flood (0 -> 1 to leave a scene, 1 -> 0 to enter the next)."""
        n_floods = sum('class="flood"' in h for h in self.html)
        fid = fid or f"{self.id}-flood{n_floods}"
        self.html.append(f'<div id="{fid}" class="flood" style="background:{color}"></div>')
        self.js.append(f"tl.fromTo('#{fid}', {{opacity:{frm}}}, {{opacity:{to}, duration:{dur}, ease:'power2.inOut', immediateRender:{'true' if self.t(abs_in) <= 0 else 'false'}}}, {max(0.0, self.t(abs_in))});")

    def dip(self):
        """Dip cut: darken 40% over the last 3 frames."""
        self.html.append(f'<div id="{self.id}-dip" class="flood" style="background:#000"></div>')
        self.js.append(f"tl.fromTo('#{self.id}-dip', {{opacity:0}}, {{opacity:0.4, duration:0.1}}, {r(self.dur-0.1)});")

    # ---- output -----------------------------------------------------------------
    def write(self, stage_html, ground=None):
        ground = ground or C["ground"]
        body = "\n".join(self.html)
        css = "\n".join(self.css)
        js = "\n".join(self.js)
        out = f"""<template>
  <style>
    #root {{ position:absolute; inset:0; overflow:hidden; background:{ground}; }}
{css}
  </style>
  <div id="root" data-composition-id="{self.id}" data-width="{W}" data-height="{H}">
{stage_html}
{body}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
{js}
    window.__timelines["{self.id}"] = tl;
  </script>
</template>
"""
        (ROOT / "compositions" / f"{self.id}.html").write_text(out)


def phone_stage(sc, extra_in_screen="", patch=True):
    """Camera wrapper with the light patch, the phone, its focus outlines and taps."""
    taps = "".join(h for h in sc.html if 'class="tap' in h)
    sc.html = [h for h in sc.html if 'class="tap' not in h]
    ol = "".join(sc.ol_html)
    patch_html = '<div class="patch"></div>' if patch else ""
    return (f'{patch_html}<div id="{sc.id}-cam" class="cam" data-layout-allow-overflow>'
            f'{sc.phone_html(extra=taps + ol + extra_in_screen)}</div>' + "".join(sc.lift_html))


# =====================================================================================
# captions
# =====================================================================================
def build_captions(caps, bottom=52, size=44):
    """caps = [(abs_start, abs_end, text)], one group on screen at a time.
    Leave out lines whose words are already a title on screen."""
    groups, js = [], []
    for i, (a, b, text) in enumerate(caps):
        d = r(b - a + 0.12)
        groups.append(f'<div id="cap{i}" class="clip cap" data-start="{a}" data-duration="{d}" data-track-index="5">'
                      f'<div class="cap-row"><span class="cap-t">{text}</span></div></div>')
        js.append(f"tl.fromTo('#cap{i} .cap-t', {{opacity:0, filter:'blur(4px)'}}, {{opacity:1, filter:'blur(0px)', duration:0.12, ease:'power2.out'}}, {a});")
        js.append(f"tl.fromTo('#cap{i} .cap-t', {{opacity:1}}, {{opacity:0, duration:0.1, ease:'power2.in', immediateRender:false}}, {r(a + d - 0.1)});")
    out = f"""<template>
  <style>
    #root {{ position:absolute; inset:0; pointer-events:none; }}
    .cap {{ position:absolute; left:0; top:0; width:{W}px; height:{H}px; }}
    .cap-row {{ position:absolute; left:0; width:{W}px; bottom:{bottom}px; text-align:center; overflow:visible; }}
    .cap-t {{ display:inline-block; white-space:nowrap;
      font-family:var(--font-main); font-weight:600; font-size:{size}px; line-height:1.3; color:{C['ink']};
      background:rgba(246,239,231,0.92); padding:8px 26px 10px; border-radius:10px; opacity:0; }}
  </style>
  <div id="root" data-composition-id="captions" data-width="{W}" data-height="{H}">
{chr(10).join(groups)}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
{chr(10).join(js)}
    window.__timelines["captions"] = tl;
  </script>
</template>
"""
    (ROOT / "compositions" / "captions.html").write_text(out)


# =====================================================================================
# index
# =====================================================================================
def build_index(sfx=(), voiceover="assets/audio/voiceover.wav", vo_volume=1.0, music=None, music_volume=0.14,
                music_start=0.0, music_media_start=0.0, music_lane=None, music_fade_out=2.0):
    """Root composition: scene hosts, captions host, voiceover, optional music bed and SFX.
    sfx = [(id, file in assets/sfx/, abs_time, volume)]; each gets its own track.
    A mono voiceover at -16 LUFS measures ~3 LU louder once rendered to stereo: vo_volume 0.85 lands the mix near -14.5."""
    hosts = "\n".join(
        f'      <div id="{sid}" data-composition-id="{sid}" data-composition-src="compositions/{sid}.html" data-start="{a}" '
        f'data-duration="{r(b-a)}" data-track-index="1" data-track-kind="graphics" data-width="{W}" data-height="{H}" style="z-index:{i+1}"></div>'
        for i, (sid, a, b) in enumerate(SCENES))
    sfx_html = "\n".join(
        f'      <audio id="{i}" class="clip" src="assets/sfx/{f}" data-start="{t}" data-track-index="{11 + n}" data-volume="{v}"></audio>'
        for n, (i, f, t, v) in enumerate(sfx))
    # music: enter on a bar line (music_start on the film, music_media_start into the track), duck with a volume lane
    # [(t, v), ...] in clip seconds; without a lane the bed sits at music_volume throughout
    lane = ""
    if music_lane:
        pts = ",".join(f'{{&quot;t&quot;:{t},&quot;v&quot;:{v}}}' for t, v in music_lane)
        lane = f' data-automation="{{&quot;version&quot;:1,&quot;lanes&quot;:[{{&quot;target&quot;:&quot;volume&quot;,&quot;points&quot;:[{pts}]}}]}}"'
    music_html = (f'      <audio id="music" class="clip" src="{music}" data-start="{music_start}" data-media-start="{music_media_start}" '
                  f'data-duration="{r(TOTAL - music_start)}" data-track-index="9" data-volume="{1 if music_lane else music_volume}" '
                  f'data-fade-out="{music_fade_out}"{lane}></audio>') if music else ""
    font_faces = "\n".join(
        f"      @font-face {{ font-family:'{fam}'; src:url('assets/fonts/{file}'); font-weight:{wt}; }}" for fam, file, wt in FONTS)
    vars_ = json.dumps([
        {"id": "color-ground", "type": "color", "label": "Background", "default": C["ground"]},
        {"id": "color-ink", "type": "color", "label": "Text", "default": C["ink"]},
        {"id": "color-accent", "type": "color", "label": "Brand colour", "default": C["brand"]},
    ], ensure_ascii=False)
    out = f"""<!doctype html>
<html lang="{LANG}" data-resolution="{'portrait' if H > W else 'landscape'}" data-composition-variables='{vars_}'>
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={W}, height={H}" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
{font_faces}
      :root {{
        --ground: {C['ground']};
        --ink: {C['ink']};
        --font-main: {FONT_MAIN};
        --font-display: {FONT_DISPLAY};
      }}
      * {{ margin:0; padding:0; box-sizing:border-box; }}
      html, body {{ margin:0; width:{W}px; height:{H}px; overflow:hidden; background:var(--ground); }}
      #root {{ position:relative; width:100%; height:100%; }}
      .patch {{ position:absolute; left:{r(PL + PW / 2 - 460)}px; top:{PT - 140}px; width:1000px; height:{r(PH + 389)}px; border-radius:50%;
        background:radial-gradient(closest-side, {C['patch']} 0%, rgba(251,247,241,0) 100%); }}
      .cam {{ position:absolute; left:0; top:0; width:{W}px; height:{H}px; transform-origin:0 0; }}
      .phone {{ position:absolute; width:{r(PW)}px; height:{r(PH)}px; padding:{BEZ}px; background:#111; border-radius:{SCREEN_RADIUS+BEZ}px;
        box-shadow:0 30px 60px rgba(27,38,32,0.18), inset 0 0 0 2px #2a2a2a; }}
      .screen {{ position:relative; width:{r(SW)}px; height:{r(SH)}px; border-radius:{SCREEN_RADIUS}px; overflow:hidden; background:{C['ground']}; }}
      .screen > .shot {{ position:absolute; left:0; top:0; width:100%; height:100%; overflow:hidden; }}
      .screen > video.shot {{ object-fit:fill; display:block; }}
      .screen > .shot > img {{ position:absolute; left:0; top:0; width:100%; height:100%; display:block; }}
      .tap {{ position:absolute; background:rgba(27,38,32,0.14); border-radius:8px; opacity:0; z-index:40; }}
      .finger {{ background:rgba(27,38,32,0.30); border:2px solid rgba(255,255,255,0.85); border-radius:50%; z-index:42;
        box-shadow:0 4px 10px rgba(27,38,32,0.25); }}
      .lift {{ position:absolute; border-radius:22px; opacity:0; z-index:45; background-repeat:no-repeat; background-color:#fff;
        box-shadow:0 30px 70px rgba(27,38,32,0.28), 0 0 0 1px rgba(27,38,32,0.06); }}
      .lift-ok {{ position:absolute; right:-22px; top:-22px; width:64px; height:64px; border-radius:50%; background:{C['brand']};
        color:#fff; font-family:var(--font-display); font-weight:800; font-size:38px; line-height:64px; text-align:center; opacity:0;
        box-shadow:0 8px 18px rgba(27,38,32,0.25); }}
      .sweep {{ position:absolute; left:{W // 2 - 1700}px; top:{H // 2 - 1700}px; width:3400px; height:3400px; border-radius:50%; z-index:70; }}
      .ol {{ position:absolute; border:2.2px solid {C['accent']}; border-radius:9px; opacity:0; z-index:41;
        box-shadow:0 0 0 1px rgba(232,162,58,0.25); }}
      .ttl {{ position:absolute; line-height:1.25; opacity:0; }}
      .amt {{ position:absolute; opacity:0; }}
      .amt-l {{ font-family:var(--font-main); font-weight:700; font-size:48px; color:{C['ink2']}; }}
      .amt-v {{ font-family:var(--font-display); font-weight:800; line-height:1.05; letter-spacing:-0.01em; }}
      .lst {{ position:absolute; font-weight:800; opacity:0; }}
      .flood {{ position:absolute; inset:0; opacity:0; z-index:60; }}
      .icon {{ position:absolute; width:150px; height:150px; border-radius:34px; opacity:0; box-shadow:0 18px 36px rgba(27,38,32,0.18); }}
      .pro {{ position:absolute; display:flex; align-items:center; gap:18px; opacity:0; }}
      .pro-tag {{ font-family:var(--font-display); font-weight:800; font-size:40px; color:#1B2620; background:{C['accent']}; padding:4px 16px; border-radius:8px; }}
      .pro-t {{ font-family:var(--font-main); font-weight:700; font-size:48px; color:{C['ink']}; }}
      .sig {{ position:absolute; width:200px; height:150px; opacity:0; }}
      .bar {{ position:absolute; bottom:0; width:32px; background:{C['ink']}; border-radius:6px; }}
      .sig-x {{ position:absolute; left:200px; top:-30px; font-family:var(--font-display); font-weight:800; font-size:140px; color:{C['alert']}; opacity:0; }}
      .ul {{ position:absolute; width:640px; height:10px; background:{C['brand']}; border-radius:5px; transform-origin:0 50%; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="{W}" data-height="{H}">
{hosts}
      <div id="captions" data-composition-id="captions" data-composition-src="compositions/captions.html" data-start="0" data-duration="{TOTAL}" data-track-index="4" data-track-kind="captions" data-width="{W}" data-height="{H}" style="z-index:50"></div>
      <audio id="vo" class="clip" src="{voiceover}" data-start="0" data-track-index="10" data-volume="{vo_volume}"></audio>
{music_html}
{sfx_html}
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
"""
    (ROOT / "index.html").write_text(out)
