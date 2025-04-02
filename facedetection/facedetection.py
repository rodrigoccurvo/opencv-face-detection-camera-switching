import cv2

BLUE = (255, 0, 0)
GREEN = (0, 255, 0)
RED = (0, 0, 255)


class FaceDetector:
    def __init__(self, resize_factor=0.25):
        self.resize_factor = resize_factor

        self.frontal = cv2.CascadeClassifier(
            "facedetection/haarcascade_frontalface_default.xml"
        )

    def _draw_rects(self, img, rects, color):
        for dims in rects:
            dims = (dims / self.resize_factor).round().astype(int)
            x, y, w, h = dims

            cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)

    def _detect(self, img):
        # Reduce image resolution
        reduced = cv2.resize(
                img, None, fx=self.resize_factor, fy=self.resize_factor,
                interpolation=cv2.INTER_NEAREST
            )
        # Convert to grayscale
        gray_img = cv2.cvtColor(reduced, cv2.COLOR_BGR2GRAY)

        result = self.frontal.detectMultiScale3(
            gray_img, scaleFactor=1.1, minNeighbors=3, outputRejectLevels=True
        )

        return result

    def find_faces(self, img, color=GREEN):
        result = self._detect(img)
        self._draw_rects(img, result[0], color)

        return result
