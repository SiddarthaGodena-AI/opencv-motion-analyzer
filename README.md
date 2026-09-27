# OpenCV Motion Event Analyzer

A lightweight CLI that analyzes a video and reports frames with motion and motion-event starts, without a neural model or cloud service.

## How it works

Consecutive frames are converted to grayscale and blurred. Absolute differences are thresholded and dilated. Contours above a configurable area mark motion. A transition from idle to moving starts an event.

## Run

Requires Python 3.12. Create and activate a virtual environment, then:

```bash
pip install -r requirements-dev.txt
python motion.py clip.mp4 --min-area 500 --output summary.json
python -m pytest -q
python demo.py
```

Output fields:

`python demo.py` creates a 90-frame synthetic MJPG video and JSON analysis under `outputs/`, without using private footage.

| Field | Meaning |
|---|---|
| frames | All readable video frames |
| moving_frames | Frames whose difference masks exceed the area threshold |
| motion_events | Idle-to-moving transitions |

## Tests and limitations

Tests cover static frames, a synthetic motion event, and empty input. Camera movement, lighting changes, compression noise, and reflections can trigger false positives. Slow motion may be missed. Events are not unique people or tracked objects; stationary objects produce no new motion. Use consented footage and retain results locally.

## Future improvements

Region-of-interest selection, debounce windows, background subtraction, event timestamps, and annotated video export.

## Resume-ready description

“Implemented an OpenCV video motion analyzer using frame differencing, contour filtering, event-state transitions, and offline tests.”

MIT licensed. No footage or personal data is included.
