"""Count motion events from video using consecutive-frame differences."""
import argparse
import json
from pathlib import Path
import cv2
import numpy as np

def analyze_frames(frames, min_area=500, threshold=25):
    previous = None
    active = False
    events, moving_frames, frame_count = 0, 0, 0
    for frame in frames:
        frame_count += 1
        gray = cv2.GaussianBlur(cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY),(5,5),0)
        if previous is not None:
            if gray.shape != previous.shape:
                raise ValueError("Frame dimensions changed")
            mask = cv2.threshold(cv2.absdiff(previous,gray),threshold,255,cv2.THRESH_BINARY)[1]
            mask = cv2.dilate(mask,None,iterations=2)
            contours,_ = cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
            moving = any(cv2.contourArea(c) >= min_area for c in contours)
            moving_frames += int(moving)
            if moving and not active:
                events += 1
            active = moving
        previous = gray
    return {"frames":frame_count,"moving_frames":moving_frames,"motion_events":events}

def video_frames(path):
    cap = cv2.VideoCapture(str(path))
    if not cap.isOpened():
        cap.release()
        raise ValueError("Video could not be opened")
    try:
        while True:
            ok,frame = cap.read()
            if not ok:
                break
            yield frame
    finally:
        cap.release()

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("video")
    parser.add_argument("--min-area",type=float,default=500)
    parser.add_argument("--output",default="motion-summary.json")
    args=parser.parse_args()
    if args.min_area <= 0:
        parser.error("min-area must be positive")
    try:
        result=analyze_frames(video_frames(args.video),args.min_area)
        if result["frames"] == 0:
            raise ValueError("Video contains no readable frames")
    except ValueError as error:
        parser.error(str(error))
    Path(args.output).write_text(json.dumps(result,indent=2),encoding="utf-8")
    print(json.dumps(result))

if __name__ == "__main__":
    main()

