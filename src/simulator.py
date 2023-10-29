import math
import os

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import cv2
import numpy as np
import pygame

from src.vision import process_frame


def _track_points(width=800, height=600, frames=300):
    """Generate track centerline points matching generate_track.py path logic."""
    points = []
    for i in range(frames):
        t = i / frames
        x = int(width / 2 + (width / 3) * math.sin(2 * math.pi * t * 2))
        y = int(height * i / frames)
        points.append((x, y))
    return points


class Simulator:
    def __init__(self, width=800, height=600):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Line Follower Simulator")
        self.font = pygame.font.SysFont("monospace", 18)
        self.clock = pygame.time.Clock()
        self.track_points = _track_points(width, height)

    def draw_track(self, track_points):
        self.screen.fill((30, 30, 30))
        if len(track_points) > 1:
            pygame.draw.lines(self.screen, (200, 200, 200), False, track_points, 3)

    def draw_robot(self, x, y):
        pygame.draw.circle(self.screen, (0, 200, 100), (int(x), int(y)), 12)

    def draw_hud(self, direction, magnitude, confidence):
        texts = [
            f"direction : {direction}",
            f"magnitude : {magnitude:.1f}",
            f"confidence: {confidence:.3f}",
        ]
        for i, t in enumerate(texts):
            surf = self.font.render(t, True, (255, 255, 255))
            self.screen.blit(surf, (10, 10 + i * 22))

    def update(self):
        pygame.display.flip()
        self.clock.tick(30)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                return False
        return True

    def run(self, video_path, controller):
        cap = cv2.VideoCapture(video_path)
        frame_w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        center_x = frame_w // 2

        robot_x = self.width // 2
        robot_y = 50
        speed = self.height / int(cap.get(cv2.CAP_PROP_FRAME_COUNT) or 300)

        frame_idx = 0
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            line_x, confidence = process_frame(frame)
            if line_x is not None:
                direction, magnitude = controller.update(line_x, center_x)
                if direction == "left":
                    robot_x -= magnitude * 0.1
                elif direction == "right":
                    robot_x += magnitude * 0.1
            else:
                direction, magnitude = "straight", 0.0

            robot_x = max(0, min(self.width, robot_x))
            robot_y = min(self.height - 20, 50 + frame_idx * speed)

            self.draw_track(self.track_points)
            self.draw_robot(robot_x, robot_y)
            self.draw_hud(direction, magnitude, confidence if line_x else 0.0)
            self.update()

            if not self.handle_events():
                break
            frame_idx += 1

        cap.release()

    def quit(self):
        pygame.quit()
