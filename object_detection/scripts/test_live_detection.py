import cv2
import time

from src.camera import Camera
from src.yolo_detector import YOLODetector
from src.position_estimator import PositionEstimator


def main():
    camera = Camera(camera_index=1)

    detector = YOLODetector(
        model_path="models/buoy_red_green_v1.pt",
        confidence_threshold=0.5
    )
    estimator = PositionEstimator()

    try:
        camera.open()

        print("Camera opened.")
        print("Live detection started.")
        print("Press Q to quit.")

        while True:
            last_print_time = 0
            frame = camera.read()

            detections = detector.detect(frame)
            current_time = time.time()
            should_print = current_time - last_print_time >= 1.0

            if should_print:
                last_print_time = current_time

            for detection in detections:
                x_min, y_min, x_max, y_max = detection.bbox

                center_x, center_y = estimator.get_center(detection)

                normalized_x = estimator.get_normalized_x(
                    detection,
                    frame.shape[1]
                )

                position = estimator.get_horizontal_position(
                    detection,
                    frame.shape[1]
                )

                bearing = estimator.get_bearing(detection, frame.shape[1])

                if should_print:
                    print(
                        f"Object: {detection.class_name} | "
                        f"Confidence: {detection.confidence:.2f} | "
                        f"Position: {position} | "
                        f"X: {normalized_x:.2f} | "
                        f"Bearing: {bearing:+.1f} deg"
                    )

                # Draw bounding box
                cv2.rectangle(
                    frame,
                    (x_min, y_min),
                    (x_max, y_max),
                    (0, 255, 0),
                    2
                )

                # Class name + confidence
                label = f"{detection.class_name} {bearing:+.1f} deg"
                
                text_size, _ = cv2.getTextSize(
                    label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2
                )

                text_width = text_size[0]

                text_x = max(0, min(x_min, frame.shape[1] - text_width - 5))
                text_y = max(y_min - 10, 20)

                cv2.putText(
                    frame,
                    label,
                    (text_x, text_y),
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