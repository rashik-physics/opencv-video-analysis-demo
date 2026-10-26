from pathlib import Path
import pytest
from demo import make_synthetic_video, analyze_video


def test_synthetic_pipeline(tmp_path: Path):
    movie = tmp_path / 'demo.mp4'
    count = make_synthetic_video(movie, fps=10, seconds=2)
    summary = analyze_video(movie, tmp_path / 'results', roi=(10, 10, 300, 230))
    assert count == 20
    assert summary['frames'] == 20
    assert 0 <= summary['mean_y'] <= 255
    assert summary['temporal_sd_y'] > 0
    assert (tmp_path / 'results' / 'brightness_timeseries.csv').exists()
    assert (tmp_path / 'results' / 'brightness_plot.png').exists()


def test_invalid_roi(tmp_path: Path):
    movie = tmp_path / 'demo.mp4'
    make_synthetic_video(movie, fps=5, seconds=1)
    with pytest.raises(ValueError, match='ROI'):
        analyze_video(movie, tmp_path / 'results', roi=(10, 10, 500, 230))
