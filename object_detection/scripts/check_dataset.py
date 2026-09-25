from pathlib import Path

# Path to the raw image dataset
RAW_DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"

# Image formats that we accept
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png"}


def count_images(folder: Path) -> int:
    """Count image files inside a folder."""
    return sum(
        1
        for file in folder.iterdir()
        if file.is_file() and file.suffix.lower() in IMAGE_EXTENSIONS
    )


def main():
    print("HMS NEMO - Raw Dataset Check")
    print("-" * 35)

    if not RAW_DATA_DIR.exists():
        print(f"ERROR: Dataset folder not found: {RAW_DATA_DIR}")
        return

    total_images = 0

    for class_folder in sorted(RAW_DATA_DIR.iterdir()):
        if not class_folder.is_dir():
            continue

        number_of_images = count_images(class_folder)
        total_images += number_of_images

        print(f"{class_folder.name}: {number_of_images} images")

    print("-" * 35)
    print(f"Total: {total_images} images")


if __name__ == "__main__":
    main()