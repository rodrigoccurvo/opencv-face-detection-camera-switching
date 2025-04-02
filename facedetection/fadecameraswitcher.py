import time

from .cameraswitcher import CameraSwitcher


class FadeCameraSwitcher(CameraSwitcher):
    def __init__(self, *args, fade_delay=1, **kwargs):
        super().__init__(*args, **kwargs)

        self.fade_delay = fade_delay
        self.select_time = 0
        self.current_opacity = 1.0

    def is_changing(self):
        return self.current_opacity != 1.0

    def select(self, index):
        # Don't switch camera if we're already
        # in the middle of a change
        if self.is_changing():
            return False

        ret = super().select(index)

        if ret:
            self.current_opacity = 0.0
            self.select_time = time.time()

        return ret

    def read(self):
        curr_has_frame, curr_img = self.multicam.read(self.current)

        if not self.is_changing() or not curr_has_frame:
            return curr_has_frame, curr_img

        prev_has_frame, prev_img = self.multicam.read(self.previous)

        if not prev_has_frame:
            return curr_has_frame, curr_img

        return True, self._blend(prev_img, curr_img)

    def _blend(self, img_from, img_to):
        elapsed_time = time.time() - self.select_time
        self.current_opacity = min(elapsed_time / self.fade_delay, 1.0)

        blend = img_to * self.current_opacity
        blend += img_from * (1 - self.current_opacity)

        return blend.astype(img_to.dtype)
