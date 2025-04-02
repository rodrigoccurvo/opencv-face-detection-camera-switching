import time

import numpy as np

from .facedetection import FaceDetector
from .fadecameraswitcher import FadeCameraSwitcher


class AutoCameraSwitcher(FadeCameraSwitcher):
    def __init__(self, *args, check_delay=0.2, **kwargs):
        super().__init__(*args, **kwargs)

        self.check_delay = check_delay
        self.last_check = 0

        self.detector = FaceDetector()

    def read(self):
        if (
            not self.is_changing()
            and time.time() - self.last_check >= self.check_delay
        ):
            self.last_check = time.time()
            self._select_facing_cam()

        return super().read()

    def _select_facing_cam(self):
        n_cams = len(self.multicam)
        detections = np.zeros(n_cams)

        for index in range(n_cams):
            has_frame, img = self.multicam.read(index)
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
