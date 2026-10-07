from typing import List
import time

import numpy as np
from ultralytics import YOLO

from src.detector import Detector
from src.detected_object import DetectedObject


class YOLODetector(Detector):
    """
    Object detector using an Ultralytics YOLO model.
    """

    def __init__(
        self,
        model_path: str,
        confidence_threshold: float = 0.5
    ):
        self.model = YOLO(model_path)
        self.confidence_threshold = confidence_threshold

    def detect(self, frame: np.ndarray) -> List[DetectedObject]:
        """
        Run object detection on one camera frame.
        """
        results = self.model(
            frame,
            conf=self.confidence_threshold,
            verbose=False
        )

        detections = []
        timestamp = time.time()

        for result in results:
            for box in result.boxes:
                class_id = int(box.cls.item())
                confidence = float(box.conf.item())

                x_min, y_min, x_max, y_max = map(
                    int,
                    box.xyxy[0].tolist()
                )

                detection = DetectedObject(
                    class_id=class_id,
                    class_name=self.model.names[class_id],
                    confidence=confidence,
                    bbox=(x_min, y_min, x_max, y_max),
                    timestamp=timestamp
                )

                detections.append(detection)

        return detections

    def detect_image(self, image_path: str) -> List[DetectedObject]:
        """
        Load an image from disk and run object detection.
        """
        import cv2

        frame = cv2.imread(image_path)

        if frame is None:
            raise ValueError(
                f"Could not load image: {image_path}"
            )

        return self.detect(frame)