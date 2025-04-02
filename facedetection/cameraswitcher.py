from .multicamera import MultiCamera


class CameraSwitcher:
    def __init__(self, multicam: MultiCamera):
        self.multicam = multicam

        self.previous = 0
        self.current = 0

    def select(self, index):
        if index == self.current:
            return False

        if index >= len(self.multicam):
            return False

        self.previous = self.current
        self.current = index

        return True

    def read(self):
        return self.multicam.read(self.current)
