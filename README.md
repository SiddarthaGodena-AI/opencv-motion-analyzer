# OpenCV Motion Event Analyzer

![Tests](https://github.com/SiddarthaGodena-AI/opencv-motion-analyzer/actions/workflows/tests.yml/badge.svg)
![Python](https://img.shields.io/badge/Python-3.12-blue)
![License](https://img.shields.io/badge/License-MIT-green)

This command-line tool reads a video and reports how many frames contain motion and how often a new motion event starts. It uses frame differences rather than a neural model, so there are no model weights to download.

It's best suited to a fixed camera. It detects changes in the image, not people, vehicles, or object identities.

## How it works

Each frame is converted to grayscale and blurred. The difference from the previous frame is thresholded, then dilated to join nearby changed pixels. Contour areas decide whether the frame is moving, and a small state check counts event starts.

## Run

Use Python 3.12. From the repository folder, create an environment with `python -m venv .venv`. Activate it with `.venv\Scripts\activate` on Windows or `source .venv/bin/activate` on Linux/macOS, then:

```bash
pip install -r requirements-dev.txt
python motion.py clip.mp4 --min-area 500 --output summary.json
python -m pytest -q
python demo.py
```

`--min-area` is the minimum contour area used to flag motion. Lower values pick up smaller changes but can also pick up more noise. The tool prints the summary and writes it to the output file.

If you don't have a video handy, run `python demo.py`. It creates a 90-frame video of a moving rectangle in `outputs/motion-demo.avi` and analyzes the generated frames. The result is saved to `outputs/summary.json`:

```json
{
  "frames": 90,
  "moving_frames": 46,
  "motion_events": 1
}
```

The demo uses a minimum contour area of 100; the CLI defaults to 500. Running the CLI on the saved video with its default settings isn't the same experiment. Neither result is a real-world performance benchmark.

| Field | Meaning |
|---|---|
| frames | All readable video frames, including the first reference frame |
| moving_frames | Frames whose difference masks exceed the area threshold |
| motion_events | Idle-to-moving transitions |

## Tests and limitations

Three offline tests cover static frames, a synthetic motion event, and empty input. The demo and test results are recorded in [VALIDATION.md](VALIDATION.md).

A continuous stretch of motion counts as one event. If motion stops and starts again, another event is counted. These aren't counts of unique people or objects.

Camera shake, lighting changes, reflections, and compression artifacts can all look like motion. Very slow movement may be missed, and stationary objects won't keep generating events. There is no debounce window yet, so intermittent noise can split one stretch into several events. Use footage you have permission to analyze.

## Future improvements

Region-of-interest selection and event timestamps would make the summaries more useful. A debounce setting would help avoid fragmented events; background subtraction and annotated video export are other possible extensions.

MIT licensed. No footage or personal data is included.
