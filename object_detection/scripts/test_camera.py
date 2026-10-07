import cv2

from src.camera import Camera


def main():
    camera = Camera(camera_index=1)

    try:
        camera.open()
        print("Camera opened.")
        print("Press Q to quit.")

        while True:
            frame = camera.read()

            # Smaller image for display only
            display_frame = cv2.resize(
                frame,
                (960, 480)
            )

            cv2.imshow(
                "HMS NEMO - THETA X",
                display_frame
            )

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    finally:
        camera.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()