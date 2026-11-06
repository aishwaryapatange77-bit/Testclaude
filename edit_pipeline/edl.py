"""Edit decision list for the noodle-battle reel (all times = SOURCE seconds)."""
import re, numpy as np, soundfile as sf

SRC = "/root/.claude/uploads/f29330e6-8f24-5182-bfb1-c06071f78d9b/5bdd2bd1-1793957200047430.mov"
FPS = 30
HANDLE = "@yourhandle"
ENDCARD_SEC = 6.4

WIDE, MID, CLOSE = 1.0, 1.32, 1.6

# ------------------------------------------------------------------ word timing from voiced energy
_x, _sr = sf.read("/tmp/claude-0/-home-user-Testclaude/f29330e6-8f24-5182-bfb1-c06071f78d9b/scratchpad/a2.wav", dtype="float32")
_hop = int(_sr * 0.01)
_rms = np.sqrt(np.convolve(_x ** 2, np.ones(_hop * 3) / (_hop * 3), "same")[::_hop])
_db = 20 * np.log10(_rms + 1e-6)


def _syl(w):
    return max(1, len(re.findall(r"[aeiouy]+", w.lower())))


def words(text, t0, t1, style=None, line_breaks=()):
    """distribute words over the voiced part of [t0, t1] proportional to syllables.
    `|` in text forces a line break. Words wrapped in *stars* get style override (neon emphasis)."""
    toks = text.split()
    seg = _db[int(t0 * 100):int(t1 * 100)]
    voiced = (seg > np.percentile(seg, 35)).astype(float)
    cum = np.cumsum(voiced); cum /= max(cum[-1], 1)
    out, line = [], 0
    ws = [t for t in toks if t != "|"]
    weights = np.array([_syl(t) for t in ws], float)
    starts = np.concatenate([[0], np.cumsum(weights)[:-1]]) / weights.sum()
    i = 0
    for t in toks:
        if t == "|":
            line += 1; continue
        idx = int(np.searchsorted(cum, starts[i] + 1e-6))
        tt = t0 + idx / 100.0
        w = {"w": t.strip("*"), "t": round(tt, 3), "line": line}
        if t.startswith("*") and style:
            w["style"] = style
        out.append(w)
        i += 1
    return out


# ------------------------------------------------------------------ clips
# zoom: number (auto slow push 100->104 %) or (z_start, z_end). punch: zoom-blur entry. wm: watermark position.
CLIPS = [
    # SECTION 1 — HOOK
    dict(src=(0.00, 1.00), zoom=(1.20, 1.22), pull=(1.30, 10)),
    dict(src=(1.00, 3.56), zoom=(1.55, 1.60), punch=True),
    dict(src=(3.92, 5.67), zoom=WIDE),
    # SECTION 2 — EATING CHING'S
    dict(src=(5.80, 7.30), zoom=1.62, punch=True, focus=("face+", 0, 60)),
    dict(src=(8.30, 10.01), zoom=1.35),
    dict(src=(10.01, 10.72), zoom=WIDE),
    dict(src=(11.18, 11.52), zoom=1.58, punch=True),
    dict(src=(11.70, 12.75), zoom=1.35),
    dict(src=(13.03, 14.45), zoom=WIDE),
    dict(src=(14.78, 15.76), zoom=1.55, punch=True),
    dict(src=(15.90, 17.10), zoom=1.62, punch=True, focus=("face+", 0, 40)),
    dict(src=(17.57, 18.62), zoom=WIDE),
    # SECTION 3 — SLURRP INTRO
    dict(src=(19.06, 20.01), zoom=1.30, wipe_out=True),
    dict(src=(20.30, 22.25), zoom=WIDE),             # hero card B covers most of this
    dict(src=(22.25, 23.20), zoom=WIDE),
    dict(src=(23.20, 25.60), zoom=1.30, wipe_out=True),
    # SECTION 4 — EATING SLURRP
    dict(src=(25.90, 27.40), zoom=1.60, punch=True, wipe_in=True, focus=("face+", 0, 50)),
    dict(src=(27.70, 28.93), zoom=1.32),
    dict(src=(29.58, 30.80), zoom=WIDE),
    dict(src=(30.80, 31.99), zoom=1.55, punch=True),
    dict(src=(32.76, 33.80), zoom=1.32),
    dict(src=(33.80, 34.88), zoom=1.55),
    dict(src=(35.15, 36.32), zoom=1.62, punch=True, focus=("face+", 0, 230), ramp=(35.35, 35.95, 0.5)),
    dict(src=(36.32, 37.39), zoom=WIDE),
    dict(src=(37.78, 38.53), zoom=1.38),
    dict(src=(38.53, 39.90), zoom=1.58, punch=True),
    dict(src=(39.90, 41.25), zoom=WIDE),
    dict(src=(41.61, 42.21), zoom=1.32),
    dict(src=(42.55, 43.72), zoom=1.62, punch=True, focus=("face+", 0, 170), ramp=(42.75, 43.35, 0.5)),
    dict(src=(43.72, 45.20), zoom=WIDE),
    dict(src=(45.20, 46.75), zoom=1.38),
    # SECTION 5 — THE GOOD BITE + COMPARISON
    dict(src=(47.45, 48.70), zoom=1.65, punch=True, focus=("face+", 0, 60), ramp=(47.7, 48.4, 0.5)),
    dict(src=(48.70, 50.00), zoom=WIDE),
    dict(src=(51.42, 51.99), zoom=1.32),
    dict(src=(52.94, 53.99), zoom=1.58, punch=True),
    dict(src=(54.42, 55.50), zoom=WIDE),
    dict(src=(55.50, 56.49), zoom=1.38),
    dict(src=(57.03, 59.83), zoom=(1.12, 1.17)),     # VS background
    dict(src=(60.48, 61.60), zoom=1.65, punch=True),
    dict(src=(61.60, 63.17), zoom=WIDE),
    dict(src=(63.54, 65.59), zoom=1.35),
    dict(src=(66.14, 68.00), zoom=WIDE),
    dict(src=(68.00, 69.96), zoom=1.50, punch=True),
    # SECTION 6 — VERDICT
    dict(src=(69.96, 70.46), zoom=1.60),
    dict(src=(70.46, 71.55), zoom=1.45, punch=True),
    dict(src=(71.55, 72.70), zoom=1.68, punch=True),
]

CARDS = [
    dict(pack="chings", freeze=int(3.9 * FPS), t0=4.12, t1=5.60, border=((1.0, 0.23, 0.12), (1.0, 1.0, 1.0))),
    dict(pack="slurrp", freeze=int(24.2 * FPS), t0=20.30, t1=22.20, border=((1.0, 0.88, 0.23), (0.91, 0.14, 0.23)), wipe_in=True),
]

EVENTS = [
    # ---------------- SECTION 1 — HOOK
    dict(type="title", text="NOODLE battle", style="hook", y=0.15, t0=0.10, t1=3.56, size=150),
    dict(type="meter", t0=1.40, t1=3.50, y=0.30, needle=[(0, 0.0), (10, 0.12), (40, 0.25), (60, 0.3)]),
    dict(type="build", style="white", size=62, y=0.77, t0=0.25, t1=3.56,
         words=words("NEXT up: CHING'S | Schezwan instant noodles", 0.25, 3.50)),
    dict(type="leak", t0=3.92, t1=4.33),
    dict(type="build", style="chings", size=120, y=0.75, t0=4.20, t1=5.62, flash_style="reaction",
         words=[{"w": "CHING'S", "t": 4.25, "line": 0}, {"w": "Schezwan", "t": 4.55, "line": 1}]),
    dict(type="redflash", t0=5.50, t1=5.64),
    # ---------------- SECTION 2 — EATING CHING'S
    dict(type="meter", t0=8.30, t1=10.01, y=0.27, needle=[(0, 0.3), (8, 1.0)], wobble_at=8),
    dict(type="redflash", t0=8.66, t1=8.73),
    dict(type="shake", t0=8.66, t1=8.95),
    dict(type="burst", t0=8.60, t1=10.01, emoji=["🔥", "🌶️"], n=8, seed=4),
    dict(type="title", text="SPICY!!", style="chings", y=0.55, t0=8.70, t1=10.01, size=170),
    dict(type="qmarks", t0=11.72, t1=12.75, marks=[(-260, -60, 170, 1), (230, -120, 210, 1), (-170, -260, 130, 0), (300, 80, 250, 0), (40, -330, 150, 1)]),
    dict(type="bw", t0=13.08, t1=15.76),
    dict(type="build", style="reaction", size=104, y=0.74, t0=13.08, t1=14.45,
         words=words("I don't like | *SPICY* food", 13.04, 14.40, style="chings")),
    dict(type="build", style="white", size=62, y=0.77, t0=14.80, t1=15.76,
         words=words("I'd rather eat something else", 14.81, 15.74)),
    dict(type="burst", t0=15.95, t1=17.10, emoji=["🥵"], n=4, seed=9, travel=34),
    dict(type="leak", t0=18.42, t1=19.30),
    # ---------------- SECTION 3 — SLURRP INTRO
    dict(type="title", text="LAST one", style="hook", y=0.15, t0=19.08, t1=20.01, size=160),
    dict(type="title", text="SLURRP farm", style="slurrp", y=0.13, t0=20.32, t1=22.20, typewriter=True, size=140),
    dict(type="build", style="slurrp", size=112, y=0.74, t0=20.40, t1=22.20, flash_style="chings",
         words=[{"w": "MILLET", "t": 20.55, "line": 0}, {"w": "HAKKA", "t": 20.80, "line": 1}, {"w": "Noodles", "t": 21.05, "line": 1}]),
    dict(type="redflash", t0=22.08, t1=22.22),
    dict(type="sticker", text="NO maida", bg=(232, 35, 58), x=0.72, y=0.22, t0=22.95, t1=25.20, angle=8, size=66),
    dict(type="sticker", text="NOT fried", bg=(31, 168, 74), x=0.30, y=0.29, t0=23.70, t1=25.20, angle=-6, size=66),
    dict(type="build", style="white", size=62, y=0.77, t0=22.90, t1=25.20,
         words=words("No maida, not fried... let's try it!", 22.95, 25.55)),
    # ---------------- SECTION 4 — EATING SLURRP
    dict(type="meter", t0=25.95, t1=27.30, y=0.28, needle=[(0, 0.0), (10, 0.42)], wobble_at=10),
    dict(type="title", text="MAGGI?", text2="NOT maggi", morph_t=28.15, style="big", y=0.62, t0=27.72, t1=28.93, size=150),
    dict(type="build", style="white", size=62, y=0.77, t0=29.60, t1=31.99,
         words=words("You can have it as a *HEALTH* option", 29.60, 31.95, style="slurrp")),
    dict(type="scorecard", t0=30.40, t1=34.88, rows=[
        dict(text="SLURRP  health option", emoji="✅", bg=(31, 168, 74), x=0.40, y=0.14, t=30.45, size=46),
        dict(text="SLURRP  Maggi-type taste", emoji="❌", bg=(232, 35, 58), x=0.43, y=0.20, t=33.40, size=46)]),
    dict(type="bw", t0=32.80, t1=34.88),
    dict(type="build", style="reaction", size=96, y=0.74, t0=32.80, t1=34.88,
         words=words("but NOT | Maggi-type noodles", 32.80, 34.85)),
    dict(type="qmarks", t0=37.80, t1=38.53, marks=[(-250, -80, 160, 1), (240, -140, 220, 1), (-160, -280, 130, 0), (290, 60, 250, 0), (20, -340, 140, 1), (-330, 120, 180, 0)]),
    dict(type="build", style="white", size=62, y=0.77, t0=41.61, t1=42.21, words=words("So let's see...", 41.61, 42.20)),
    # ---------------- SECTION 5 — GOOD BITE + COMPARISON
    dict(type="burst", t0=48.75, t1=50.0, emoji=["🍜", "😋"], n=6, seed=12),
    dict(type="build", style="maggi", size=140, y=0.66, t0=52.96, t1=53.99,
         words=words("MAGGI is | MAGGI", 52.96, 53.95)),
    dict(type="vs", t0=57.03, t1=59.83),
    dict(type="title", text="VS", style="big", y=0.12, t0=57.10, t1=59.75, size=230),
    dict(type="shake", t0=57.10, t1=57.37),
    dict(type="build", style="white", size=62, y=0.80, t0=57.05, t1=59.83,
         words=words("Only *MAGGI* wins this competition", 57.05, 59.80, style="maggi")),
    dict(type="build", style="white", size=62, y=0.77, t0=63.56, t1=65.59,
         words=words("I liked the *RAMEN* too...", 63.56, 65.55, style="reaction")),
    dict(type="build", style="reaction", size=100, y=0.73, t0=66.16, t1=69.96,
         words=words("but NO comparison | with *MAGGI*", 66.16, 68.40, style="maggi")),
    # ---------------- SECTION 6 — VERDICT
    dict(type="dip", t0=69.96, t1=70.46),
    dict(type="build", style="big", size=120, y=0.70, t0=70.46, t1=72.70, fade=False,
         words=words("Our WINNER | is only MAGGI", 70.50, 71.95)),
    dict(type="title", text="MAGGI", style="maggi", y=0.17, t0=71.95, t1=72.70, size=210, fade_out=False),
    dict(type="sticker", text="WINNER", bg=(255, 194, 26), fg=(27, 26, 58), emoji="🏆", x=0.5, y=0.27, t0=72.10, t1=72.70, size=72),
    dict(type="sparkle", t0=72.00, t1=72.70, x0=0.2, x1=0.8, y=0.17),
    dict(type="burst", t0=71.70, t1=72.70, emoji=["😍"], n=8, seed=21, travel=24),
]
