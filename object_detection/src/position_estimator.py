
import math

from src.detected_object import DetectedObject


class PositionEstimator:
    """
    Estimates object positions relative to the camera image.
    """

    def get_center(self, detection: DetectedObject):
        """Calculate the bounding box center in pixels."""
        x_min, y_min, x_max, y_max = detection.bbox

        center_x = (x_min + x_max) / 2
        center_y = (y_min + y_max) / 2

        return center_x, center_y

    def get_normalized_x(
        self,
        detection: DetectedObject,
        frame_width: int
    ):
        """Calculate horizontal position between 0 and 1."""
        if frame_width <= 0:
            raise ValueError("Frame width must be positive.")

        center_x, _ = self.get_center(detection)

        return center_x / frame_width

    def get_horizontal_position(
        self,
        detection: DetectedObject,
        frame_width: int
    ):
        """Classify object position as LEFT, CENTER or RIGHT."""
        normalized_x = self.get_normalized_x(
            detection,
            frame_width
        )

        if normalized_x < 1 / 3:
            return "LEFT"

        if normalized_x > 2 / 3:
            return "RIGHT"

        return "CENTER"

    def get_bearing(
        self,
        detection: DetectedObject,
        frame_width: int,
        horizontal_fov: float = 96.0
    ) -> float:
        """
        Estimate horizontal bearing relative to the camera.

        Negative = left
        Zero = center
        Positive = right

        horizontal_fov is in degrees.
        """
        if frame_width <= 0:
            raise ValueError("Frame width must be positive.")

        if not 0 < horizontal_fov < 180:
            raise ValueError(
                "Horizontal FOV must be between 0 and 180 degrees."
            )

        center_x, _ = self.get_center(detection)

        focal_length_px = (
            frame_width
            / (2 * math.tan(math.radians(horizontal_fov / 2)))
        )

        offset_x = center_x - frame_width / 2

        bearing_rad = math.atan2(
            offset_x,
            focal_length_px
        )

        return math.degrees(bearing_rad)
    
    
    
