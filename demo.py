"""Create synthetic motion footage and analyze it without private video."""
from pathlib import Path
import json
import cv2
import numpy as np
from motion import analyze_frames

def main():
    out = Path("outputs")
    out.mkdir(exist_ok=True)
    frames = []
    for i in range(90):
        frame = np.zeros((240,320,3), np.uint8)
        if 15 <= i < 60:
            x = 20 + (i-15)*4
            cv2.rectangle(frame, (x,80), (x+40,130), (255,255,255), -1)
        frames.append(frame)
    writer = cv2.VideoWriter(str(out/"motion-demo.avi"), cv2.VideoWriter_fourcc(*"MJPG"), 15, (320,240))
    if not writer.isOpened():
        raise RuntimeError("MJPG video encoder unavailable")
    try:
        for frame in frames:
            writer.write(frame)
    finally:
        writer.release()
    result = analyze_frames(frames, min_area=100)
    (out/"summary.json").write_text(json.dumps(result,indent=2), encoding="utf-8")
    print(result)

if __name__ == "__main__":
    main()
