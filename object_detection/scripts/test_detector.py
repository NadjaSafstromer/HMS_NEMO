from pathlib import Path

from src.yolo_detector import YOLODetector


def main():
    # Pretrained YOLO model
    detector = YOLODetector(
        model_path="yolo11n.pt",
        confidence_threshold=0.5
    )

    # Choose one image from our raw dataset
    image_path = Path("data/raw/red_buoy/IMG_1039.JPG")

    detections = detector.detect(image_path)

    print(f"\nImage: {image_path}")
    print(f"Number of detections: {len(detections)}")

    for detection in detections:
        print(detection)


if __name__ == "__main__":
    main()