class Controller:
    def __init__(self, kp=0.5, threshold=5.0):
        self.kp = kp
        self.threshold = threshold

    def update(self, line_x, frame_center_x):
        """
        Returns (direction, magnitude) based on line position relative to center.
        direction: "left", "right", or "straight"
        magnitude: abs(kp * error)
        """
        error = line_x - frame_center_x
        magnitude = abs(self.kp * error)

        if magnitude < self.threshold:
            return "straight", 0.0
        elif error > 0:
            return "right", round(magnitude, 2)
        else:
            return "left", round(magnitude, 2)
