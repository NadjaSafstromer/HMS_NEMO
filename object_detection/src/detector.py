from abc import ABC, abstractmethod
from typing import List

import numpy as np

from src.detected_object import DetectedObject


class Detector(ABC):
    """
    Base interface for object detectors used in HMS NEMO.
    """

    @abstractmethod
    def detect(self, frame: np.ndarray) -> List[DetectedObject]:
        """
        Detect objects in an image frame and return the detections.
        """
        pass