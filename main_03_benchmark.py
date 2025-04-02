import timeit

import cv2

from facedetection.camera import Camera


class FaceDetector:
    def __init__(self):
        self.frontal = cv2.CascadeClassifier(
            "facedetection/haarcascade_frontalface_default.xml"
        )

    def _detect(self, img):
        result = self.frontal.detectMultiScale3(
            img, scaleFactor=1.1, minNeighbors=3, outputRejectLevels=True
        )

        return result


class FaceDetectorReduced:
    def __init__(self, resize_factor=0.25):
        self.resize_factor = resize_factor

        self.frontal = cv2.CascadeClassifier(
            "facedetection/haarcascade_frontalface_default.xml"
        )

    def _detect(self, img):
        # Reduce image resolution
        reduced = cv2.resize(
            img,
            None,
            fx=self.resize_factor,
            fy=self.resize_factor,
            interpolation=cv2.INTER_NEAREST,
        )

        result = self.frontal.detectMultiScale3(
            reduced, scaleFactor=1.1, minNeighbors=3, outputRejectLevels=True
        )

        return result


class FaceDetectorGray:
    def __init__(self):
        self.frontal = cv2.CascadeClassifier(
            "facedetection/haarcascade_frontalface_default.xml"
        )

    def _detect(self, img):
        # Convert to grayscale
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        result = self.frontal.detectMultiScale3(
            gray_img, scaleFactor=1.1, minNeighbors=3, outputRejectLevels=True
        )

        return result


class FaceDetectorReducedGray:
    def __init__(self, resize_factor=0.25):
        self.resize_factor = resize_factor

        self.frontal = cv2.CascadeClassifier(
            "facedetection/haarcascade_frontalface_default.xml"
        )

    def _detect(self, img):
        # Reduce image resolution
        reduced = cv2.resize(
            img,
            None,
            fx=self.resize_factor,
            fy=self.resize_factor,
            interpolation=cv2.INTER_NEAREST,
        )
        # Convert to grayscale
        gray_img = cv2.cvtColor(reduced, cv2.COLOR_BGR2GRAY)

        result = self.frontal.detectMultiScale3(
            gray_img, scaleFactor=1.1, minNeighbors=3, outputRejectLevels=True
        )

        return result


DETECTOR_CLASSES = [
    FaceDetector,
    FaceDetectorReduced,
    FaceDetectorGray,
    FaceDetectorReducedGray,
]


def main():
    cam = Camera(device="/dev/video2", resolution=(1080, 720))
    has_frame, cam_img = cam.read()
    cam.release()

    results = []

    for cls in DETECTOR_CLASSES:
        print(f"Testing {cls.__name__}...")
        detector = cls()

        result = timeit.timeit(lambda: detector._detect(cam_img), number=100)

        results.append((result, cls.__name__))

    results.sort()
    print("Done.\n")

    print("Results:")
    for result, cls in results:
        print(f"{result} seconds - {cls}")


if __name__ == "__main__":
    print("Running...")
    main()
