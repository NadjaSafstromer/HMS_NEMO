
from pathlib import Path
import shutil

# Project directory
PROJECT_DIR = Path(__file__).resolve().parents[1]

# Original images and annotations
SOURCE_DIR = PROJECT_DIR / "data" / "Buoy_Pictures"

SOURCE_IMAGES = SOURCE_DIR / "All_buoys"
SOURCE_LABELS = SOURCE_DIR / "Annotations_all_buoys"

# Dataset inside the project
DATASET_DIR = PROJECT_DIR / "data" / "dataset"

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png"}

# Exact duplicate, excluded without deleting the original
EXCLUDED_IMAGES = {"20230613_130501(1)"}

CLASS_NAMES = {
    0: "green_buoy",
    1: "red_buoy",
}


def get_split(filename: str) -> str:
    """Assign image series to training or validation."""

    if filename.startswith(("20230611_", "20230613_")):
        return "train"

    if filename.startswith("IMG_"):
        return "val"

    raise ValueError(f"Unknown image series: {filename}")


def main():
    counts = {
        "train": {0: 0, 1: 0},
        "val": {0: 0, 1: 0},
    }

    image_counts = {"train": 0, "val": 0}

    if not SOURCE_IMAGES.is_dir() or not SOURCE_LABELS.is_dir():
        raise FileNotFoundError("Source image or annotation folder not found.")

    # Validate all inputs before copying anything
    samples = []

    for image_path in sorted(SOURCE_IMAGES.iterdir()):
        if image_path.suffix.lower() not in IMAGE_EXTENSIONS:
            continue

        if image_path.stem in EXCLUDED_IMAGES:
            continue

        label_path = SOURCE_LABELS / f"{image_path.stem}.txt"

        if not label_path.is_file():
            raise FileNotFoundError(f"Missing annotation: {label_path}")

        split = get_split(image_path.name)
        class_ids = []

        for line in label_path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue

            values = line.split()

            if len(values) != 5:
                raise ValueError(f"Invalid YOLO label: {label_path}")

            class_id = int(values[0])

            if class_id not in CLASS_NAMES:
                raise ValueError(f"Unknown class {class_id}: {label_path}")

            class_ids.append(class_id)

        samples.append((image_path, label_path, split, class_ids))

    # Avoid accidentally mixing an old dataset with the new one
    for split in ("train", "val"):
        for folder in ("images", "labels"):
            destination = DATASET_DIR / folder / split
            destination.mkdir(parents=True, exist_ok=True)

            if any(destination.iterdir()):
                raise RuntimeError(
                    f"Destination is not empty: {destination}"
                )

    # Copy images and matching annotations
    for image_path, label_path, split, class_ids in samples:
        image_dest = DATASET_DIR / "images" / split
        label_dest = DATASET_DIR / "labels" / split

        shutil.copy2(image_path, image_dest / image_path.name)
        shutil.copy2(label_path, label_dest / label_path.name)

        image_counts[split] += 1

        for class_id in class_ids:
            counts[split][class_id] += 1

    print("\nDataset prepared successfully!")

    for split in ("train", "val"):
        print(f"\n{split.upper()}")
        print(f"Images: {image_counts[split]}")

        for class_id, class_name in CLASS_NAMES.items():
            print(f"{class_name}: {counts[split][class_id]} annotations")

    print(f"\nTotal images: {sum(image_counts.values())}")
    print("Original files were not modified.")


if __name__ == "__main__":
    main()
