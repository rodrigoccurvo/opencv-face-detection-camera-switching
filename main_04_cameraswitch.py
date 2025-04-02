import cv2

from facedetection.cameraswitcher import CameraSwitcher
from facedetection.facedetection import FaceDetector
from facedetection.multicamera import MultiCamera


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
NUM_KEYS = [ord(str(i)) for i in range(10)]


def main():
    multicam = MultiCamera(
        devices=["/dev/video2", "/dev/video0"], resolution=(640, 480)
    )
    camswitcher = CameraSwitcher(multicam)

    detector = FaceDetector()

    key_pressed = 0

    while not window_closed(WINDOW_TITLE) and key_pressed != ESC:
        has_frame, cam_img = camswitcher.read()

        if not has_frame:
            continue

        detector.find_faces(cam_img)

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
