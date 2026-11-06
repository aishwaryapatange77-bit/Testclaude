# Edit pipeline: Desi Noodle Battle reel

These scripts produced `deliverables/final_reel.mp4` from the raw iPhone clip. Paths inside the scripts point at the session scratchpad; change `WORK`, `ASSETS`, `M` and `SRC` to re-run them elsewhere.

1. `analyze.py`: runs per-frame MediaPipe face detection and person segmentation (the `selfie_multiclass` model), writing `faces.json` and `masks.npy`.
2. `edl.py`: the edit itself, with clips, zooms, captions and effects, all keyed to source timecode. `HANDLE` sets the Instagram handle.
3. `gfx.py`: neon bubble text, the glossy 3D question marks, the spice-meter, emoji, stickers, and the Instagram and YouTube glyphs.
4. `render.py`: `python3 render.py plan`, then `python3 render.py <i> 4` for i = 0..3 (parallel workers), and `still <frame>` for QA frames.
5. `audio.py`: builds the time-warped voice, the synthesized SFX and the original beat. These stems are then mixed and loudness-normalised with ffmpeg (see the session notes).

Fonts: Bubblegum Sans and Sniglet (OFL), plus Noto Color Emoji.
