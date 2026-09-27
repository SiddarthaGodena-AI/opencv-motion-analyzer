# Validation record

On 27 September 2026, all three offline tests passed locally and on GitHub Actions.

The reproducible synthetic demo contains 90 frames with a moving white rectangle against a stationary black background. The analyzer reported:

```json
{"frames": 90, "moving_frames": 46, "motion_events": 1}
```

Run `python demo.py` to recreate the MJPG video and JSON. This is a functional demonstration, not a benchmark on real surveillance footage. Object counting, tracking, and classification are outside this project's scope.
