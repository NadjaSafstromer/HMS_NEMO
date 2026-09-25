from pathlib import Path

import cv2


IMAGE_DIR = Path("data/dataset/images")
LABEL_DIR = Path("data/dataset/labels")

CLASS_NAMES = {
    0: "red_buoy",
    1: "green_buoy",
}

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png"}


def draw_annotations(image_path: Path):
    """Load one image and draw its YOLO annotations."""

    label_path = LABEL_DIR / f"{image_path.stem}.txt"

    if not label_path.exists():
        print(f"WARNING: No label found for {image_path.name}")
        return None

    image = cv2.imread(str(image_path))

    if image is None:
        print(f"ERROR: Could not open {image_path}")
        return None

    height, width = image.shape[:2]

    with open(label_path, "r") as file:
        for line in file:
            values = line.strip().split()

            if len(values) != 5:
                print(f"WARNING: Invalid annotation in {label_path.name}")
                continue

            class_id = int(values[0])
            x_center = float(values[1])
            y_center = float(values[2])
            box_width = float(values[3])
            box_height = float(values[4])

            # Convert YOLO coordinates to pixel coordinates
            x_center *= width
            y_center *= height
            box_width *= width
            box_height *= height

            x_min = int(x_center - box_width / 2)
            y_min = int(y_center - box_height / 2)
            x_max = int(x_center + box_width / 2)
            y_max = int(y_center + box_height / 2)

            class_name = CLASS_NAMES.get(
                class_id,
                f"class_{class_id}"
            )

            cv2.rectangle(
                image,
                (x_min, y_min),
                (x_max, y_max),
                (0, 255, 0),
                8
            )

            cv2.putText(
                image,
                class_name,
                (x_min, max(y_min - 15, 30)),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.0,
                (0, 255, 0),
                3
            )

    return image


def resize_for_display(image):
    """Resize image so it fits on the screen."""

    max_width = 1200
    max_height = 800

    height, width = image.shape[:2]

    scale = min(
        max_width / width,
        max_height / height,
        1.0
    )

    display_width = int(width * scale)
    display_height = int(height * scale)

    return cv2.resize(
        image,
        (display_width, display_height)
    )


def main():
    image_paths = sorted(
        image
        for image in IMAGE_DIR.iterdir()
        if image.suffix.lower() in IMAGE_EXTENSIONS
    )

    print(f"Found {len(image_paths)} images.")
    print("SPACE = next image")
    print("Q = quit")

    for image_path in image_paths:

        image = draw_annotations(image_path)

        if image is None:
            continue

        display_image = resize_for_display(image)

        cv2.imshow(
            f"HMS NEMO - {image_path.name}",
            display_image
        )

        print(f"Checking: {image_path.name}")

        # Wait until a key is pressed
        key = cv2.waitKey(0) & 0xFF

        # Q = quit
        if key == ord("q"):
            break

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()