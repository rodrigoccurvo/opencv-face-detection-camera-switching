import cv2


def window_closed(window_title):
    try:
        window_closed = not cv2.getWindowProperty(
            window_title, cv2.WND_PROP_VISIBLE
        )
    except cv2.error:
        window_closed = False

    return window_closed


WINDOW_TITLE = "Preview"
ESC = 27


def main():
    device = "/dev/video2"
    cam = cv2.VideoCapture(device)

    if not cam.isOpened():
        raise SystemExit(f"Unable to open {device}")

    width, height = 640, 480
    cam.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    key_pressed = 0

    while not window_closed(WINDOW_TITLE) and key_pressed != ESC:
        has_frame, cam_img = cam.read()

        if not has_frame:
            continue

        cv2.imshow(WINDOW_TITLE, cam_img)
        key_pressed = cv2.waitKey(1)

    cv2.destroyAllWindows()
    cam.release()


if __name__ == "__main__":
    print("Running...")
    main()
