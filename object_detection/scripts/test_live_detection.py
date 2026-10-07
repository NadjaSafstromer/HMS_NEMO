import cv2

from src.camera import Camera
from src.yolo_detector import YOLODetector


def main():
    camera = Camera(camera_index=1)

    detector = YOLODetector(
        model_path="../runs/detect/red_buoy_v1/weights/best.pt",
        confidence_threshold=0.5
    )

    try:
        camera.open()

        print("Camera opened.")
        print("Live detection started.")
        print("Press Q to quit.")

        while True:
            frame = camera.read()

            detections = detector.detect(frame)

            for detection in detections:
                x_min, y_min, x_max, y_max = detection.bbox

                # Draw bounding box
                cv2.rectangle(
                    frame,
                    (x_min, y_min),
                    (x_max, y_max),
                    (0, 255, 0),
                    2
                )

                # Class name + confidence
                label = (
                    f"{detection.class_name} "
                    f"{detection.confidence:.2f}"
                )

                cv2.putText(
                    frame,
                    label,
                    (x_min, max(y_min - 10, 20)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0, 255, 0),
                    2
                )

            # Smaller display only
            display_frame = cv2.resize(
                frame,
                (960, 480)
            )

            cv2.imshow(
                "HMS NEMO - Live Object Detection",
                display_frame
            )

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    finally:
        camera.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()