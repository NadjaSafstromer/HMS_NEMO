import cv2


def main():
    camera = cv2.VideoCapture(1)

    if not camera.isOpened():
        print("ERROR: Could not open camera.")
        return

    print("Camera opened.")
    print(
        f"Resolution: "
        f"{int(camera.get(cv2.CAP_PROP_FRAME_WIDTH))} x "
        f"{int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT))}"
    )
    print(f"FPS: {camera.get(cv2.CAP_PROP_FPS)}")
    print("Press Q to quit.")

    while True:
        success, frame = camera.read()

        if not success:
            print("ERROR: Could not read frame.")
            break

        display_frame = cv2.resize(frame, (960, 480))
        cv2.imshow("HMS NEMO - THETA X", display_frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    camera.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()