from pathlib import Path
import random
import shutil


DATASET_DIR = Path("data/dataset")

IMAGE_DIR = DATASET_DIR / "images"
LABEL_DIR = DATASET_DIR / "labels"

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png"}

TRAIN_RATIO = 0.8
RANDOM_SEED = 42


def get_class_id(label_path: Path) -> int:
    """Read class ID from a YOLO label file."""
    with open(label_path, "r") as file:
        line = file.readline().strip()

    return int(line.split()[0])


def main():
    random.seed(RANDOM_SEED)

    # Find all image/label pairs
    samples_by_class = {}

    for image_path in IMAGE_DIR.iterdir():

        if image_path.suffix.lower() not in IMAGE_EXTENSIONS:
            continue

        label_path = LABEL_DIR / f"{image_path.stem}.txt"

        if not label_path.exists():
            print(f"WARNING: Missing label for {image_path.name}")
            continue

        class_id = get_class_id(label_path)

        samples_by_class.setdefault(class_id, []).append(
            (image_path, label_path)
        )

    # Create output folders
    for split in ["train", "val"]:
        (IMAGE_DIR / split).mkdir(exist_ok=True)
        (LABEL_DIR / split).mkdir(exist_ok=True)

    total_train = 0
    total_val = 0

    # Split each class separately
    for class_id, samples in samples_by_class.items():

        random.shuffle(samples)

        split_index = int(len(samples) * TRAIN_RATIO)

        train_samples = samples[:split_index]
        val_samples = samples[split_index:]

        print(
            f"Class {class_id}: "
            f"{len(train_samples)} train, "
            f"{len(val_samples)} val"
        )

        for image_path, label_path in train_samples:
            shutil.copy2(
                image_path,
                IMAGE_DIR / "train" / image_path.name
            )

            shutil.copy2(
                label_path,
                LABEL_DIR / "train" / label_path.name
            )

        for image_path, label_path in val_samples:
            shutil.copy2(
                image_path,
                IMAGE_DIR / "val" / image_path.name
            )

            shutil.copy2(
                label_path,
                LABEL_DIR / "val" / label_path.name
            )

        total_train += len(train_samples)
        total_val += len(val_samples)

    print("-" * 35)
    print(f"Train: {total_train} images")
    print(f"Validation: {total_val} images")
    print(f"Total: {total_train + total_val} images")


if __name__ == "__main__":
    main()