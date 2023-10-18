import cv2
import numpy as np


def process_frame(frame):
    """
    Detect line position in a frame.

    Returns (line_x, confidence) where:
      - line_x: horizontal centroid of the detected line (int)
      - confidence: contour area / frame area (float 0-1)
    Returns (None, 0.0) if no line detected.
    """
    h, w = frame.shape[:2]
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blurred, 127, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if not contours:
        return None, 0.0

    largest = max(contours, key=cv2.contourArea)
    area = cv2.contourArea(largest)
    if area < 100:
        return None, 0.0

    M = cv2.moments(largest)
    if M["m00"] == 0:
        return None, 0.0

    line_x = int(M["m10"] / M["m00"])
    confidence = round(area / (h * w), 4)
    return line_x, confidence
