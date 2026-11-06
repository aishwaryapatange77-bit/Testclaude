"""Per-frame analysis: face box + person matte for the raw clip.
Outputs: faces.json (per frame [cx, cy, w, h] in 720x1280 px, smoothed) and masks.npy (N,640,360) uint8."""
import sys, json, subprocess, numpy as np, cv2
import mediapipe as mp
from mediapipe.tasks import python as mpt
from mediapipe.tasks.python import vision

SRC, OUT, MODELS = sys.argv[1], sys.argv[2], sys.argv[3]
W, H, FPS = 720, 1280, 30
N = 2181

proc = subprocess.Popen(["ffmpeg", "-v", "error", "-i", SRC, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                        stdout=subprocess.PIPE)
fd = vision.FaceDetector.create_from_options(vision.FaceDetectorOptions(
    base_options=mpt.BaseOptions(model_asset_path=f"{MODELS}/face_detector.tflite"),
    running_mode=vision.RunningMode.VIDEO, min_detection_confidence=0.4))
seg = vision.ImageSegmenter.create_from_options(vision.ImageSegmenterOptions(
    base_options=mpt.BaseOptions(model_asset_path=f"{MODELS}/selfie_multiclass.tflite"),
    running_mode=vision.RunningMode.VIDEO, output_confidence_masks=True))

masks = np.lib.format.open_memmap(f"{OUT}/masks.npy", mode="w+", dtype=np.uint8, shape=(N, 640, 360))
faces = []
i = 0
while True:
    buf = proc.stdout.read(W * H * 3)
    if len(buf) < W * H * 3 or i >= N:
        break
    fr = np.frombuffer(buf, np.uint8).reshape(H, W, 3)
    img = mp.Image(image_format=mp.ImageFormat.SRGB, data=np.ascontiguousarray(fr))
    ts = int(i * 1000 / FPS)
    r = fd.detect_for_video(img, ts)
    if r.detections:
        b = max(r.detections, key=lambda d: d.bounding_box.width).bounding_box
        faces.append([b.origin_x + b.width / 2, b.origin_y + b.height / 2, b.width, b.height])
    else:
        faces.append(None)
    s = seg.segment_for_video(img, ts)
    bg = s.confidence_masks[0].numpy_view()  # background confidence
    person = 1.0 - bg
    m = cv2.resize(person, (360, 640), interpolation=cv2.INTER_LINEAR)
    masks[i] = np.clip(m * 255, 0, 255).astype(np.uint8)
    i += 1
masks.flush()
print("frames", i)

# fill gaps + smooth face track (0.3 s window, centred)
arr = np.array([f if f else [np.nan] * 4 for f in faces], float)
for c in range(4):
    v = arr[:, c]; idx = np.arange(len(v)); ok = ~np.isnan(v)
    arr[:, c] = np.interp(idx, idx[ok], v[ok])
k = 9
ker = np.ones(k) / k
sm = np.stack([np.convolve(np.pad(arr[:, c], k // 2, mode="edge"), ker, "valid") for c in range(4)], 1)
json.dump({"n": i, "faces": sm.round(1).tolist(), "detected": [f is not None for f in faces]},
          open(f"{OUT}/faces.json", "w"))
print("face detected ratio", np.mean([f is not None for f in faces]))
