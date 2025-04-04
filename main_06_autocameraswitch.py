import cv2

from facedetection.autocameraswitcher import AutoCameraSwitcher
from facedetection.multicameracached import MultiCameraCached


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
NUM_KEYS = {ord(str(i)) for i in range(1, 10)}


def main():
    multicam = MultiCameraCached(
        devices=["/dev/video2", "/dev/video0"], resolution=(640, 480)
    )
    camswitcher = AutoCameraSwitcher(multicam)

    key_pressed = 0

    while not window_closed(WINDOW_TITLE) and key_pressed != ESC:
        multicam.clear_cache()
        has_frame, cam_img = camswitcher.read()

        if not has_frame:
            continue

        cv2.imshow(WINDOW_TITLE, cam_img)
        key_pressed = cv2.waitKey(1)

        if key_pressed in NUM_KEYS:
            num = int(chr(key_pressed))
            if camswitcher.select(num - 1):
                print(f"Selected camera {num}")
            else:
                print(f"Can't select camera {num}")

    cv2.destroyAllWindows()
    multicam.release()


if __name__ == "__main__":
    print("Running...")
    main()
