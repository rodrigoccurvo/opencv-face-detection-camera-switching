from .multicamera import MultiCamera


class MultiCameraCached(MultiCamera):
    EMPTY = (None, None)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.clear_cache()

    def clear_cache(self):
        self.cams_cache = [MultiCameraCached.EMPTY] * len(self)

    def read(self, index):
        if not self.cams_cache[index][0]:
            self.cams_cache[index] = super().read(index)

        return self.cams_cache[index]
