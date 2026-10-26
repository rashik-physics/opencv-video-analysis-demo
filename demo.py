"""Synthetic-only video illumination analysis portfolio demonstration."""
from pathlib import Path
import argparse
import csv
import cv2
import numpy as np


def make_synthetic_video(path: Path, fps: int = 25, seconds: int = 8, size=(320, 240)):
    """Create artificial frames with known periodic illumination and a moving shape."""
    path.parent.mkdir(parents=True, exist_ok=True)
    writer = cv2.VideoWriter(str(path), cv2.VideoWriter_fourcc(*'mp4v'), fps, size)
    if not writer.isOpened():
        raise RuntimeError('MP4 writer unavailable: check OpenCV/video codecs')
    width, height = size
    for i in range(fps * seconds):
        t = i / fps
        level = int(round(110 + 22 * np.sin(2 * np.pi * 0.35 * t)))
        frame = np.full((height, width, 3), level, dtype=np.uint8)
        cx = int(width / 2 + 22 * np.sin(2 * np.pi * 0.25 * t))
        cv2.circle(frame, (cx, height // 2), 24, (50, 160, 220), -1)
        writer.write(frame)
    writer.release()
    return fps * seconds


def analyze_video(video: Path, output: Path, roi=(30, 30, 290, 210)):
    """Measure mean Y (YCrCb) luminance in a fixed rectangular ROI, per frame."""
    cap = cv2.VideoCapture(str(video))
    if not cap.isOpened():
        raise FileNotFoundError(f'Cannot open video: {video}')
    fps = float(cap.get(cv2.CAP_PROP_FPS))
    if fps <= 0:
        cap.release()
        raise ValueError('Video does not report valid FPS')
    x1, y1, x2, y2 = roi
    measurements = []
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        height, width = frame.shape[:2]
        if not (0 <= x1 < x2 <= width and 0 <= y1 < y2 <= height):
            cap.release()
            raise ValueError(f'ROI {roi} outside {width}x{height} video')
        crop = frame[y1:y2, x1:x2]
        y = cv2.cvtColor(crop, cv2.COLOR_BGR2YCrCb)[:, :, 0]
        measurements.append(float(np.mean(y)))
    cap.release()
    if not measurements:
        raise ValueError('No frames decoded')
    output.mkdir(parents=True, exist_ok=True)
    with (output / 'brightness_timeseries.csv').open('w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['frame_index', 'time_seconds', 'mean_y_0_255'])
        writer.writerows((i, round(i / fps, 6), round(v, 4)) for i, v in enumerate(measurements))
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    times = np.arange(len(measurements)) / fps
    fig, ax = plt.subplots(figsize=(9, 3.5))
    ax.plot(times, measurements)
    ax.set(xlabel='Time (s)', ylabel='Mean Y luminance (0–255)', title='Synthetic-video ROI brightness')
    fig.tight_layout()
    fig.savefig(output / 'brightness_plot.png', dpi=150)
    plt.close(fig)
    return {'frames': len(measurements), 'fps': fps,
            'mean_y': float(np.mean(measurements)),
            'temporal_sd_y': float(np.std(measurements))}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=Path('outputs'))
    parser.add_argument('--roi', nargs=4, type=int, default=[30, 30, 290, 210],
                        metavar=('X1', 'Y1', 'X2', 'Y2'))
    args = parser.parse_args()
    video = args.output / 'synthetic_video.mp4'
    make_synthetic_video(video)
    summary = analyze_video(video, args.output, tuple(args.roi))
    print('Analysis complete:', summary)
    print('Outputs:', args.output.resolve())


if __name__ == '__main__':
    main()
