from .fadecameraswitcher import FadeCameraSwitcher
from .facedetection import FaceDetector
import time
import numpy as np


class _CachedCameraSwitcher(FadeCameraSwitcher):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._clear_cache()

    def _clear_cache(self):
        self.cams_cache = [None] * len(self.multicam)

    def _read_cam(self, index):
        if self.cams_cache[index] is None:
            self.cams_cache[index] = self.multicam.read(index)

        return self.cams_cache[index]


class AutoCameraSwitcher(_CachedCameraSwitcher):
    def __init__(self, *args, check_delay=0.2, **kwargs):
        super().__init__(*args, **kwargs)

        self.check_delay = check_delay
        self.last_check = 0

        self.detector = FaceDetector()

    def read(self):
        self._clear_cache()

        if not self.is_fading() and time.time() - self.last_check >= self.check_delay:
            self.last_check = time.time()
            self._select_facing_cam()

        return super().read()

    def _select_facing_cam(self):
        size = len(self.multicam)
        detections = np.zeros(size)

        for index in range(size):
            has_frame, img = self._read_cam(index)
            if not has_frame:
                continue

            _, _, confidences = self.detector.find_faces(img)

            if len(confidences) > 0:
                detections[index] = confidences.max()

        # print(detections)

        max_confidence = detections.max()

        if max_confidence > 0:
            face_index = detections.argmax()
            self.select(face_index)
