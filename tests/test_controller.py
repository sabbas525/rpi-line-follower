from src.controller import Controller


def test_line_right_of_center():
    c = Controller(kp=0.5)
    direction, magnitude = c.update(line_x=400, frame_center_x=320)
    assert direction == "right"
    assert magnitude > 0


def test_line_left_of_center():
    c = Controller(kp=0.5)
    direction, magnitude = c.update(line_x=200, frame_center_x=320)
    assert direction == "left"
    assert magnitude > 0


def test_line_at_center_is_straight():
    c = Controller(kp=0.5)
    direction, magnitude = c.update(line_x=320, frame_center_x=320)
    assert direction == "straight"
    assert magnitude == 0.0


def test_magnitude_scales_with_error():
    c = Controller(kp=0.5)
    _, mag_small = c.update(line_x=340, frame_center_x=320)
    _, mag_large = c.update(line_x=420, frame_center_x=320)
    assert mag_large > mag_small
