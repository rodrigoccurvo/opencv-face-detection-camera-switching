from .camera import Camera


class MultiCamera:
    def __init__(self, devices, resolution):
        self.devices = devices
        self.resolution = resolution

        self.cams = [
            Camera(device, self.resolution) for device in self.devices
        ]

    def __len__(self):
        return len(self.cams)

    def read(self, index):
        return self.cams[index].read()

    def flush(self):
        # Grab frame without processing it, just to empty buffer
        for cam in self.cams:
            cam.grab()

    def release(self):
        for cam in self.cams:
            cam.release()
