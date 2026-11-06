"""Graphics primitives for the noodle-battle reel. Everything returns RGBA uint8 numpy arrays (premultiplied NOT)."""
import numpy as np, cv2, math, functools
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops

M = "/tmp/claude-0/-home-user-Testclaude/f29330e6-8f24-5182-bfb1-c06071f78d9b/scratchpad/models"
FONT_BUBBLE = f"{M}/BubblegumSans-Regular.ttf.ttf"
FONT_SNIGLET = f"{M}/Sniglet-ExtraBold.ttf.ttf"
FONT_EMOJI = "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf"

NAVY = (27, 26, 58)
PAL = {
    "hook":     ((255, 194, 26), (255, 106, 0)),
    "chings":   ((255, 75, 43), (184, 0, 0)),
    "slurrp":   ((201, 245, 90), (31, 168, 74)),
    "reaction": ((255, 225, 198), (224, 86, 42)),
    "big":      ((255, 47, 208), (255, 122, 230)),
    "maggi":    ((255, 214, 0), (230, 30, 30)),
    "white":    ((255, 255, 255), None),
}


def hexrgb(h):
    h = h.lstrip("#"); return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def _font(path, size):
    return ImageFont.truetype(path, size)


@functools.lru_cache(maxsize=512)
def neon_text(text, size=130, style="hook", font=FONT_BUBBLE, glow_r=25, outline=3):
    """Chunky bubble neon title: drop shadow + wide glow + navy outline + fill + top inner highlight."""
    fill, glow = PAL[style]
    f = _font(font, size)
    pad = int(glow_r * 2.2 + 20)
    l, t, r, b = f.getbbox(text, stroke_width=outline)
    w, h = r - l + pad * 2, b - t + pad * 2
    org = (pad - l, pad - t)

    def mask(stroke=0, off=(0, 0)):
        im = Image.new("L", (w, h), 0)
        ImageDraw.Draw(im).text((org[0] + off[0], org[1] + off[1]), text, font=f, fill=255,
                                stroke_width=stroke, stroke_fill=255)
        return im

    core = mask()
    outl = mask(outline)
    out = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    # soft drop shadow (navy, 6px down, 18px blur, 45 %)
    sh = mask(outline, (0, 6)).filter(ImageFilter.GaussianBlur(18 / 2))
    out.alpha_composite(Image.merge("RGBA", [Image.new("L", (w, h), c) for c in NAVY] + [sh.point(lambda v: int(v * .45))]))
    if glow is not None:
        g = mask(outline + 4).filter(ImageFilter.GaussianBlur(glow_r / 2))
        g = g.point(lambda v: min(255, int(v * 1.6 * .8)))
        out.alpha_composite(Image.merge("RGBA", [Image.new("L", (w, h), c) for c in glow] + [g]))
        # tight inner glow ring for neon punch
        g2 = mask(outline + 1).filter(ImageFilter.GaussianBlur(4))
        out.alpha_composite(Image.merge("RGBA", [Image.new("L", (w, h), c) for c in glow] + [g2.point(lambda v: int(v * .9))]))
    # navy outline 85 %
    out.alpha_composite(Image.merge("RGBA", [Image.new("L", (w, h), c) for c in NAVY] + [outl.point(lambda v: int(v * .85))]))
    # fill
    out.alpha_composite(Image.merge("RGBA", [Image.new("L", (w, h), c) for c in fill] + [core]))
    # inner highlight: top edge, 2px lighter, 40 %
    hl = ImageChops.subtract(core, mask(0, (0, 3)))
    lite = tuple(min(255, int(c + (255 - c) * .7)) for c in fill)
    out.alpha_composite(Image.merge("RGBA", [Image.new("L", (w, h), c) for c in lite] + [hl.point(lambda v: int(v * .4))]))
    return np.array(out)


@functools.lru_cache(maxsize=256)
def plain_caption(text, size=58):
    """Secondary white caption, navy soft shadow, no glow."""
    f = _font(FONT_BUBBLE, size)
    pad = 30
    l, t, r, b = f.getbbox(text, stroke_width=2)
    w, h = r - l + pad * 2, b - t + pad * 2
    org = (pad - l, pad - t)
    sh = Image.new("L", (w, h), 0)
    ImageDraw.Draw(sh).text((org[0], org[1] + 4), text, font=f, fill=255, stroke_width=3, stroke_fill=255)
    sh = sh.filter(ImageFilter.GaussianBlur(6)).point(lambda v: int(v * .6))
    out = Image.merge("RGBA", [Image.new("L", (w, h), c) for c in NAVY] + [sh])
    ImageDraw.Draw(out).text(org, text, font=f, fill=(255, 255, 255, 255), stroke_width=2, stroke_fill=(*NAVY, 200))
    return np.array(out)


@functools.lru_cache(maxsize=64)
def emoji(ch, px=160):
    f = ImageFont.truetype(FONT_EMOJI, 109)
    im = Image.new("RGBA", (160, 160), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((80, 80), ch, font=f, embedded_color=True, anchor="mm")
    bb = im.getbbox(); im = im.crop(bb)
    s = px / max(im.size)
    im = im.resize((max(1, int(im.width * s)), max(1, int(im.height * s))), Image.LANCZOS)
    return np.array(im)


@functools.lru_cache(maxsize=16)
def question_mark(px=260):
    """Glossy white extruded 3D '?' with soft shadow."""
    S = 2
    size = px * S
    f = _font(FONT_BUBBLE, int(size * 0.95))
    W = H = int(size * 1.4)
    def m(off=(0, 0)):
        im = Image.new("L", (W, H), 0)
        ImageDraw.Draw(im).text((W // 2 + off[0], H // 2 + off[1]), "?", font=f, fill=255, anchor="mm")
        return im
    out = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sh = m((int(14 * S), int(22 * S))).filter(ImageFilter.GaussianBlur(14 * S))
    out.alpha_composite(Image.merge("RGBA", [Image.new("L", (W, H), c) for c in (40, 40, 60)] + [sh.point(lambda v: int(v * .45))]))
    depth = int(16 * S)
    for d in range(depth, 0, -1):  # extrusion, darker further back
        shade = int(150 + 70 * (1 - d / depth))
        out.alpha_composite(Image.merge("RGBA", [Image.new("L", (W, H), c) for c in (shade, shade, shade + 8)] + [m((d // 2, d))]))
    face = m()
    # vertical gradient face: white top -> light grey bottom
    grad = Image.linear_gradient("L").resize((W, H)).point(lambda v: 255 - int(v * .22))
    out.alpha_composite(Image.merge("RGBA", [grad, grad, grad.point(lambda v: min(255, v + 6))] + [face]))
    # specular highlight along top-left
    hl = ImageChops.subtract(face, m((int(6 * S), int(8 * S)))).filter(ImageFilter.GaussianBlur(2 * S))
    out.alpha_composite(Image.merge("RGBA", [Image.new("L", (W, H), 255)] * 3 + [hl]))
    out = out.crop(out.getbbox())
    out = out.resize((out.width // S, out.height // S), Image.LANCZOS)
    return np.array(out)


@functools.lru_cache(maxsize=4)
def spice_meter(width=980):
    """Glossy semicircular gauge without needle. Returns (rgba, pivot_xy, radius)."""
    S = 2
    W = width * S
    R = int(W * 0.46)
    H = int(R * 1.32)
    cx, cy = W // 2, int(R * 1.08)
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    # drop shadow
    sh = Image.new("L", (W, H), 0)
    ImageDraw.Draw(sh).pieslice([cx - R, cy - R + 24 * S, cx + R, cy + R + 24 * S], 180, 360, fill=150)
    ImageDraw.Draw(sh).rounded_rectangle([cx - R, cy - 10 * S + 24 * S, cx + R, cy + 70 * S + 24 * S], 40 * S, fill=150)
    sh = sh.filter(ImageFilter.GaussianBlur(20 * S))
    im.alpha_composite(Image.merge("RGBA", [Image.new("L", (W, H), c) for c in NAVY] + [sh]))
    # silver rim: concentric rings of varying grey
    for i in range(18 * S, 0, -1):
        v = int(150 + 100 * math.sin(i / (18 * S) * math.pi))
        rr = R - (18 * S - i)
        d.pieslice([cx - rr, cy - rr, cx + rr, cy + rr], 180, 360, fill=(v, v, v + 6, 255))
    d.rounded_rectangle([cx - R, cy - 12 * S, cx + R, cy + 70 * S], 36 * S, fill=(205, 205, 212, 255))
    d.rounded_rectangle([cx - R + 12 * S, cy - 6 * S, cx + R - 12 * S, cy + 58 * S], 28 * S, fill=(246, 239, 227, 255))
    r2 = R - 18 * S
    d.pieslice([cx - r2, cy - r2, cx + r2, cy + r2], 180, 360, fill=(246, 239, 227, 255))
    # gradient arc green->yellow->orange->red
    stops = [(0, (46, 190, 80)), (.38, (255, 214, 30)), (.68, (255, 120, 20)), (1, (230, 25, 25))]
    def col(t):
        for (a, ca), (b, cb) in zip(stops, stops[1:]):
            if t <= b:
                u = (t - a) / (b - a); return tuple(int(ca[k] + (cb[k] - ca[k]) * u) for k in range(3))
        return stops[-1][1]
    ra, rb = r2 - 20 * S, r2 - 95 * S
    for k in range(180):
        t = k / 179
        a0, a1 = 180 + k, min(360, 180 + k + 1.5)
        d.pieslice([cx - ra, cy - ra, cx + ra, cy + ra], a0, a1, fill=(*col(t), 255))
    d.pieslice([cx - rb, cy - rb, cx + rb, cy + rb], 180, 360, fill=(246, 239, 227, 255))
    # ticks
    for k in range(0, 41):
        ang = math.radians(180 + k * 4.5)
        big = k % 5 == 0
        r_out, r_in = rb - 8 * S, rb - (40 if big else 22) * S
        d.line([cx + r_out * math.cos(ang), cy + r_out * math.sin(ang), cx + r_in * math.cos(ang), cy + r_in * math.sin(ang)],
               fill=(*NAVY, 255), width=(7 if big else 3) * S)
    # gloss: white ellipse highlight on upper half
    gl = Image.new("L", (W, H), 0)
    ImageDraw.Draw(gl).ellipse([cx - R * .85, cy - R * 1.02, cx + R * .85, cy - R * .25], fill=70)
    gl = gl.filter(ImageFilter.GaussianBlur(30 * S))
    im.alpha_composite(Image.merge("RGBA", [Image.new("L", (W, H), 255)] * 3 + [ImageChops.multiply(gl, im.getchannel("A"))]))
    # label
    lab = Image.fromarray(neon_text("teekha-meter", 64 * S // 2 * 2, "chings", glow_r=10))
    lab = lab.resize((lab.width * S // 2 * 2 // 2, lab.height * S // 2 * 2 // 2))
    im.alpha_composite(lab, (cx - lab.width // 2, int(cy - rb * .55 - lab.height // 2)))
    # emoji end caps
    for ch, ang in (("🙂", 192), ("🥵", 348)):
        e = Image.fromarray(emoji(ch, 70 * S))
        rr = ra + 55 * S
        a = math.radians(ang)
        im.alpha_composite(e, (int(cx + rr * math.cos(a) - e.width / 2), int(cy + rr * math.sin(a) - e.height / 2)))
    im = im.resize((W // S, H // S), Image.LANCZOS)
    return np.array(im), (cx // S, cy // S), R // S


@functools.lru_cache(maxsize=2)
def needle(length=380):
    S = 2
    L = length * S
    w = 44 * S
    im = Image.new("RGBA", (L * 2, L * 2), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    c = L
    d.polygon([(c, c - 12 * S), (c + L - 10 * S, c), (c, c + 12 * S), (c - 50 * S, c)], fill=(220, 30, 30, 255))
    d.polygon([(c, c - 12 * S), (c + L - 10 * S, c), (c, c)], fill=(255, 90, 80, 255))
    d.ellipse([c - w // 2, c - w // 2, c + w // 2, c + w // 2], fill=(60, 60, 70, 255))
    d.ellipse([c - w // 4, c - w // 4, c + w // 4, c + w // 4], fill=(200, 200, 210, 255))
    im = im.resize((L, L), Image.LANCZOS)
    return np.array(im)  # pivot at centre, pointing +x (0 deg)


def pill(text, size, bg, fg=(255, 255, 255), font=FONT_BUBBLE, pad=(34, 14), emoji_ch=None):
    f = _font(font, size)
    l, t, r, b = f.getbbox(text)
    ew = 0
    e = None
    if emoji_ch:
        e = Image.fromarray(emoji(emoji_ch, int(size * 1.1))); ew = e.width + 12
    w, h = r - l + pad[0] * 2 + ew, b - t + pad[1] * 2
    m = 24
    im = Image.new("RGBA", (w + m * 2, h + m * 2), (0, 0, 0, 0))
    sh = Image.new("L", im.size, 0)
    ImageDraw.Draw(sh).rounded_rectangle([m, m + 8, m + w, m + h + 8], h // 2, fill=120)
    im.alpha_composite(Image.merge("RGBA", [Image.new("L", im.size, c) for c in NAVY] + [sh.filter(ImageFilter.GaussianBlur(8))]))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([m, m, m + w, m + h], h // 2, fill=(*bg, 255), outline=(255, 255, 255, 255), width=5)
    d.text((m + pad[0] - l, m + pad[1] - t), text, font=f, fill=(*fg, 255))
    if e is not None:
        im.alpha_composite(e, (m + w - pad[0] - e.width + 6, m + (h - e.height) // 2))
    return np.array(im)


def instagram_glyph(px=64, color=(255, 255, 255), stroke=None):
    S = 4
    W = px * S
    st = stroke or max(2, int(W * .085))
    im = Image.new("L", (W, W), 0)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([st // 2, st // 2, W - st // 2, W - st // 2], int(W * .28), outline=255, width=st)
    r = W * .22
    d.ellipse([W / 2 - r, W / 2 - r, W / 2 + r, W / 2 + r], outline=255, width=st)
    rd = W * .055
    d.ellipse([W * .75 - rd, W * .25 - rd, W * .75 + rd, W * .25 + rd], fill=255)
    im = im.resize((px, px), Image.LANCZOS)
    out = Image.merge("RGBA", [Image.new("L", (px, px), c) for c in color] + [im])
    return np.array(out)


def instagram_gradient(px):
    """Instagram-style radial gradient square (yellow/orange/pink/purple)."""
    y, x = np.mgrid[0:px, 0:px].astype(np.float32) / px
    t = np.clip(np.sqrt((x - 0.2) ** 2 + (y - 1.05) ** 2) / 1.25, 0, 1)
    stops = np.array([[254, 218, 117], [250, 126, 30], [214, 41, 118], [150, 47, 191], [79, 91, 213]], np.float32)
    pos = np.linspace(0, 1, len(stops))
    rgb = np.stack([np.interp(t, pos, stops[:, k]) for k in range(3)], -1)
    return rgb.astype(np.uint8)


def youtube_button(w=220):
    S = 3
    W, H = w * S, int(w * .7) * S
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, W - 1, H - 1], int(H * .3), fill=(255, 0, 0, 255))
    cx, cy, s = W / 2, H / 2, H * .22
    d.polygon([(cx - s * .8, cy - s), (cx - s * .8, cy + s), (cx + s * 1.1, cy)], fill=(255, 255, 255, 255))
    return np.array(im.resize((w, int(w * .7)), Image.LANCZOS))


# ---------------------------------------------------------------- compositing helpers
def blend(dst, src, x, y, alpha=1.0, scale=1.0, angle=0.0, blur=0):
    """Alpha-composite RGBA src (uint8) onto float32 RGB dst (0..1) centred at (x, y)."""
    if alpha <= 0.003:
        return
    s = src
    if scale != 1.0 or angle != 0.0:
        h, w = s.shape[:2]
        if angle:
            diag = int(math.hypot(w, h) * scale) + 4
            Mx = cv2.getRotationMatrix2D((w / 2, h / 2), angle, scale)
            Mx[0, 2] += diag / 2 - w / 2; Mx[1, 2] += diag / 2 - h / 2
            s = cv2.warpAffine(s, Mx, (diag, diag), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0, 0))
        else:
            nw, nh = max(1, int(round(w * scale))), max(1, int(round(h * scale)))
            s = cv2.resize(s, (nw, nh), interpolation=cv2.INTER_AREA if scale < 1 else cv2.INTER_LINEAR)
    if blur > 0:
        k = int(blur) * 2 + 1
        s = cv2.GaussianBlur(s, (k, k), 0)
    h, w = s.shape[:2]
    x0, y0 = int(round(x - w / 2)), int(round(y - h / 2))
    H, W = dst.shape[:2]
    ax0, ay0, ax1, ay1 = max(0, x0), max(0, y0), min(W, x0 + w), min(H, y0 + h)
    if ax0 >= ax1 or ay0 >= ay1:
        return
    sub = s[ay0 - y0:ay1 - y0, ax0 - x0:ax1 - x0].astype(np.float32) / 255.0
    a = sub[..., 3:4] * alpha
    dst[ay0:ay1, ax0:ax1] = dst[ay0:ay1, ax0:ax1] * (1 - a) + sub[..., :3] * a


def pop_scale(f, dur=6):
    """120 % -> 95 % -> 100 % over `dur` frames, ease-out. f = frames since entrance."""
    if f < 0:
        return 0.0
    if f >= dur:
        return 1.0
    t = f / dur
    if t < .5:
        u = t / .5; u = 1 - (1 - u) ** 2
        return 1.2 + (0.95 - 1.2) * u
    u = (t - .5) / .5; u = 1 - (1 - u) ** 2
    return 0.95 + 0.05 * u


def glow_flicker(f):
    return {2: .55, 3: .4, 4: .75}.get(f, 1.0)
