"""Builds voice / sfx / music stems (48 kHz stereo) matching render.py's plan, then mixes."""
import json, subprocess, math, numpy as np, soundfile as sf
import random
from edl import CLIPS, SRC, FPS

WORK = "/tmp/claude-0/-home-user-Testclaude/f29330e6-8f24-5182-bfb1-c06071f78d9b/scratchpad/work"
SR = 48000
P = json.load(open(f"{WORK}/plan.json"))
PLAN, NMAIN, EV, CARDS = P["plan"], P["n_main"], P["events"], P["cards"]
N = len(PLAN)
T = N / FPS
L = int(T * SR) + SR
rng = np.random.default_rng(3)

# ---------------------------------------------------------------- voice: time-warped source
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", SRC, "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True).stdout
src = np.frombuffer(raw, np.float32).reshape(-1, 2)
voice = np.zeros((L, 2), np.float32)
spf = SR // FPS
fade = int(0.006 * SR)
for ci, c in enumerate(CLIPS):
    frames = [(i, p) for i, p in enumerate(PLAN) if p["clip"] == ci]
    o0 = frames[0][0] * spf
    # source sample position for every output sample (linear between frame anchors)
    ts = np.array([p["t"] for _, p in frames] + [frames[-1][1]["t"] + (frames[-1][1]["t"] - frames[-2][1]["t"])])
    n = len(frames) * spf
    pos = np.interp(np.arange(n) / spf, np.arange(len(ts)), ts) * SR
    seg = np.stack([np.interp(pos, np.arange(len(src)), src[:, k]) for k in range(2)], 1).astype(np.float32)
    env = np.ones(n, np.float32); env[:fade] = np.linspace(0, 1, fade); env[-fade:] = np.linspace(1, 0, fade)
    voice[o0:o0 + n] += seg * env[:, None]

# ---------------------------------------------------------------- SFX synthesis
t_ = lambda d: np.arange(int(d * SR)) / SR


def norm(x, peak=1.0):
    return x / (np.abs(x).max() + 1e-9) * peak


def bandnoise(d, f0, f1, q=6):
    """noise swept through a resonant band (cheap whoosh)."""
    n = rng.standard_normal(int(d * SR)).astype(np.float32)
    out = np.zeros_like(n)
    f = np.geomspace(f0, f1, len(n))
    y1 = y2 = 0.0
    for i in range(0, len(n), 64):  # block-wise biquad bandpass
        w0 = 2 * math.pi * f[i] / SR; al = math.sin(w0) / (2 * q)
        b0, b2 = al, -al; a0, a1, a2 = 1 + al, -2 * math.cos(w0), 1 - al
        x = n[i:i + 64]
        yb = np.empty_like(x)
        x1 = x2 = 0.0
        for j in range(len(x)):
            y = (b0 * x[j] + b2 * x2 - a1 * y1 - a2 * y2) / a0
            x2, x1 = x1, x[j]; y2, y1 = y1, y; yb[j] = y
        out[i:i + 64] = yb
    return out


def whoosh(d=0.32, up=True):
    x = bandnoise(d, 300 if up else 3000, 3000 if up else 300, q=2.5)
    e = np.sin(np.pi * np.linspace(0, 1, len(x))) ** 1.5
    return norm(x * e)


def pop(f=700):
    t = t_(0.09)
    fr = f * (1 + 0.6 * np.exp(-t * 60))
    x = np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-t * 45)
    x[:80] += rng.standard_normal(80) * np.linspace(1, 0, 80) * 0.5
    return norm(x)


def click(f=2400, d=0.025):
    t = t_(d)
    return norm(np.sin(2 * np.pi * f * t) * np.exp(-t * 300) + rng.standard_normal(len(t)) * np.exp(-t * 500) * 0.3)


def tick_seq(d, rate=8):
    out = np.zeros(int(d * SR))
    for k in range(int(d * rate)):
        c = click(3200 if k % 2 else 2600)
        i = int(k / rate * SR); out[i:i + len(c)] += c[:len(out) - i]
    return out


def rev(d=0.8):
    t = t_(d)
    f = 60 + 140 * (t / d) ** 1.5
    ph = 2 * np.pi * np.cumsum(f) / SR
    x = ((ph / np.pi) % 2 - 1) * 0.6 + np.sin(ph * 2) * 0.3
    return norm(x * np.minimum(1, t * 8) * np.exp(-np.maximum(0, t - d * .7) * 10))


def fwoosh(d=0.6):
    n = rng.standard_normal(int(d * SR))
    lp = np.convolve(n, np.ones(40) / 40, "same")
    t = t_(d)
    return norm(lp * np.exp(-t * 5) * np.minimum(1, t * 30))


def sizzle(d=0.9):
    n = rng.standard_normal(int(d * SR))
    hp = n - np.convolve(n, np.ones(6) / 6, "same")
    crack = (rng.random(len(n)) > 0.9985) * rng.standard_normal(len(n)) * 6
    t = t_(d)
    return norm((hp + crack) * np.minimum(1, t * 10) * np.exp(-t * 2.5))


def piano_note(f, d=1.4):
    t = t_(d)
    x = sum(np.sin(2 * np.pi * f * h * t) * a for h, a in ((1, 1), (2, .4), (3, .2), (4, .1)))
    return x * np.exp(-t * 3) * np.minimum(1, t * 200)


def sad_sting():
    out = np.zeros(int(2.6 * SR))
    for k, f in enumerate([440.0, 349.2, 293.7, 220.0]):  # A F D A (minor fall)
        n = piano_note(f, 1.4); i = int(k * 0.28 * SR); out[i:i + len(n)] += n
    return norm(out)


def riser(d=0.8):
    t = t_(d)
    f = 200 * (2 ** (3 * t / d))
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * 0.4 + bandnoise(d, 400, 6000, 3) * 0.6 / 3
    return norm(x * (t / d) ** 2)


def boom():
    t = t_(1.0)
    f = 90 * np.exp(-t * 4) + 38
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 3.2)
    x += rng.standard_normal(len(t)) * np.exp(-t * 25) * 0.3
    return norm(x)


def ding():
    t = t_(0.9)
    return norm((np.sin(2 * np.pi * 1318.5 * t) + .4 * np.sin(2 * np.pi * 2637 * t) + .2 * np.sin(2 * np.pi * 3955 * t)) * np.exp(-t * 5))


def sparkle_sfx():
    out = np.zeros(int(1.0 * SR))
    for k in range(10):
        f = rng.choice([2093, 2349, 2637, 3136, 3520, 4186])
        t = t_(0.25); n = np.sin(2 * np.pi * f * t) * np.exp(-t * 18)
        i = int(k * 0.06 * SR); out[i:i + len(n)] += n
    return norm(out)


def shutter():
    a = click(1800, 0.03); b = click(1300, 0.04)
    out = np.zeros(int(0.12 * SR)); out[:len(a)] += a; out[int(0.06 * SR):int(0.06 * SR) + len(b)] += b
    return norm(out)


def drumroll(d=0.5):
    out = np.zeros(int(d * SR))
    t = 0.0
    while t < d:
        n = rng.standard_normal(int(0.03 * SR)) * np.exp(-np.arange(int(0.03 * SR)) / SR * 90)
        i = int(t * SR); out[i:i + len(n)] += n[:len(out) - i] * (0.4 + 0.6 * t / d)
        t += 0.06 - 0.035 * t / d
    return norm(out)


def scratch():
    t = t_(0.45)
    f = 300 + 900 * np.abs(np.sin(2 * np.pi * 3 * t))
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * 0.5 + rng.standard_normal(len(t)) * 0.4
    return norm(x * np.exp(-t * 4))


def gasp():
    n = rng.standard_normal(int(0.35 * SR))
    b = np.convolve(n, np.ones(12) / 12, "same")
    t = t_(0.35)
    return norm(b * np.sin(np.pi * t / 0.35) ** 2)


sfx = np.zeros((L, 2), np.float32)


def put(x, sec, db=-22, pan=0.0):
    i = int(sec * SR)
    if i < 0 or i >= L:
        return
    g = 10 ** (db / 20)
    x = x[:L - i] * g
    sfx[i:i + len(x), 0] += x * (1 - max(0, pan))
    sfx[i:i + len(x), 1] += x * (1 + min(0, pan))


of = lambda f: f / FPS
CS = {}
for i, p in enumerate(PLAN):
    CS.setdefault(p["clip"], i)
WH = [whoosh(0.3), whoosh(0.35, False), whoosh(0.28)]
POPS = [pop(f) for f in (620, 700, 780, 860)]

for ci, c in enumerate(CLIPS):
    s = of(CS[ci])
    if c.get("punch"):
        put(WH[ci % 3], s - 0.12, -21, pan=random.uniform(-.3, .3))
    if c.get("wipe_out"):
        put(WH[1], of(CS[ci] + sum(1 for p in PLAN if p["clip"] == ci)) - 0.2, -20)

pk = 0
for e in EV:
    t, f0, f1 = e["type"], e["f0"], e["f1"]
    s = of(f0)
    if t in ("leak", "redflash", "whiteflash"):
        put(WH[0], s - 0.1, -19)
    if t == "redflash" and f1 - f0 <= 3:
        put(gasp(), s, -24)
    if t == "build":
        for w in e["words"]:
            put(POPS[pk % 4], of(w["f"]), -25 if e["style"] == "white" else -22); pk += 1
    if t == "title":
        if e.get("typewriter"):
            for k in range(len(e["text"])):
                put(click(2800), s + k * 2 / FPS, -27)
        else:
            put(POPS[pk % 4], s, -21); pk += 1
        if e.get("text2"):
            put(WH[2], of(f0) + 0.4, -22)
    if t == "burst":
        for k in range(e.get("n", 8)):
            put(POPS[(pk + k) % 4], s + k * 3 / FPS, -27, pan=random.uniform(-.5, .5))
    if t in ("sticker",):
        put(POPS[2], s, -20)
    if t == "qmarks":
        for k in range(len(e["marks"])):
            put(POPS[k % 4], s + k * 3 / FPS, -25)
    if t == "meter":
        put(tick_seq(of(f1 - f0), 8), s, -27)
        put(rev(min(0.9, of(f1 - f0))), s + 0.1, -25)
        if any(v >= 0.95 for _, v in e["needle"]):
            put(fwoosh(), s + 8 / FPS, -20); put(sizzle(), s + 0.3, -24)
    if t == "bw":
        put(sad_sting(), s, -21)
        put(scratch(), s - 0.05, -27)
    if t == "vs":
        put(boom(), s + 0.05, -16)
    if t == "scorecard":
        for r in e["rows"]:
            put(ding(), of(r["f"]), -22)
    if t == "sparkle":
        put(sparkle_sfx(), s, -21)
    if t == "dip":
        put(drumroll(of(f1 - f0) + 0.15), s, -22)
        put(riser(of(f1 - f0) + 0.1), s - 0.1, -24)
for cd in CARDS:
    put(riser(0.6), of(cd["f0"]) - 0.6, -23)
    put(shutter(), of(cd["f0"]), -20)
# end card pops
EC = NMAIN / FPS
for k, dt in enumerate([0, 0.1, 0.2, 0.3, 0.5, 0.6]):
    put(POPS[k % 4], EC + dt, -21)
put(whoosh(0.4), EC + 57 / FPS - 0.1, -20); put(sparkle_sfx(), EC + 60 / FPS, -22)

# ---------------------------------------------------------------- music: original light beat, 100 BPM
BPM = 100
beat = 60 / BPM
music = np.zeros(L, np.float32)


def kick():
    t = t_(0.35); f = 120 * np.exp(-t * 25) + 45
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 9)


def snare():
    t = t_(0.25)
    return (rng.standard_normal(len(t)) * 0.7 + np.sin(2 * np.pi * 190 * t) * 0.5) * np.exp(-t * 18)


def hat():
    t = t_(0.06); n = rng.standard_normal(len(t))
    return (n - np.convolve(n, np.ones(4) / 4, "same")) * np.exp(-t * 70)


def chord(freqs, d):
    t = t_(d)
    x = sum(np.sin(2 * np.pi * f * t) + 0.3 * np.sin(2 * np.pi * 2 * f * t + 1) for f in freqs)
    env = np.minimum(1, t * 20) * np.exp(-t * 0.9)
    return x * env / len(freqs)


def bassnote(f, d):
    t = t_(d)
    return np.sin(2 * np.pi * f * t) * np.minimum(1, t * 50) * np.exp(-t * 2.5)


prog = [([261.6, 329.6, 392.0, 493.9], 65.4), ([220.0, 261.6, 329.6, 392.0], 55.0),
        ([174.6, 220.0, 261.6, 329.6], 43.65), ([196.0, 246.9, 293.7, 349.2], 49.0)]
K, Sn, Hh = kick(), snare(), hat()
nbeats = int(T / beat) + 2
for b in range(nbeats):
    s = int(b * beat * SR)
    def add(x, g, off=0):
        i = s + int(off * SR)
        if i < L:
            music[i:i + len(x)] += (x[:L - i] * g).astype(np.float32)
    add(K, 0.9 if b % 4 in (0, 2) else 0.0)
    if b % 4 == 2 and b % 8 == 6:
        add(K, 0.5, beat * 0.5)
    if b % 2 == 1:
        add(Sn, 0.35)
    add(Hh, 0.18); add(Hh, 0.12, beat / 2)
    if b % 4 == 0:
        ch, bf = prog[(b // 4) % 4]
        add(chord(ch, beat * 4), 0.22)
        add(bassnote(bf, beat * 1.5), 0.45)
        add(bassnote(bf, beat * 1.5), 0.35, beat * 2)
music = np.convolve(music, np.ones(3) / 3, "same")  # soften
music = norm(music, 0.5)

# ducking: -4 dB extra while voice is active
venv = np.sqrt(np.convolve((voice.mean(1)) ** 2, np.ones(int(0.05 * SR)) / int(0.05 * SR), "same"))
active = (20 * np.log10(venv + 1e-6) > -38).astype(np.float32)
active = np.convolve(active, np.ones(int(0.25 * SR)) / int(0.25 * SR), "same")
duck = 10 ** (-4 * np.clip(active, 0, 1) / 20)
music_st = np.stack([music * duck, music * duck], 1)
# end card: music comes up and fades out at the very end
ec = int(NMAIN / FPS * SR)
music_st[ec:] *= 1.6
tail = int(0.8 * SR)
music_st[int(T * SR) - tail:int(T * SR)] *= np.linspace(1, 0, tail)[:, None]
music_st[int(T * SR):] = 0

L2 = int(T * SR)
sf.write(f"{WORK}/voice_raw.wav", voice[:L2], SR, subtype="FLOAT")
sf.write(f"{WORK}/sfx.wav", sfx[:L2], SR, subtype="FLOAT")
sf.write(f"{WORK}/music.wav", music_st[:L2], SR, subtype="FLOAT")
print("stems written", T)
