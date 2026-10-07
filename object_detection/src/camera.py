import cv2


class Camera:
    """
    Handles camera capture for the HMS NEMO perception system.
    """

    def __init__(self, camera_index: int = 1):
        self.camera_index = camera_index
        self.capture = None

    def open(self):
        """Open the camera."""
        self.capture = cv2.VideoCapture(self.camera_index)

        if not self.capture.isOpened():
            raise RuntimeError(
                f"Could not open camera with index {self.camera_index}"
            )

    def read(self):
        """Read one frame from the camera."""
        if self.capture is None:
            raise RuntimeError("Camera is not open.")

        success, frame = self.capture.read()

        if not success:
            raise RuntimeError("Could not read frame from camera.")

        return frame

    def release(self):
        """Release the camera."""
        if self.capture is not None:
            self.capture.release()
            self.capture = None