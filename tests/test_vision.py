import numpy as np
import pytest
from src.vision import process_frame


def make_frame_with_line(width=640, height=480, line_x=320, line_width=15):
    """White frame with a vertical black line at line_x."""
    frame = np.ones((height, width, 3), dtype=np.uint8) * 255
    frame[:, max(0, line_x - line_width // 2):line_x + line_width // 2 + 1] = 0
    return frame


def test_detects_line_at_known_position():
    expected_x = 300
    frame = make_frame_with_line(line_x=expected_x)
    detected_x, confidence = process_frame(frame)
    assert detected_x is not None
    assert abs(detected_x - expected_x) <= 10
    assert 0.0 < confidence <= 1.0


def test_detects_line_at_left():
    frame = make_frame_with_line(line_x=100)
    detected_x, _ = process_frame(frame)
    assert detected_x is not None
    assert abs(detected_x - 100) <= 10


def test_blank_white_frame_returns_none():
    frame = np.ones((480, 640, 3), dtype=np.uint8) * 255
    detected_x, confidence = process_frame(frame)
    assert detected_x is None
    assert confidence == 0.0
