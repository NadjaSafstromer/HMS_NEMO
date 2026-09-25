from pathlib import Path
from typing import List
import time

from ultralytics import YOLO

from src.detector import Detector
from src.detected_object import DetectedObject


class YOLODetector(Detector):
    """
    Object detector using an Ultralytics YOLO model.
    """

    def __init__(self, model_path: str, confidence_threshold: float = 0.5):
        self.model = YOLO(model_path)
        self.confidence_threshold = confidence_threshold

    def detect(self, image_path: Path) -> List[DetectedObject]:
        """
        Run object detection on one image.
        """

        results = self.model(
            str(image_path),
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