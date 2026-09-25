from dataclasses import dataclass
from typing import Optional, Tuple


@dataclass
class DetectedObject:
    """
    Represents one object detected by the perception system.
    """

    class_id: int
    class_name: str
    confidence: float

    # Bounding box: (x_min, y_min, x_max, y_max)
    bbox: Tuple[int, int, int, int]

    # Time when the detection was made
    timestamp: float

    # Optional information added later in the perception pipeline
    track_id: Optional[int] = None
    bearing: Optional[float] = None
    distance: Optional[float] = None