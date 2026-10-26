# OpenCV Video Illumination Analysis — Synthetic Demo

A small, reproducible **educational** Python portfolio project by Mohammad Rashik Zaman. Demonstrates frame-by-frame video processing, fixed rectangular region-of-interest (ROI) selection, illumination statistics, CSV export, and plotting.

**No clinical data, pediatric recordings, original research code, or unpublished research results are included.** All video content is generated artificially by `demo.py`. This demonstration is independent of and does not represent a validated physiological measurement system.

## What this demo does

1. Creates an 8-second, 25 FPS synthetic MP4 with sinusoidally changing brightness and an animated circle.
2. Reads each frame with OpenCV and crops a fixed ROI (coordinates `x1 y1 x2 y2`, exclusive upper bounds).
3. Converts BGR to YCrCb, then computes the **mean Y-channel pixel value** in the ROI (0–255).
4. Saves per-frame measurements to `brightness_timeseries.csv` and a graph to `brightness_plot.png`.
5. Reports frame count, FPS, mean Y, and temporal standard deviation of ROI mean Y.

This is a demonstration of **brightness analysis, not respiratory-rate estimation**. Periodic variations are programmed into the synthetic video and should not be interpreted as physiological signals. Mean Y is a convenient luminance-like digital channel, not an absolute photometric brightness calibration.

## Quick start

Requires Python 3.10+ and MP4 encoding/decoding supported by the installed OpenCV build.

```bash
python -m pip install -r requirements.txt
python demo.py
```

Results are written to `outputs/` (ignored by Git). To specify another rectangular ROI:

```bash
python demo.py --roi 40 40 280 200
```

Run tests:

```bash
python -m pytest -q
```

## Repository structure

```text
README.md
requirements.txt
demo.py
tests/test_demo.py
.gitignore
```

## Limitations and next steps

- ROI is fixed and does not track object movement.
- Video compression can slightly change the measured pixel values.
- Illumination changes and object movement both affect ROI measurements.
- No respiratory rate, heart rate, or health interpretation is produced.

Potential independently developed extensions include interactive ROI selection, ROI tracking, robust statistics, and comparison of illumination channels—using synthetic or appropriately licensed data only.

## Research context

My broader academic interests include non-contact physiological monitoring, biomedical imaging, and computer vision. This public-facing demonstration is intentionally separate from my ongoing supervised work at the University of Dhaka. Publication of research datasets or project-specific methods would require appropriate authorization.
