from abc import ABC, abstractmethod
from pathlib import Path
from typing import List

from src.detected_object import DetectedObject


class Detector(ABC):
    """
    Base interface for object detectors used in HMS NEMO.

    A detector receives an image and returns detected objects.
    """

    @abstractmethod
    def detect(self, image_path: Path) -> List[DetectedObject]:
        """
        Detect objects in an image.

        Args:
            image_path: Path to the input image.

        Returns:
            List of detected objects.
        """
        pass