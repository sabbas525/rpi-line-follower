import math
import os

import cv2
import numpy as np

WIDTH, HEIGHT = 640, 480
FPS = 30
FRAMES = 300
LINE_WIDTH = 15
OUT_PATH = os.path.join(os.path.dirname(__file__), "track1.mp4")


def line_x_at(frame_idx):
    """S-curve path: sine wave oscillating across the frame width."""
    t = frame_idx / FRAMES
    return int(WIDTH / 2 + (WIDTH / 3) * math.sin(2 * math.pi * t * 2))


def main():
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    writer = cv2.VideoWriter(OUT_PATH, fourcc, FPS, (WIDTH, HEIGHT))

    for i in range(FRAMES):
        frame = np.ones((HEIGHT, WIDTH, 3), dtype=np.uint8) * 255
        cx = line_x_at(i)
        cv2.line(frame, (cx, 0), (cx, HEIGHT), (0, 0, 0), LINE_WIDTH)
        writer.write(frame)

    writer.release()
    print(f"Saved {FRAMES} frames to {OUT_PATH}")


if __name__ == "__main__":
    main()
