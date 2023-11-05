import argparse
import csv
import os
import time

import cv2

from src.controller import Controller
from src.vision import process_frame


def main():
    parser = argparse.ArgumentParser(description="RPi Line Follower")
    parser.add_argument("--video", default="tracks/track1.mp4", help="Path to video file")
    parser.add_argument("--simulate", action="store_true", help="Enable Pygame visualization")
    parser.add_argument("--log", default=None, help="CSV output path")
    parser.add_argument("--kp", type=float, default=0.5, help="Proportional gain")
    args = parser.parse_args()

    controller = Controller(kp=args.kp)
    sim = None

    if args.simulate:
        os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
        os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
        from src.simulator import Simulator
        sim = Simulator()

    cap = cv2.VideoCapture(args.video)
    if not cap.isOpened():
        print(f"Error: cannot open {args.video}")
        return

    frame_w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    center_x = frame_w // 2

    csv_file = None
    writer = None
    if args.log:
        csv_file = open(args.log, "w", newline="")
        writer = csv.writer(csv_file)
        writer.writerow(["timestamp", "frame_number", "line_x", "confidence", "steering_direction", "steering_magnitude"])

    frame_idx = 0
    robot_x = 400

    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            line_x, confidence = process_frame(frame)
            if line_x is not None:
                direction, magnitude = controller.update(line_x, center_x)
            else:
                direction, magnitude = "straight", 0.0

            if writer:
                writer.writerow([
                    time.strftime("%Y-%m-%dT%H:%M:%S"),
                    frame_idx,
                    line_x if line_x is not None else "",
                    confidence,
                    direction,
                    magnitude,
                ])

            if sim:
                if direction == "left":
                    robot_x -= magnitude * 0.1
                elif direction == "right":
                    robot_x += magnitude * 0.1
                robot_x = max(0, min(sim.width, robot_x))
                robot_y = min(sim.height - 20, 50 + frame_idx * (sim.height / 300))
                sim.draw_track(sim.track_points)
                sim.draw_robot(robot_x, robot_y)
                sim.draw_hud(direction, magnitude, confidence)
                sim.update()
                if not sim.handle_events():
                    break

            frame_idx += 1

    finally:
        cap.release()
        if csv_file:
            csv_file.close()
        if sim:
            sim.quit()

    print(f"Done. Processed {frame_idx} frames.")


if __name__ == "__main__":
    main()
