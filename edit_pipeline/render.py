"""Frame renderer for the noodle-battle reel.
usage: python3 render.py <worker_idx> <n_workers>   -> writes part_<idx>.mkv
       python3 render.py plan                         -> writes plan.json (output frame -> source mapping)
       python3 render.py still <out_frame> [...]      -> writes still_<f>.jpg for QA
"""
import sys, json, math, subprocess, collections, random
import numpy as np, cv2
import gfx
from edl import CLIPS, EVENTS, CARDS, HANDLE, ENDCARD_SEC, SRC, FPS

W, H = 1080, 1920
SW, SH = 720, 1280
WORK = "/tmp/claude-0/-home-user-Testclaude/f29330e6-8f24-5182-bfb1-c06071f78d9b/scratchpad/work"
ASSETS = "/tmp/claude-0/-home-user-Testclaude/f29330e6-8f24-5182-bfb1-c06071f78d9b/scratchpad/assets"

FACES = np.array(json.load(open(f"{WORK}/faces.json"))["faces"], np.float32)
MASKS = np.load(f"{WORK}/masks.npy", mmap_mode="r")
NSRC = len(FACES)


# ------------------------------------------------------------------ plan: output frame -> (clip, src time)
def build_plan():
    plan = []
    for ci, c in enumerate(CLIPS):
        a, b = c["src"]
        ramp = c.get("ramp")  # (r0, r1, speed) source-time window played at `speed`
        t = a
        k = 0
        while t < b - 1e-6:
            plan.append({"clip": ci, "t": round(t, 5), "k": k})
            sp = 1.0
            if ramp and ramp[0] <= t < ramp[1]:
                sp = ramp[2]
            t += sp / FPS
            k += 1
    n_main = len(plan)
    for k in range(int(round(ENDCARD_SEC * FPS))):
        plan.append({"clip": -1, "t": None, "k": k})
    return plan, n_main


PLAN, N_MAIN = build_plan()
CLIP_START = {}
for i, p in enumerate(PLAN):
    CLIP_START.setdefault(p["clip"], i)


def src_to_out(ts):
    """first output frame whose source time >= ts"""
    for i, p in enumerate(PLAN[:N_MAIN]):
        if p["t"] >= ts - 1e-4:
            return i
    return N_MAIN - 1


for e in EVENTS:
    e["f0"] = src_to_out(e["t0"]) if "t0" in e else e["out0"]
    e["f1"] = src_to_out(e["t1"]) if "t1" in e else e.get("out1", e["f0"] + 30)
    for wd in e.get("words", []):
        wd["f"] = src_to_out(wd["t"])
for cd in CARDS:
    cd["f0"] = src_to_out(cd["t0"]); cd["f1"] = src_to_out(cd["t1"])


# ------------------------------------------------------------------ grading
def _curve():
    x = np.arange(256) / 255.0
    y = x ** (1 / 1.06)                      # ~ +0.25 stop lift in mids
    y = y + 0.06 * np.sin(2 * np.pi * (y - 0.5)) * 0  # placeholder
    s = 0.5 + (y - 0.5) * 1.08               # gentle S / contrast
    s = 0.047 + s * (0.975 - 0.047)          # blacks lifted to ~12/255, highlight roll-off
    s = np.where(s > 0.88, 0.88 + (s - 0.88) * 0.6, s)
    return np.clip(s * 255, 0, 255).astype(np.uint8)


LUT = _curve()


def grade(rgb):
    img = cv2.LUT(rgb, LUT).astype(np.float32) / 255.0
    lum = img @ np.array([0.299, 0.587, 0.114], np.float32)
    # selective saturation: boost warm hues (shirt / noodles / packs) more than neutrals
    r, g, b = img[..., 0], img[..., 1], img[..., 2]
    warm = np.clip((r - b) * 3.0, 0, 1)
    sat = 1.10 + 0.10 * warm
    img = lum[..., None] + (img - lum[..., None]) * sat[..., None]
    # neutral-warm white balance, walls to clean ivory
    img *= np.array([1.015, 1.0, 0.975], np.float32)
    return np.clip(img, 0, 1)


def bloom(img):
    small = cv2.resize(img, (270, 480), interpolation=cv2.INTER_AREA)
    lum = small.max(axis=2)
    hi = small * np.clip((lum - 0.85) / 0.15, 0, 1)[..., None]
    hi = cv2.GaussianBlur(hi, (0, 0), 10)
    return np.clip(img + 0.15 * cv2.resize(hi, (W, H), interpolation=cv2.INTER_LINEAR), 0, 1)


rng = np.random.default_rng(7)
GRAIN = [(rng.standard_normal((H // 2, W // 2)).astype(np.float32) * 0.02) for _ in range(6)]
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
VIGNETTE = (1 - 0.08 * np.clip(((xx / W - .5) ** 2 + (yy / H - .5) ** 2 * 0.6) * 3.2, 0, 1))[..., None]
VIG_BW = (1 - 0.15 * np.clip(((xx / W - .5) ** 2 + (yy / H - .5) ** 2 * 0.6) * 3.2, 0, 1))[..., None]


# ------------------------------------------------------------------ source reader (sequential, small cache)
class Source:
    def __init__(self, start_frame):
        self.start = max(0, start_frame - 2)
        ss = self.start / FPS
        self.p = subprocess.Popen(["ffmpeg", "-v", "error", "-ss", f"{ss:.4f}", "-i", SRC, "-f", "rawvideo",
                                   "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE, bufsize=SW * SH * 3 * 4)
        self.idx = self.start - 1
        self.cache = collections.OrderedDict()

    def get(self, i):
        i = max(0, min(NSRC - 1, i))
        if i in self.cache:
            return self.cache[i]
        if i < self.idx - 1 and i not in self.cache:
            return still_frame(i)
        while self.idx < i:
            buf = self.p.stdout.read(SW * SH * 3)
            if len(buf) < SW * SH * 3:
                break
            self.idx += 1
            fr = grade(np.frombuffer(buf, np.uint8).reshape(SH, SW, 3))
            self.cache[self.idx] = fr
            while len(self.cache) > 6:
                self.cache.popitem(last=False)
        return self.cache.get(i, self.cache[next(reversed(self.cache))])


_still = {}


def still_frame(i):
    if i not in _still:
        out = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{i / FPS:.4f}", "-i", SRC, "-frames:v", "1", "-f", "rawvideo",
                              "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
        _still[i] = grade(np.frombuffer(out[:SW * SH * 3], np.uint8).reshape(SH, SW, 3))
    return _still[i]


# ------------------------------------------------------------------ camera
def crop_box(si, zoom, focus):
    """returns (x0, y0, cw, ch) crop in source px."""
    cw, ch = SW / zoom, SH / zoom
    fx, fy, fw, fh = FACES[min(si, NSRC - 1)]
    if focus == "face":
        cx, cy = fx, fy + ch * (0.5 - 0.36)
    elif isinstance(focus, (list, tuple)) and focus[0] == "face+":
        cx, cy = fx + focus[1], fy + ch * (0.5 - 0.36) + focus[2]
    else:
        cx, cy = focus
    x0 = min(max(cx - cw / 2, 0), SW - cw)
    y0 = min(max(cy - ch / 2, 0), SH - ch)
    return x0, y0, cw, ch


def render_cam(img, mask, box, ox=0, oy=0):
    x0, y0, cw, ch = box
    sx, sy = W / cw, H / ch
    Mx = np.array([[sx, 0, -x0 * sx + ox], [0, sy, -y0 * sy + oy]], np.float32)
    fr = cv2.warpAffine(img, Mx, (W, H), flags=cv2.INTER_LANCZOS4, borderMode=cv2.BORDER_REFLECT)
    Mm = Mx.copy(); Mm[:, :2] *= 2  # mask is half-res (360x640)
    mk = cv2.warpAffine(mask.astype(np.float32) / 255.0, np.array([[sx * 2, 0, -x0 * sx + ox], [0, sy * 2, -y0 * sy + oy]], np.float32),
                        (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
    zoom = SW / cw
    if zoom > 1.05:  # unsharp after digital zoom
        bl = cv2.GaussianBlur(fr, (0, 0), 1.6)
        fr = np.clip(fr + 0.6 * (fr - bl), 0, 1)
    return fr, np.clip(mk, 0, 1)


def zoom_blur(fr, strength, cx=W / 2, cy=H * .36):
    if strength <= 0.002:
        return fr
    acc = np.zeros_like(fr)
    n = 6
    for i in range(n):
        s = 1 + strength * i / (n - 1)
        Mx = cv2.getRotationMatrix2D((cx, cy), 0, s)
        acc += cv2.warpAffine(fr, Mx, (W, H), borderMode=cv2.BORDER_REFLECT)
    return acc / n


def dir_blur(fr, px, horizontal=True):
    if px < 2:
        return fr
    k = np.zeros((1, px) if horizontal else (px, 1), np.float32); k[:] = 1 / px
    return cv2.filter2D(fr, -1, k)


def desat(fr, amt):
    lum = (fr @ np.array([0.299, 0.587, 0.114], np.float32))[..., None]
    return fr * (1 - amt) + lum * amt


# ------------------------------------------------------------------ transitions
LEAK_W = [0.92, 0.97, 0.75, 0.6, 0.48, 0.38, 0.3, 0.22, 0.15, 0.09, 0.04, 0.0]
TURMERIC = np.array([1.0, 0.76, 0.10], np.float32)
TERRA = np.array([0.85, 0.35, 0.17], np.float32)


def light_leak(fr, k):
    if not 0 <= k < 12:
        return fr
    w = LEAK_W[k]
    t = k / 11
    out = fr * (1 - w) + w
    # moving film-burn blobs (screen blend)
    for col, (sx, sy, ex, ey, rad) in ((TURMERIC, (-0.3, -0.2, 1.2, 1.1, 0.75)), (TERRA, (1.3, -0.1, -0.2, 1.0, 0.6)),
                                       (np.array([1, .55, .15], np.float32), (0.2, 1.2, 0.8, -0.2, 0.5))):
        px, py = (sx + (ex - sx) * t) * W, (sy + (ey - sy) * t) * H
        d = np.sqrt(((xx - px) / W) ** 2 + ((yy - py) / H) ** 2 * 0.5) / rad
        inten = np.clip(1 - d, 0, 1) ** 1.6 * math.sin(math.pi * min(1, (k + 1) / 10)) * 0.95
        layer = col[None, None, :] * inten[..., None]
        out = 1 - (1 - out) * (1 - layer)
    return np.clip(out, 0, 1)


def red_flash(fr, k):
    if k in (0, 1):
        return fr * 0.15 + np.array([1.0, 0.165, 0.10], np.float32) * 0.85
    if k in (2, 3):
        return fr * 0.2 + np.array([1.0, 0.95, 0.70], np.float32) * 0.8
    return fr


def white_flash(fr, k, n=4):
    w = [0.9, 0.7, 0.4, 0.15][k] if 0 <= k < n else 0
    return fr * (1 - w) + w


# ------------------------------------------------------------------ text helpers
def draw_build(dst, ev, f, color_override=None):
    """word-by-word build; line re-centres as words appear; supports multiple lines."""
    words = ev["words"]
    vis = [w for w in words if f >= w["f"]]
    if not vis:
        return
    size = ev.get("size", 110)
    style = color_override or ev.get("style", "reaction")
    lines = {}
    for w in vis:
        lines.setdefault(w.get("line", 0), []).append(w)
    lh = int(size * 1.15) if style != "white" else int(size * 1.25)
    for li, ws in lines.items():
        sprites = [gfx.plain_caption(w["w"], size) if style == "white" else gfx.neon_text(w["w"], size, w.get("style", style)) for w in ws]
        widths = [s.shape[1] - (60 if style == "white" else int(25 * 2.2 + 20) * 2) for s in sprites]
        gap = int(size * 0.28)
        total = sum(widths) + gap * (len(widths) - 1)
        x = W / 2 - total / 2
        y = ev["y"] * H + li * lh
        for w, s, wd in zip(ws, sprites, widths):
            df = f - w["f"]
            sc = gfx.pop_scale(df) * ev.get("scale", 1.0)
            a = 1.0
            if f > ev["f1"] - 4 and ev.get("fade", True):
                a = max(0, (ev["f1"] - f) / 4)
            gfx.blend(dst, s, x + wd / 2, y, alpha=a * (gfx.glow_flicker(df) if style != "white" else 1), scale=sc)
            x += wd + gap


def draw_title(dst, ev, f):
    df = f - ev["f0"]
    text = ev["text"]
    style = ev.get("style", "hook")
    if ev.get("typewriter"):
        n = min(len(text), df // 2 + 1)
        text = text[:n]
        s = gfx.neon_text(text, ev.get("size", 130), style)
        sc = 1.0
    else:
        s = gfx.neon_text(text, ev.get("size", 130), style)
        sc = gfx.pop_scale(df)
    if ev.get("text2"):
        mf = ev["_mf"] = ev.get("_mf") or src_to_out(ev["morph_t"])
        if f >= mf:
            u = min(1, (f - mf) / 6)
            s2 = gfx.neon_text(ev["text2"], ev.get("size", 130), style)
            sc2 = 1 + 0.1 * math.sin(math.pi * u)
            gfx.blend(dst, s, W / 2, ev["y"] * H, alpha=1 - u, scale=sc2 * ev.get("scale", 1.0))
            gfx.blend(dst, s2, W / 2, ev["y"] * H, alpha=u, scale=sc2 * ev.get("scale", 1.0))
            return
    a = 1.0
    if ev.get("fade_out", True) and f > ev["f1"] - 4:
        a = max(0, (ev["f1"] - f) / 4)
    gfx.blend(dst, s, W / 2 + ev.get("dx", 0), ev["y"] * H, alpha=a * gfx.glow_flicker(df), scale=sc * ev.get("scale", 1.0))


def ease_out_back(t):
    c1 = 1.70158; c3 = c1 + 1
    return 1 + c3 * (t - 1) ** 3 + c1 * (t - 1) ** 2


# ------------------------------------------------------------------ static assets
PACK = {"chings": cv2.cvtColor(cv2.imread(f"{ASSETS}/pack_chings.png", cv2.IMREAD_UNCHANGED), cv2.COLOR_BGRA2RGBA),
        "slurrp": cv2.cvtColor(cv2.imread(f"{ASSETS}/pack_slurrp.png", cv2.IMREAD_UNCHANGED), cv2.COLOR_BGRA2RGBA)}
METER, METER_PIV, METER_R = gfx.spice_meter(980)
NEEDLE = gfx.needle(int(METER_R * 0.78))


def pack_tinted(name):
    """grade the pack cut-out like the footage"""
    p = PACK[name].copy()
    p[..., :3] = (grade(np.ascontiguousarray(p[..., :3])) * 255).astype(np.uint8)
    return p


PACK_G = {k: pack_tinted(k) for k in PACK}


def meter_layer(dst, ev, f):
    df = f - ev["f0"]
    dur = ev["f1"] - ev["f0"]
    # entrance: 40% -> 100 % with slight spin + fade (8 f); exit: scale-out (5 f)
    if df < 8:
        t = df / 8; e = 1 - (1 - t) ** 3
        sc, ang, a = 0.4 + 0.6 * e, -25 * (1 - e), e
    elif df > dur - 5:
        t = (df - (dur - 5)) / 5
        sc, ang, a = 1 - 0.6 * t, 0, 1 - t
    else:
        sc, ang, a = 1, 0, 1
    sc *= ev.get("scale", 0.92)
    cx, cy = W / 2, ev.get("y", 0.30) * H
    # needle angle: keyframes (frame_offset, value 0..1)
    kf = ev["needle"]
    v = kf[0][1]
    for (fa, va), (fb, vb) in zip(kf, kf[1:]):
        if fa <= df <= fb:
            u = (df - fa) / max(1, fb - fa); u = u * u * (3 - 2 * u); v = va + (vb - va) * u
    if df > kf[-1][0]:
        v = kf[-1][1]
    wob = ev.get("wobble_at")
    if wob is not None and df >= wob:
        v += 0.06 * math.exp(-(df - wob) / 6) * math.sin((df - wob) * 1.6)
    v += 0.012 * math.sin(df * 1.3)  # live twitch
    v = min(max(v, -0.02), 1.03)
    mh, mw = METER.shape[:2]
    gfx.blend(dst, METER, cx, cy, alpha=a, scale=sc, angle=ang)
    # pivot location after scale (no rotation applied to needle placement during spin; small)
    px = cx + (METER_PIV[0] - mw / 2) * sc
    py = cy + (METER_PIV[1] - mh / 2) * sc
    needle_ang = 180 - v * 180  # degrees CCW from +x: 180 = left (cool), 0 = right (hot)
    # motion-blur trail
    prev = ev.setdefault("_prev", {}).get(f - 1, needle_ang)
    for tr in (0.66, 0.33):
        gfx.blend(dst, NEEDLE, px, py, alpha=a * 0.25, scale=sc, angle=prev + (needle_ang - prev) * tr + ang)
    gfx.blend(dst, NEEDLE, px, py, alpha=a, scale=sc, angle=needle_ang + ang)
    ev["_prev"][f] = needle_ang


def qmarks(dst, ev, f, layer):
    """glossy 3D question marks around head; layer 'back' or 'front'."""
    df = f - ev["f0"]
    hx, hy = ev["_head"]
    for i, (dx, dy, px, back) in enumerate(ev["marks"]):
        st = i * 3
        if df < st or bool(back) != (layer == "back"):
            continue
        d = df - st
        sc = gfx.pop_scale(d)
        rise = d * 2.2
        q = gfx.question_mark(px)
        a = 1.0 if f < ev["f1"] - 4 else max(0, (ev["f1"] - f) / 4)
        blur = 5 if px >= 230 and not back else 0
        gfx.blend(dst, q, hx + dx, hy + dy - rise, alpha=a, scale=sc, angle=math.sin(d * .2 + i) * 8, blur=blur)


def burst(dst, ev, f):
    """emoji burst: from lower-left, arcing up and out of the top."""
    df = f - ev["f0"]
    random.seed(ev.get("seed", 1))
    n = ev.get("n", 8)
    for i in range(n):
        ch = ev["emoji"][i % len(ev["emoji"])]
        px = random.choice([90, 120, 150, 180, 220])
        st = i * 3
        d = df - st
        if d < 0:
            continue
        T = ev.get("travel", 30)
        t = d / T
        if t > 1.15:
            continue
        x0, y0 = W * (0.08 + random.random() * 0.12), H * 1.04
        x1 = W * (0.35 + random.random() * 0.6)
        y1 = -H * 0.12
        xm, ym = W * (0.05 + random.random() * 0.3), H * (0.25 + random.random() * 0.2)
        u = 1 - (1 - min(t, 1.15)) ** 1.6 if t <= 1 else t
        bx = (1 - u) ** 2 * x0 + 2 * (1 - u) * u * xm + u * u * x1
        by = (1 - u) ** 2 * y0 + 2 * (1 - u) * u * ym + u * u * y1
        sc = gfx.pop_scale(d)
        rot = (random.random() * 30 - 15) * u
        gfx.blend(dst, gfx.emoji(ch, px), bx, by, scale=sc, angle=rot, blur=6 if px >= 200 else 0)


def vs_background(bg, ev, f):
    """split red / yellow background with zig-zag divider + packs sliding in from sides (behind person)."""
    df = f - ev["f0"]
    dur = ev["f1"] - ev["f0"]
    e = min(1, df / 8)
    out_t = max(0, (df - (dur - 6)) / 6)
    a = min(1, df / 3) * (1 - out_t)
    # zig-zag divider x as function of y
    zz = W / 2 + 40 * np.abs(((yy[:, :1] / 120) % 2) - 1) * 2 - 40
    left = (xx < zz).astype(np.float32)[..., None]
    red = np.array([1.0, 0.23, 0.12], np.float32); yel = np.array([1.0, 0.85, 0.20], np.float32)
    panel = left * red + (1 - left) * yel
    # subtle radial shading
    panel = panel * (0.82 + 0.18 * (1 - np.clip(np.sqrt((xx / W - .5) ** 2 + (yy / H - .35) ** 2) * 1.4, 0, 1)))[..., None]
    edge = np.abs(xx - zz) < 7
    panel[edge] = 1.0
    bg[:] = bg * (1 - a) + panel * a
    sl = ease_out_back(e) if df < 8 else 1.0
    for name, side in (("chings", -1), ("slurrp", 1)):
        p = PACK_G[name]
        sc = (W * 0.36) / p.shape[1]
        x_final = W / 2 + side * W * 0.30
        x = x_final + side * W * 0.6 * (1 - sl)
        gfx.blend(bg, p, x, H * 0.47, alpha=a, scale=sc * (1 - 0.3 * out_t), angle=-side * 6)


def gradient_band(dst, y0=0.65, a=0.7):
    t = np.clip((yy[:, :1] / H - y0) / (1 - y0), 0, 1) * a
    dst[:] = dst * (1 - t[..., None]) + np.array(gfx.NAVY, np.float32) / 255 * t[..., None]


def hero_card(cd, f):
    """freeze-frame product hero card."""
    df = f - cd["f0"]
    base = still_frame(cd["freeze"])
    fr = cv2.resize(base, (W, H), interpolation=cv2.INTER_LANCZOS4)
    fr = cv2.GaussianBlur(fr, (0, 0), 14) * 0.6
    p = PACK_G[cd["pack"]]
    sc = (W * 0.72) / p.shape[1]
    bob = math.sin(df / 30 * 2 * math.pi * 0.7) * 0.03 * H * 0.3
    sway = math.sin(df / 30 * 2 * math.pi * 0.5) * 2
    ent = gfx.pop_scale(df, 8)
    # shadow
    sh = np.zeros((p.shape[0] + 80, p.shape[1] + 80, 4), np.uint8)
    sh[40:-40, 40:-40, 3] = (p[..., 3] * 0.6).astype(np.uint8)
    sh[..., :3] = gfx.NAVY
    sh = cv2.GaussianBlur(sh, (0, 0), 14)
    gfx.blend(fr, sh, W / 2 + 10, H * 0.40 + bob + 28, scale=sc * ent, angle=sway)
    gfx.blend(fr, p, W / 2, H * 0.40 + bob, scale=sc * ent, angle=sway)
    # thin border round the frame (8 px)
    c1, c2 = cd["border"]
    fr[:8, :] = c1; fr[-8:, :] = c1; fr[:, :8] = c2; fr[:, -8:] = c2
    gradient_band(fr, 0.62, 0.72)
    if cd.get("wipe_in") and df < 4:
        fr = dir_blur(fr, [60, 40, 20, 8][df])
    return fr


def watermark(dst, pos, alpha=0.6):
    g = gfx.instagram_glyph(58)
    t = gfx.plain_caption(HANDLE.upper(), 24)
    if pos == "tr":
        x, y = W * 0.88, H * 0.27
    else:
        x, y = W * 0.075, H * 0.57
    gfx.blend(dst, g, x, y, alpha=alpha)
    gfx.blend(dst, t, min(W - t.shape[1] / 2 + 10, max(t.shape[1] / 2 - 10, x)), y + 50, alpha=alpha)


# ------------------------------------------------------------------ end card
THUMB = None


def build_thumb():
    """16:9 thumbnail built from the VS card: split bg, packs, host cut-out, title."""
    tw, th = 1600, 900
    yy2, xx2 = np.mgrid[0:th, 0:tw].astype(np.float32)
    zz = tw / 2 + 60 * np.abs(((yy2[:, :1] / 150) % 2) - 1) * 2 - 60
    left = (xx2 < zz)[..., None]
    img = np.where(left, np.array([1.0, 0.23, 0.12], np.float32), np.array([1.0, 0.85, 0.2], np.float32)).astype(np.float32)
    img[np.abs(xx2 - zz) < 8] = 1
    gfx.blend(img, PACK_G["chings"], 330, 520, scale=560 / PACK["chings"].shape[1], angle=8)
    gfx.blend(img, PACK_G["slurrp"], 1270, 520, scale=420 / PACK["slurrp"].shape[1], angle=-8)
    si = int(54.8 * FPS)
    fr = still_frame(si); mk = MASKS[si]
    m = cv2.resize(mk, (SW, SH)).astype(np.float32) / 255
    face = FACES[si]
    x0, y0 = int(face[0] - 260), max(0, int(face[1] - 260))
    crop = fr[max(0, y0):y0 + 640, max(0, x0):x0 + 520]
    mc = m[max(0, y0):y0 + 640, max(0, x0):x0 + 520]
    rgba = np.dstack([crop * 255, mc * 255]).astype(np.uint8)
    gfx.blend(img, rgba, tw / 2, th - rgba.shape[0] * 1.25 / 2 + 20, scale=1.25)
    gfx.blend(img, gfx.neon_text("VS", 220, "big"), tw / 2, 190)
    gfx.blend(img, gfx.neon_text("NOODLE battle", 120, "hook"), tw / 2, th - 90)
    return (np.clip(img, 0, 1) * 255).astype(np.uint8)


def end_card(f):
    global THUMB
    if THUMB is None:
        THUMB = build_thumb()
    fr = np.ones((H, W, 3), np.float32) * (np.array([0xE0, 0x60, 0x2C], np.float32) / 255)
    for i, line in enumerate(["WATCH FULL", "VIDEO ON", "YOUTUBE"]):
        st = i * 3
        if f >= st:
            gfx.blend(fr, gfx.plain_caption(line, 110), W / 2, 300 + i * 135, scale=gfx.pop_scale(f - st))
    t0 = 9
    if f >= t0:
        tw = int(W * 0.86)
        th_ = int(tw * 9 / 16)
        tb = cv2.resize(THUMB, (tw, th_), interpolation=cv2.INTER_AREA)
        # rounded corners + shadow
        mk = np.zeros((th_, tw), np.uint8)
        cv2.rectangle(mk, (24, 0), (tw - 24, th_), 255, -1); cv2.rectangle(mk, (0, 24), (tw, th_ - 24), 255, -1)
        for cx_, cy_ in ((24, 24), (tw - 24, 24), (24, th_ - 24), (tw - 24, th_ - 24)):
            cv2.circle(mk, (cx_, cy_), 24, 255, -1, lineType=cv2.LINE_AA)
        rgba = np.dstack([tb, mk])
        sh = np.zeros((th_ + 80, tw + 80, 4), np.uint8); sh[40:-40, 40:-40, 3] = 140; sh[..., :3] = gfx.NAVY
        sh = cv2.GaussianBlur(sh, (0, 0), 16)
        d = f - t0
        sc = gfx.pop_scale(d, 8)
        gfx.blend(fr, sh, W / 2, 1000 + 14, scale=sc)
        gfx.blend(fr, rgba, W / 2, 1000, scale=sc)
    if f >= 15:
        gfx.blend(fr, gfx.youtube_button(170), W / 2, 1400, scale=gfx.pop_scale(f - 15))
    if f >= 18:
        gfx.blend(fr, gfx.plain_caption(HANDLE, 70), W / 2, 1540, scale=gfx.pop_scale(f - 18))
    t1 = 57
    if f >= t1:
        d = f - t1
        a = min(1, d / 4) * 0.75
        fr *= (1 - a)
        sc = gfx.pop_scale(d, 8)
        px = 300
        gl = gfx.instagram_glyph(px).astype(np.float32)
        u = min(1, max(0, (d - 4) / 18))  # 0.6 s white -> gradient
        grad = gfx.instagram_gradient(px).astype(np.float32)
        gl[..., :3] = gl[..., :3] * (1 - u) + grad * u
        gfx.blend(fr, gl.astype(np.uint8), W / 2, 1000, scale=sc)
        gfx.blend(fr, gfx.plain_caption(HANDLE, 74), W / 2, 1000 + 230, scale=sc)
    return fr


# ------------------------------------------------------------------ main per-frame
def active(f):
    return [e for e in EVENTS if e["f0"] <= f < e["f1"]]


def render_frame(fi, src: Source):
    p = PLAN[fi]
    if p["clip"] == -1:
        fr = end_card(p["k"])
        return finish(fr, fi, wm=None)
    c = CLIPS[p["clip"]]
    si = int(round(p["t"] * FPS))
    img = src.get(si)
    mask = MASKS[min(si, NSRC - 1)]
    k = p["k"]
    n_clip = sum(1 for q in PLAN if q["clip"] == p["clip"])
    z0, z1 = c["zoom"] if isinstance(c["zoom"], (list, tuple)) else (c["zoom"], c["zoom"] * (1.04 if n_clip > 60 else 1.02))
    if c.get("pull"):  # fast pull-out over first N frames, then slow push
        n = c["pull"][1]
        z = c["pull"][0] + (z0 - c["pull"][0]) * min(1, k / n) ** 0.5 if k < n else z0 + (z1 - z0) * (k - n) / max(1, n_clip - n)
    else:
        z = z0 + (z1 - z0) * k / max(1, n_clip - 1)
    ox = oy = 0
    for e in active(fi):
        if e["type"] == "shake":
            rs = random.Random(fi)
            ox, oy = rs.uniform(-6, 6), rs.uniform(-6, 6)
    box = crop_box(si, z, c.get("focus", "face"))
    fr, mk = render_cam(img, mask, box, ox, oy)
    # fake shallow depth of field on MID/CLOSE
    if z >= 1.25 and not c.get("no_dof"):
        bl = cv2.GaussianBlur(fr, (0, 0), 7 if z < 1.5 else 9)
        mk_s = cv2.GaussianBlur(mk, (0, 0), 3)[..., None]
        fr = fr * mk_s + bl * (1 - mk_s)
    fr = bloom(fr)
    person = fr.copy()
    mk3 = cv2.GaussianBlur(mk, (0, 0), 1.5)[..., None]
    # face position in output space (for graphics placement)
    fx, fy, fw, fh = FACES[min(si, NSRC - 1)]
    x0, y0, cw, ch = box
    head = ((fx - x0) * W / cw, (fy - y0) * H / ch, fw * W / cw)
    behind = False
    acts = active(fi)
    for e in acts:
        if e["type"] == "vs":
            vs_background(fr, e, fi); behind = True
    for e in acts:
        if e["type"] == "meter":
            meter_layer(fr, e, fi); behind = True
        if e["type"] == "qmarks":
            e["_head"] = (head[0], head[1] - head[2] * 0.2)
            qmarks(fr, e, fi, "back"); behind = True
    if behind:
        fr = fr * (1 - mk3) + person * mk3
    # zoom blur on punch-in entries (first 4 frames of clips flagged punch)
    if c.get("punch") and k < 4:
        fr = zoom_blur(fr, [0.10, 0.07, 0.04, 0.02][k], head[0], head[1])
    if c.get("wipe_in") and k < 4:
        fr = dir_blur(fr, [60, 40, 20, 8][k])
    if c.get("wipe_out"):
        kk = n_clip - 1 - k
        if kk < 4:
            fr = dir_blur(fr, [60, 40, 20, 8][kk])
    # B&W mood shift
    for e in acts:
        if e["type"] == "bw":
            d = (fi - e["f0"]) / 30
            amt = min(1, d / 1.0)
            fr = desat(fr, amt)
            fr = fr * (VIGNETTE + (VIG_BW - VIGNETTE) * amt)
            # slow 100->105 push-in on the B&W hold
            s = 1 + 0.05 * min(1, (fi - e["f0"]) / max(1, e["f1"] - e["f0"]))
            Mx = cv2.getRotationMatrix2D((W / 2, H * 0.38), 0, s)
            fr = cv2.warpAffine(fr, Mx, (W, H), borderMode=cv2.BORDER_REFLECT)
    # hero cards replace the picture
    for cd in CARDS:
        if cd["f0"] <= fi < cd["f1"]:
            fr = hero_card(cd, fi)
    # dip dissolve
    for e in acts:
        if e["type"] == "dip":
            d = fi - e["f0"]
            dark = desat(fr, 0.7) * 0.45
            if d < 6:
                fr = fr * (1 - d / 6) + dark * (d / 6)
            else:
                u = min(1, (d - 6) / max(1, e["f1"] - e["f0"] - 6))
                fr = dark * (1 - 0.88 * u)
    # transitions (video layer)
    flash_on = False
    for e in acts:
        d = fi - e["f0"]
        if e["type"] == "leak":
            fr = light_leak(fr, d)
        elif e["type"] == "redflash":
            fr = red_flash(fr, d); flash_on = d < 2
        elif e["type"] == "whiteflash":
            fr = white_flash(fr, d)
    # front graphics
    for e in acts:
        t = e["type"]
        if t == "title":
            draw_title(fr, e, fi)
        elif t == "build":
            draw_build(fr, e, fi, color_override=e.get("flash_style") if flash_on else None)
        elif t == "burst":
            burst(fr, e, fi)
        elif t == "qmarks":
            qmarks(fr, e, fi, "front")
        elif t == "sticker":
            d = fi - e["f0"]
            gfx.blend(fr, e["_img"], e["x"] * W, e["y"] * H, scale=gfx.pop_scale(d), angle=e.get("angle", 0))
        elif t == "scorecard":
            scorecard(fr, e, fi)
        elif t == "sparkle":
            sparkle(fr, e, fi)
    wm = c.get("wm", "tr")
    if any(cd["f0"] <= fi < cd["f1"] for cd in CARDS):
        wm = "tr"
    return finish(fr, fi, wm)


def scorecard(dst, e, f):
    for row in e["rows"]:
        if f < row["f"]:
            continue
        d = f - row["f"]
        gfx.blend(dst, row["_img"], row["x"] * W, row["y"] * H, scale=gfx.pop_scale(d))


def sparkle(dst, e, f):
    d = f - e["f0"]
    random.seed(3)
    for i in range(14):
        st = random.randint(0, 12)
        if d < st:
            continue
        u = (d - st) / 10
        if u > 1:
            continue
        x = (e["x0"] + (e["x1"] - e["x0"]) * (i / 13)) * W + random.uniform(-30, 30)
        y = e["y"] * H + random.uniform(-90, 90)
        s = math.sin(math.pi * u)
        gfx.blend(dst, gfx.emoji("✨", 70), x, y, alpha=s, scale=0.6 + 0.6 * s)


def finish(fr, fi, wm):
    if wm:
        watermark(fr, wm)
    if PLAN[fi]["clip"] != -1:
        fr = fr * VIGNETTE
    g = GRAIN[fi % len(GRAIN)]
    g = cv2.resize(g, (W, H), interpolation=cv2.INTER_LINEAR)[..., None]
    fr = np.clip(fr + g, 0, 1)
    return (fr * 255 + 0.5).astype(np.uint8)


def prep_events():
    for e in EVENTS:
        if e["type"] == "sticker":
            e["_img"] = gfx.pill(e["text"], e.get("size", 56), e["bg"], fg=e.get("fg", (255, 255, 255)), emoji_ch=e.get("emoji"))
        if e["type"] == "scorecard":
            for row in e["rows"]:
                row["f"] = src_to_out(row["t"])
                row["_img"] = gfx.pill(row["text"], row.get("size", 46), row["bg"], fg=row.get("fg", (255, 255, 255)), emoji_ch=row.get("emoji"))


prep_events()

if __name__ == "__main__":
    if sys.argv[1] == "plan":
        json.dump({"n_main": N_MAIN, "plan": PLAN,
                   "events": [{k: v for k, v in e.items() if not k.startswith("_")} for e in EVENTS],
                   "cards": CARDS}, open(f"{WORK}/plan.json", "w"), default=str)
        print("frames", len(PLAN), "main", N_MAIN, "sec", len(PLAN) / FPS)
    elif sys.argv[1] == "still":
        for a in sys.argv[2:]:
            fi = int(a)
            p = PLAN[fi]
            si = int(round(p["t"] * FPS)) if p["t"] is not None else 0
            src = Source(si)
            # warm up sequential state for the frame
            out = render_frame(fi, src)
            cv2.imwrite(f"{WORK}/still_{fi}.jpg", cv2.cvtColor(out, cv2.COLOR_RGB2BGR), [cv2.IMWRITE_JPEG_QUALITY, 88])
            src.p.kill()
    else:
        wi, nw = int(sys.argv[1]), int(sys.argv[2])
        N = len(PLAN)
        a, b = N * wi // nw, N * (wi + 1) // nw
        first_src = next((int(round(PLAN[i]["t"] * FPS)) for i in range(a, b) if PLAN[i]["t"] is not None), 0)
        src = Source(first_src)
        enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                                "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "10", "-pix_fmt", "yuv420p",
                                f"{WORK}/part_{wi}.mkv"], stdin=subprocess.PIPE)
        for fi in range(a, b):
            enc.stdin.write(render_frame(fi, src).tobytes())
            if (fi - a) % 30 == 0:
                print(f"w{wi} {fi - a}/{b - a}", flush=True)
        enc.stdin.close(); enc.wait(); src.p.kill()
        print(f"w{wi} done")
