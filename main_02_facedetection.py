import cv2

from facedetection.camera import Camera


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
    cam = Camera(device="/dev/video2", resolution=(640, 480))
    detector = cv2.CascadeClassifier(
        "facedetection/haarcascade_frontalface_default.xml"
    )

    key_pressed = 0

    while not window_closed(WINDOW_TITLE) and key_pressed != ESC:
        has_frame, cam_img = cam.read()

        if not has_frame:
            continue

        result = detector.detectMultiScale(cam_img)

        for dims in result:
            x, y, w, h = dims
            cv2.rectangle(cam_img, (x, y), (x + w, y + h), (0, 255, 0), 2)

        cv2.imshow(WINDOW_TITLE, cam_img)
        key_pressed = cv2.waitKey(1)

    cv2.destroyAllWindows()
    cam.release()


if __name__ == "__main__":
    print("Running...")
    main()
