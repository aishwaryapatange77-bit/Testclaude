# MASTER EDIT PROMPT — "Desi Noodle Battle" vertical food reel
### (Ching's Schezwan vs Slurrp Farm Millet Hakka — styled after the "Celebrity Favourite Food Challenge" reference edit)

> Copy everything below this line and give it to Claude together with the raw video file.

---

## 0. YOUR ROLE AND THE DELIVERABLE

You are a senior short-form video editor and motion designer. You specialise in Indian food and lifestyle Instagram Reels and YouTube Shorts. Edit the attached raw video into a finished, high-retention vertical reel.

Match the **editing language** of a reference reel I like: chunky neon bubble titles, punch-ins, light-leak burns, red flashes, B&W mood shifts, subject-cutout graphics, emoji bursts and an end card. Every rule from that reference is written out in this prompt. The **colours are re-designed** to suit my footage (see §4 and §5).

**Deliverables**
1. `final_reel.mp4`: 1080×1920, 9:16, 30 fps, H.264 High profile, about 16 Mbps VBR, AAC 320 kbps 48 kHz, yuv420p, Rec.709, `+faststart`.
2. `captions.srt`: the full transcript with word-level timing. Use it to place the caption builds.
3. `edit_decision_list.md`: a table of every cut, effect, text and SFX with **source** and **output** timecodes. I want to be able to check your work against this prompt.
4. A 3×4 contact sheet of stills from the final edit, for a quick visual QA.

---

## 1. THE RAW FOOTAGE (what you are working with)

- **File:** one `.mov`, HEVC, **720×1280**, 30 fps, **72.7 s**, stereo AAC. Upscale to 1080×1920 with Lanczos. Add light sharpening (unsharp 5:5:0.6) after every digital zoom. 720p gets soft fast, so **never digitally zoom past 170 %** of the 1080 frame.
- **Location:** a single bright indoor dining area for the whole video. Ivory/cream walls. A **warm-white backlit leaf-shaped LED wall panel** (three/four glowing leaves) sits directly behind my head. White marble floor. A dark-wood dining table with white top and chairs on the right. Brass wall sconces.
- **Me (host):** terracotta/rust-orange floral printed shirt, navy trousers, hair tied back. Filmed on a gimbal/phone at chest height. I walk slowly **towards** the camera and talk straight to the lens with lots of hand gestures.
- **Products:**
  - **Product A — Ching's Secret Schezwan Instant Noodles.** White/orange/red pack with a chef's face logo and a red Schezwan band.
  - **Product B — Slurrp Farm Millet Hakka Noodles (Classic Masala).** Bright yellow pack, red "slurrp farm" badge, cartoon kid, "NO MAIDA" claim.
- **Language:** Hindi/Hinglish with some English. Transcribe it (see §2). **Do not invent dialogue.** Every caption must be words I actually say, unless this prompt marks it as a graphic label.

### 1a. Source structure (measured from the file — use these timecodes)

The timecodes below are **SOURCE** timecodes. "Speech" and "silence" come from audio analysis (silence < −32 dB for 0.35 s or longer). Existing hard cuts are at **5.70, 19.00, 25.67 and 38.53**.

| Source TC | What happens | Speech/silence |
|---|---|---|
| 0.00–3.56 | Wide shot. I walk in holding the **Ching's** pack, flip it towards the lens (≈1.0), turn it while talking (2–3) | speech |
| 3.56–3.92 | — | silence (trim) |
| 3.92–5.70 | Ching's pack held flat to the lens, front facing (≈4.0 is the best packshot frame), then held at chest | speech |
| **5.70 cut** | | |
| 5.70–10.01 | Eating Ching's. Fork to mouth (≈6.0–7.0), chewing with the bowl, **eyes squeezed, scrunched "spicy!" face (≈8.5–10)** | silence: bites/chewing |
| 10.01–10.59 | Short reaction line | speech |
| 10.59–11.20 | — | silence |
| 11.20–11.50 | Tiny word/exclamation | speech |
| 11.50–13.03 | **Squinting, lip-pursed "judging the taste" face**, noodles on fork | silence |
| 13.03–14.42 | Talking about the taste | speech |
| 14.42–14.81 | — | silence |
| 14.81–15.76 | Talking | speech |
| 15.76–17.57 | **Second bite of Ching's**, bowl at chin (≈16.0) | silence |
| 17.57–18.44 | Wrap-up line on Ching's | speech |
| 18.44–19.00 | — | silence |
| **19.00 cut** | | |
| 19.00–25.60 | **Slurrp Farm** pack intro. Pack raised next to my face (19–20), **pushed right up to the lens covering my face (≈20.0 and again ≈24.0–25.0)**, pack held to the side while I talk (21–23) | speech (brief pause 20.01–20.38) |
| **25.67 cut** | | |
| 25.60–27.70 | First bite of Slurrp, leaning down over the bowl (≈26.0) | silence |
| 27.70–28.93 | Talking | speech |
| 28.93–29.58 | — | silence |
| 29.58–31.99 | Talking, fork in hand | speech |
| 31.99–32.76 | — | silence |
| 32.76–34.88 | Talking | speech |
| 34.88–36.32 | **Noodles lifted high on the fork** (≈35.5–36) | silence |
| 36.32–37.39 | Talking | speech |
| 37.39–37.78 | — | silence |
| 37.78–41.25 | **Frowning / squinting / unsure face (≈37–39)**, then talking (hard cut at 38.53 inside this) | speech |
| 41.25–41.61 | — | silence |
| 41.61–42.21 | Talking | speech |
| 42.21–43.72 | **Long noodle lift on the fork (≈43.0)** | silence |
| 43.72–46.75 | Talking | speech |
| 46.75–51.45 | **Big happy slurps, bowl at chin (≈48–50)** | silence: eating |
| 51.45–51.99 | Short line | speech |
| 51.99–52.96 | — | silence |
| 52.96–53.99 | Talking | speech |
| 53.99–54.44 | — | silence |
| 54.44–56.49 | **Big smile, closer to camera, explaining (≈53–55)** | speech |
| 56.49–57.05 | — | silence |
| 57.05–59.83 | Explaining with hand gestures | speech |
| 59.83–60.50 | — | silence |
| 60.50–63.17 | "Oh!" mouth-open expressive face (≈60), explaining | speech |
| 63.17–63.56 | — | silence |
| 63.56–65.59 | Explaining | speech |
| 65.59–66.16 | — | silence |
| 66.16–69.96 | Talking, fork near mouth, counting on fingers | speech |
| 69.96–70.46 | — | silence |
| 70.46–72.70 | **Final verdict to camera**, hand gesture, smile | speech |

---

## 2. STEP ZERO — ANALYSE BEFORE YOU EDIT (mandatory)

1. **Transcribe** the audio with word-level timestamps, using Whisper large-v3 or similar. Set language to Hindi; Hinglish is expected. Write each word in the script I use: Hindi words in **Roman Hinglish** (e.g. "bahut spicy hai"), not Devanagari. Save the transcript as `captions.srt`.
2. **Find the key words** from the transcript:
   - the first strong noun or hook in the first 2 s
   - every product name I say
   - every taste word ("spicy", "teekha", "tasty", "healthy", "masala", "bland", "achha", "bekaar", etc.)
   - every positive word ("best", "mast", "love", "kamaal", "winner") and every negative or disappointed word ("nahi", "not good", "disappointed", "pasand nahi", "kuch khaas nahi")
   - **the final verdict sentence (≈70.5–72.7)**
3. **Work out the verdict.** Find which product I prefer, and the moment I say it. The winner gets the "WINNER" treatment and the heart-eyes burst. The other product gets the B&W mood shift if I'm negative about it. **If the transcript is ambiguous, ask me before rendering**; don't guess the winner.
4. Every placeholder in this prompt looks like **⟦…⟧**. Replace each one with my **real words** from the transcript. The suggestions next to them are only fallbacks.

---

## 3. FORMAT AND PACING

- 9:16, **1080×1920**, 30 fps. Target output length about **58–64 s of content plus a 6.4 s end card** (≈ 64–70 s total). You get there by trimming the silences.
- **Tighten:** Cut every silence gap marked "trim" down to **4–6 frames** of breath, using jump cuts. Silences that are *eating/reaction beats* are content. Shorten them to the best 1.2–2.5 s, never remove them completely. Remove ums, false starts and repeated words.
- **Never hold one framing longer than ~3 s.** Most of the footage is one continuous walking take, so you create "new shots" digitally with three zoom levels, and you alternate between them on every jump cut and emphasis word:
  - **WIDE** = 100 % (full frame, head to knees)
  - **MID** = 130–135 % (waist up), centred on my face
  - **CLOSE** = 155–170 % (chest up / face), centred on my face. Keep my eyes on the upper-third line (y ≈ 33 %).
  - Never repeat the same zoom level across a jump cut; a jump cut must change the scale or it looks like a glitch.
  - Track my face so the crop follows me as I walk forward. Use smoothed face tracking with a 0.3 s smoothing window and no jitter.
- Very slow **constant push-in** (100 → 104 % over the shot) on any shot longer than 2 s, so the frame is never dead.
- Optional speed ramps: 100 % → **50 %** → 100 % on noodle-lift moments (≈35.5, ≈43.0) and on the big slurp (≈48–49). Use frame blending, or optical flow if available.

---

## 4. LOOK / COLOUR GRADE (adapted to my footage)

The reference is "warm, bright, airy, lifted shadows, saturated pinks and teal-greens". My footage is already bright and warm, but it is **slightly flat and grey-beige**: averaged wall and floor values sit around #A9A097–#BBB597. Grade it like this:

- **Exposure / tone:** +0.2 to +0.3 stop. Lift shadows slightly (blacks to about 12/255). Gentle S-curve for contrast. Keep the highlights of the white walls and the LED leaf panel **below clipping**; roll off softly.
- **White balance:** neutral-warm. Walls should read **clean ivory/cream (#F3EDE2–#EFE6D6)**, not grey and not yellow.
- **Saturation (selective):**
  - Terracotta shirt: +15 % saturation, aiming for about #C8552E–#D9622F.
  - Noodles / turmeric yellows: +20 % (make the food look appetising and golden, ~#E9B83A).
  - Ching's red band and Slurrp Farm yellow pack: +15 %, so they pop as hero props.
  - Navy trousers: keep them deep (~#1B1A3A), no crushing.
  - **Skin protection:** limit skin hue shifts to ±3°, keep skin soft and warm, and apply a light skin-smoothing pass at 20 % with no plastic look.
- **Glow / bloom:** subtle bloom on the LED leaf panel and sconces (threshold 85 %, radius 40 px, 15 % strength). It gives the dreamy "airy" glow the reference has.
- **Depth:** the background is in focus in my footage. For the MID and CLOSE punch-ins, add a **fake shallow depth of field**. Use the person-segmentation matte (see §7, effect 5), blur the background (Gaussian 6–10 px at 1080p) and keep me sharp. That reproduces the reference's "blurry background" look.
- Light vignette (−8 %, very soft). Fine film grain (2 %) on top of everything to glue the graphics in.

### 4a. Palette for this edit (taken from my video)

| Token | Hex | Where it comes from |
|---|---|---|
| CREAM | #F6EFE3 | walls and marble |
| LEAF GLOW | #FFE9B0 | LED leaf panel |
| TERRACOTTA | #D9582B | my shirt |
| TURMERIC | #FFC21A | noodles |
| CHILLI RED | #FF3B1F | Ching's Schezwan band |
| MILLET YELLOW | #FFE03A | Slurrp Farm pack |
| SLURRP RED | #E8233A | Slurrp Farm badge |
| FRESH GREEN | #9BEA4A | "millet / healthy" accent |
| NAVY INK | #1B1A3A | my trousers; outlines and shadows |

---

## 5. TEXT SYSTEM (same style as the reference, recoloured)

**Font:** a chunky, rounded, cartoon display font that **mixes capital and lowercase letter shapes at the same cap height**, e.g. "NOODLE battle", "ROUND two", "next ONE", "Let's EAT". Use **Bubblegum Sans**, **Sniglet ExtraBold**, or CapCut "Bubble"/"Candy" in this order of preference. The mixed casing is a deliberate style: write each word as the examples show, not auto-capitalised.

**Neon glow treatment** (same as the reference):
- Solid fill colour.
- **Wide soft outer glow**, radius about 25 px at 1080 width, 80 % opacity, in a **deeper shade** of the fill.
- Faint inner highlight: a 2 px lighter inner stroke at the top edge, 40 % opacity.
- **Extra for my footage:** my background is bright cream, so neon glows wash out. Add a **3 px NAVY INK (#1B1A3A) outline** at 85 % opacity *under* the glow. Also add a **soft drop shadow** (NAVY INK, 0 px x / 6 px y, 18 px blur, 45 %). Every title must pass a legibility check on the brightest wall area.

**Colour code (replaces the reference's yellow/blue/pink/magenta roles):**

| Role | Reference used | **Use in my edit** |
|---|---|---|
| **Hook / call-to-action word** | yellow #FFD400 + orange glow | **TURMERIC fill #FFC21A + orange glow #FF6A00** |
| **Product A — Ching's / anything spicy** | sky-blue + blue glow (topic) | **CHILLI fill #FF4B2B + deep red glow #B80000** |
| **Product B — Slurrp Farm / millet / healthy** | sky-blue + blue glow (topic) | **MILLET YELLOW-GREEN: fill #C9F55A + green glow #1FA84A** |
| **Reactions / taste words** | pale pink + magenta glow | **PEACH CREAM fill #FFE1C6 + TERRACOTTA glow #E0562A** |
| **Big moment: VS, WINNER, verdict** | hot magenta + pink glow | **HOT MAGENTA fill #FF2FD0 + pink glow #FF7AE6**. Keep the reference's magenta for the biggest moments only: it is the one colour that isn't in my scene, so it jumps out. |
| Small spoken captions (secondary) | white, soft shadow, no glow | **White #FFFFFF, NAVY INK soft shadow (4 px, 12 px blur, 60 %), no glow**, Sniglet/Bubblegum, 54–60 px |

**Sizes (at 1080×1920):** primary titles 110–150 px cap height; lower-third builds 90–110 px; secondary white captions 54–60 px. Keep a safe area of 90 px each side, 250 px top and 380 px bottom (Instagram UI). Lower third sits at y ≈ 73–77 %, top titles at y ≈ 13–17 %.

**Animation (identical to the reference):**
- **Entrance (default): POP-IN.** Scale 120 % → 95 % → 100 % over **6 frames**, ease-out. The glow **flickers once** on entry (opacity 80 → 30 → 80 % over frames 2–4).
- **Exit:** a hard cut with the shot, or a 4-frame fade.
- **Word-by-word builds:** multi-word captions build **one word at a time**. Each word pops in **3–4 frames** after the previous one, timed to the moment I *say* that word (use the word timestamps). The line re-centres as it grows.
- **Typewriter variant:** letter by letter, 2 frames per letter. Use it for the product names (as the reference did for "B PRAAK").
- **Colour-swap-on-flash:** when a RED FLASH (effect 3) passes over a title, the title's fill switches colour during the flash (as the reference turned the name pink).
- **Morph:** one word morphs into another (as the reference did "IMPROVED" → "IMPROVISED"). Cross-scale 100 → 110 → 100 % over 6 frames, with the letters cross-dissolving.
- Pop SFX on every word or letter build (see §10).

---

## 6. PERSISTENT WATERMARK

- A small white Instagram glyph with **"@⟦MYHANDLE⟧"** in tiny caps (22–24 px, letter-spacing +8 %) under it, at **60 % opacity**, with a NAVY INK 30 % soft shadow.
- It **jumps position from shot to shot so it never covers my face, the food or a product pack**. Use either **top-right (x ≈ 88 %, y ≈ 27 %)**, which sits on the plain wall left of the sconce, or **middle-left (x ≈ 4 %, y ≈ 57 %)**. Pick the clear one per shot. It switches only on cuts, never mid-shot.
- Hide it during the end card (the end card has its own handle).

---

## 7. EFFECTS LIBRARY (all from the reference; 6 adapted, 3 new ones added for a product battle)

1. **PUNCH-IN:** instant 140–170 % digital zoom on my face (or on the pack or bowl when that's the subject), with **3–4 frames of zoom motion blur** (radial blur from 18 → 0). Use it on emphasis words. Add a whoosh.
2. **LIGHT-LEAK BURN (≈12 f):** the frame washes to white (2 f). Yellow and orange film-burn light leaks sweep across it diagonally, tinted with TURMERIC #FFC21A and TERRACOTTA #D9582B, with a sweep of glow (6 f). Then it settles into the next clip (4 f). Text can stay on screen through it.
3. **RED FLASH OUT:** 2 frames of a CHILLI RED (#FF2A1A) colour overlay at 85 %, then 2 frames of a white/yellow burn, then a cut. Use it to leave a product hero card (the equivalent of leaving a celeb cutaway) and to punctuate "SPICY" moments.
4. **B&W MOOD SHIFT:** over about 1 s, fade saturation from 100 % to 0 % while I say something negative or disappointed. Hold in black and white with a slow 100 → 105 % push-in, and add a subtle vignette (−15 %). Cut back to full colour on the next shot. **Use it at most twice.** Only use it on genuinely negative lines (see §8).
5. **SUBJECT-CUTOUT OVERLAY:** separate me from the background with person segmentation (MediaPipe Selfie Segmentation, RVM, rembg or SAM2), feather the matte 3 px and fix the hair edges. Place the graphic **between the background and me**, so my head and shoulders overlap it. The glowing **LED leaf panel behind my head is the perfect stage**: graphics should appear to come out of that panel.
6. **PACK-PASS WIPE (adapted from the "body-pass wipe"):** in my footage I push the product pack right up to the lens until it fills the frame (Slurrp at ≈20.0 and ≈24.0–25.0, Ching's at ≈1.0). That frame-filling moment is the cut point into the next scene. Add a 4-frame directional motion blur in the direction the pack moves.
7. **DIP DISSOLVE:** a double-exposure dissolve (6 f) into a dark, low-key close-up, then a fade to near black (12 f), then a hard cut back. Use it once, to build suspense just before the verdict (see §8, ≈69.9).
8. **NEW: PRODUCT HERO CARD (replaces the celeb cutaways).** Freeze-frame the best packshot frame. Cut out **just the pack** (rotoscope or segmentation plus a manual mask), straighten it and scale it to about 70 % of frame width. Float it with a slow 3 % bob and a 2° sway over a **blurred, darkened (−40 %) copy of the same frame**. Add a thin border round the frame (8 px), coloured to match the pack: CHILLI RED/white for Ching's, MILLET YELLOW/SLURRP RED for Slurrp. The product name builds word by word in the lower third, in that product's neon colour, over a dark gradient band (NAVY INK 0 → 70 % from y 65 % to 100 %). Enter with a LIGHT-LEAK BURN; exit with a RED FLASH OUT. 2.0–2.5 s each.
9. **NEW: SPICE-METER (replaces the reference's giant wall clock).** A big glossy analog **semicircular gauge** about 90 % of frame width: cream face, silver rim, tick marks, a green → yellow → orange → red gradient arc and a red needle, labelled "teekha-meter" in the bubble font. It scales up from 40 % with a slight spin and fade, **placed BEHIND my head using the cutout (effect 5)**, centred on the LED leaf panel. The needle swings hard into the red with motion-blur trails, overshoots and wobbles. Add ticking/rev SFX. On the Slurrp section the same gauge returns and the needle settles in the green/yellow zone.
10. **NEW: EMOJI / ICON BURSTS (same physics as the reference's heart-eyes burst):** 6–8 emoji of mixed sizes (90–220 px) burst from the lower-left, then arc **up and out of the top of the frame**, staggered 3 frames apart. Each has a slight spin (±15°) and a scale pop. The larger ones closer to the lens get a 6 px blur (fake out-of-focus). Variants: 🔥 + 🌶️ for spicy moments; 😍 for the winner moment; 🤔 or glossy white 3D question marks for confusion (see the timeline).

---

## 8. TIMELINE (keyed to SOURCE timecode; output timecode will be shorter after the trims — list both in the EDL)

### SECTION 1 — HOOK (source 0.00–5.70)
- **0.00–1.00:** Open at **MID 130 %** with a fast 130 → 120 % pull-out over 10 frames, so the first frame has motion. At **≈0.3** (my first strong word) the hook title pops in **top centre, y ≈ 15 %, TURMERIC hook style**: ⟦first hook keyword⟧. Fallback: **"NOODLE battle"**.
- **≈1.00:** I flip the Ching's pack to the lens: **PUNCH-IN to 155 %** with zoom blur and a whoosh. The pack and my face fill the frame.
- **≈1.4–3.5:** **SPICE-METER** (effect 9) scales up **behind my head** via the cutout. Its needle starts at zero and twitches. The hook title stays on screen.
- **3.56–3.92:** trim.
- **3.92–5.70:** **WIDE.** At **≈4.0** (pack flat to the lens) trigger a **LIGHT-LEAK BURN** into **PRODUCT HERO CARD A** (effect 8). Freeze-frame the pack. Build **"CHING'S" → "Schezwan"** letter by letter (typewriter) in **CHILLI neon** in the lower third. Hold 2.0 s, then **RED FLASH OUT** at ≈5.6. The hook title is gone by now.
- Small white caption at y ≈ 77 %, word by word: my actual line here (from the transcript).

### SECTION 2 — EATING CHING'S (source 5.70–19.00)
- **5.70–7.6 (bite):** Keep the best 1.5 s of the fork going to my mouth. **CLOSE 165 %** on my mouth and fork, with a whoosh on the cut-in.
- **≈8.3–10.0 (scrunched spicy face):** cut to **MID 135 %**. On the peak of the face, play a **🔥/🌶️ burst** (effect 10) from lower left. Hit a quick **RED FLASH** (2 f only, no cut) synced to the face. Push the **SPICE-METER needle hard into red** behind my head (cutout), with overshoot and wobble. Pop in **"SPICY!!"** in **CHILLI neon** at mid-frame (y ≈ 55 %). If I actually say "teekha" or "spicy", sync it to that word; otherwise pop it on the face. Add a subtle screen shake (±6 px, 8 frames).
- **10.01–15.76:** jump-cut the speech, trimming the silences at 10.59–11.20 and 11.50–13.03 down to about 0.3 s. **Keep about 1 s of the squint/lip-purse "judging" face (≈12.0)**. On it, 5 glossy white 3D question marks pop in one after another around my head and float upwards. Some sit **behind my head (cutout)**, and the larger ones near the lens are out of focus (effect 10, confusion variant). Alternate WIDE ↔ CLOSE on each jump cut. Build my taste words word by word in **PEACH-CREAM reaction neon**, lower third: ⟦taste words from transcript⟧.
- **Conditional B&W #1:** if my Ching's comments at 13.0–15.8 are **negative** (too spicy, too oily, not good), apply the **B&W MOOD SHIFT** over the most negative sentence. Use a sad piano sting or record scratch. Otherwise skip it here.
- **15.76–17.57 (second bite):** keep 1.2 s. **PUNCH-IN 160 %**, then back out to WIDE.
- **17.57–18.44:** wrap-up line, small white caption, word by word.
- **≈18.44 → 19.06 transition:** **LIGHT-LEAK BURN** into Section 3. Over the burn, pop **"ROUND two"** in **TURMERIC hook neon**, centred at y ≈ 45 %, held 0.8 s.

### SECTION 3 — SLURRP FARM INTRO (source 19.00–25.67)
- **19.06–20.01:** **MID 130 %**, pack raised beside my face. Typewriter **"SLURRP farm"** in **MILLET green neon**, top, y ≈ 15 %.
- **≈20.0 (pack covers my face):** **PACK-PASS WIPE** (effect 6) into **PRODUCT HERO CARD B** (effect 8). Freeze-frame the clearest Slurrp packshot (≈24.0 has it fully front-on; you can use that frame here). Build **"MILLET" → "HAKKA" → "Noodles"** word by word, MILLET green neon, lower third, over the gradient band. Add a small sticker-style badge "NO maida" (white bubble text on a SLURRP RED pill, pop-in) at upper-right of the pack. Hold 2.0 s, then **RED FLASH OUT**. During the flash the title fill swaps to CHILLI red for 2 frames, then back (the reference's colour-swap trick).
- **20.38–24.0:** back to the live shot. Alternate WIDE / MID on the jump cuts. Secondary white captions follow my speech word by word. Keep one key claim from what I say (e.g. ⟦"healthy"⟧, ⟦"millet"⟧) as a **MILLET-green** neon word.
- **≈24.0–25.0 (pack fills the lens again):** **PACK-PASS WIPE** with a 4-frame motion blur, cutting into 25.67.

### SECTION 4 — EATING SLURRP (source 25.67–46.75)
- **25.67–27.70 (first bite):** keep 1.5 s, **CLOSE 160 %**. The SPICE-METER briefly appears behind my head with the needle settling in the green/yellow zone (contrast with Ching's), 1.2 s, scale-out exit.
- **27.70–34.88:** jump cuts (trim 28.93–29.58 and 31.99–32.76). Change the zoom level every 1.5–2.5 s and add a **PUNCH-IN** on each emphasis word. Build taste words word by word in **PEACH-CREAM neon**, lower third.
- **34.88–36.32 (noodle lift):** speed ramp 100 → 50 → 100 %, **CLOSE 165 % on the fork and noodles**, slow 105 % push. If you can, briefly rack the background blur (effect 5 matte) so the noodles feel macro.
- **≈37.0–39.0 (frown/unsure face):**
  - If my words here are **doubtful or questioning**, use the 3D question-mark pop (5–7 marks, some behind my head) and a reaction caption in PEACH-CREAM neon.
  - If they're **negative**, use **B&W MOOD SHIFT #2** instead, with the slow push-in, and cut back to colour at the 38.53 cut.
  - **Do not use both on the same moment.**
- **38.53–46.75:** the long take starts. Create shot variety: jump-cut the silences (41.25–41.61 and 42.21–43.72, keeping the noodle lift at ≈43.0 with a speed ramp). Change the punch level every 2–3 s.
- If at any point I say an "improved / better / healthier"-type comparison word that has a natural twin, use the **MORPH** effect (reference: "IMPROVED" → "IMPROVISED") in HOT MAGENTA mid-frame. Example: ⟦"TASTY" → "HEALTHY"⟧ or ⟦"MAIDA" → "MILLET"⟧. Only do this if my words support it.

### SECTION 5 — THE GOOD BITE AND THE COMPARISON (source 46.75–69.96)
- **46.75–51.45 (big happy slurps):** keep the best 2.0–2.5 s. Speed-ramp the slurp. Use **CLOSE 165 %**, then snap out to WIDE on the swallow.
  - **If Slurrp is the winner**, play the **😍 heart-eyes burst** (≈8 emojis, lower-left, arcing up and out of the top of frame, staggered, different sizes) on the smile right after the slurp.
  - If Ching's is the winner, move the 😍 burst to my verdict line instead.
- **51.45–57.05:** big smile and explaining. Jump cuts with PUNCH-INs. On my most positive phrase, a word-by-word **PEACH-CREAM** neon build.
- **≈57.0–60.0: VS SPLIT moment.** When I start comparing the two, a graphic panel slides in **behind me (cutout)**, in front of the leaf panel.
  - It's a split-screen card: **left half CHILLI RED, right half MILLET YELLOW**, divided by a jagged lightning-bolt edge.
  - Each half shows its pack cutout (from the hero cards), scaled to about 35 % of frame width.
  - A huge **"VS"** in **HOT MAGENTA neon** sits in the middle with a pop-in and a camera-shake impact.
  - The packs slide in from their sides (8 f, ease-out back). Hold 2.0 s, then a scale-out exit.
- **60.50–66.16:** jump cuts and punch-ins. The "Oh!" face at ≈60.5 gets a **PUNCH-IN 165 %**. Animate my **comparison points as a mini scorecard**: two small columns (Ching's red pill, Slurrp green pill) appear top-left, and ✓/✗ ticks pop next to each point as I say it (taste, spice, health, value). **Only include points I actually say.**
- **66.16–69.96:** counting on my fingers. Pop a number per finger ("1", "2", "3") in TURMERIC neon near my hand, tracked.

### SECTION 6 — VERDICT (source 69.96–72.70)
- **69.96–70.46 (silence before the verdict):** **DIP DISSOLVE** (effect 7). Use a 6-frame double-exposure into a darkened, desaturated CLOSE of my face, then about 10 frames towards near-black for suspense. Add a riser and a drum roll. Hard cut back on my first verdict word.
- **70.46–72.70:** **CLOSE 160 %**, then PUNCH-IN on the winner word. Caption the **last line one word at a time, centre-low (y ≈ 70 %), HOT MAGENTA neon**, exactly as I say it. Reference equivalent: "BEST" → "KA" → "PANEER". Example shape: ⟦"MILLET" → "WALA" → "WINNER"⟧.
  - The **winner's pack cutout** pops in above my shoulder with a gold "WINNER 🏆" sticker (white bubble text on a TURMERIC pill).
  - A sparkle sweep crosses the pack.
  - 😍 burst here if it wasn't used at ≈50.

---

## 9. END CARD (6.4 s, after the last frame)

- Hard cut to a **flat TERRACOTTA background (#E0602C)**. This replaces the reference's orange #FFA800 and matches my shirt.
- **+0.0 s:** three lines **"WATCH FULL / VIDEO ON / YOUTUBE"** pop in at the top, white bubbly font, soft NAVY INK drop shadow, staggered 3 frames per line.
- **+0.3 s:** the main video's **16:9 thumbnail** ⟦I will supply it; if not, build one from the VS card⟧ scales in at the centre (120 % → 97 % → 100 %). It has 24 px rounded corners and a soft shadow.
- **+0.5 s:** a red YouTube play button pops in below it, then **"@⟦MYHANDLE⟧"** in white.
- **+2.4 s:** the whole card dims to about **25 % brightness** (black overlay at 75 %). A **white outline Instagram logo** pops in, centred over the thumbnail, with "@⟦MYHANDLE⟧" under it. **Over 0.6 s the logo colour shifts from white to the Instagram pink/purple/orange gradient.**
- Hold until the end.

---

## 10. AUDIO

- **My voice is the main track.** Normalise it to −14 LUFS integrated with a −1 dBTP true-peak limit, light compression (3:1) and a de-esser. Remove room hum and AC hiss gently. Keep the eating and slurping sounds **audible and crisp**, because they sell the food. Lift those gaps by about 3 dB.
- **Music:** a light, trending, upbeat Indian or lo-fi pop beat under everything at about **−18 dB** relative to the voice, ducked another 4 dB while I speak. Use royalty-free or library music only. Leave it on a separate track so I can swap in an Instagram trending sound.
- **SFX:**
  - whoosh on every PUNCH-IN, flash and wipe
  - **pop** on every word/letter build, emoji and sticker
  - **ticking + engine-rev** under the SPICE-METER, with a sizzle or fire "fwoosh" when the needle hits red
  - a cartoon "sizzle" and a short gasp on the spicy face
  - a sad piano sting or record scratch on each B&W shift
  - a small riser before each PRODUCT HERO CARD and before the verdict
  - an impact "boom" on the VS
  - a "ding" on each scorecard tick
  - a sparkle on WINNER
  - a camera-shutter click on each freeze-frame
- Keep SFX at −20 to −24 dB so they never mask my words.

---

## 11. TECHNICAL IMPLEMENTATION GUIDANCE (if you're building this with code)

- **Pipeline:** FFmpeg for decode, trims and the final encode. Python (MoviePy/OpenCV/PIL) **or** Remotion/After Effects-style compositing for the graphics. Render the graphics as RGBA layers and composite them at 1080×1920.
- **Segmentation:** MediaPipe Selfie Segmentation or Robust Video Matting for the per-frame person matte. Temporally smooth the matte (an EMA over 3 frames) to avoid flicker. Use the matte for effect 5 (graphics behind me), the fake depth of field (§4) and the hero-card pack cutouts (plus a manual mask).
- **Face tracking:** MediaPipe Face Detection to centre the punch-in crops. Smooth the crop path and clamp it to the frame edges.
- **Word timing:** Whisper with word timestamps drives every word-by-word build.
- **3D question marks and spice-meter:** render them as PNG sequences (Blender/three.js) or draw clean 2.5D vector versions with gloss highlights and soft shadows. They must look **glossy and premium, not clip-art**.
- **Emojis:** use Apple- or Noto-style colour emoji PNGs at high resolution. Animate their paths along arcs with ease-out and staggered starts.
- **Quality bar:** no aliasing on text (render at 2× and downscale), no matte halos, no jitter on tracked elements, and no title covering my mouth or the food in the bowl.

---

## 12. FINAL QA CHECKLIST (check every item before delivering)

- [ ] 1080×1920, 30 fps, about 64–70 s, audio at −14 LUFS, no clipping.
- [ ] No framing held longer than about 3 s; every jump cut changes the zoom level.
- [ ] Every caption matches what I actually say (spelling in Roman Hinglish); no invented dialogue.
- [ ] The colour code is consistent: Ching's = CHILLI red neon, Slurrp = MILLET green neon, hook = TURMERIC, reactions = PEACH-CREAM/terracotta, VS/verdict = HOT MAGENTA.
- [ ] Every neon title is legible on the bright cream wall (navy outline and shadow present).
- [ ] The watermark never covers my face, the food or a pack, and only moves on cuts.
- [ ] Every one of these is used at least once: punch-in, light-leak burn, red flash out, B&W shift (only if a negative line exists), subject-cutout overlay, pack-pass wipe, dip dissolve, hero card ×2, spice-meter, emoji burst, question marks, VS card, morph (only if my words support it).
- [ ] The winner and the verdict match the transcript (ask me if unsure).
- [ ] The end card matches §9 exactly.
- [ ] The EDL, the SRT and the contact sheet are delivered.

**Before rendering the final**, send me:
1. the transcript with the key words highlighted
2. the winner you detected
3. the list of placeholders ⟦…⟧ and what you plan to fill them with

Then render.
