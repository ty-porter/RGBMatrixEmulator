import time
from RGBMatrixEmulator.logger import Logger

DEFAULT_UPDATE_RATE = 0.5 # seconds


class FPSMonitor:
    def __init__(self, update_rate=DEFAULT_UPDATE_RATE):
        self.update_rate = update_rate
        self.n_frames = 0
        self.start_time = time.time()

    def tick(self):
        self.n_frames += 1
        now = time.time()
        elapsed = now - self.start_time

        if elapsed >= self.update_rate:
            fps = round(self.n_frames / elapsed, 2)

            Logger.debug(f"FPS: {fps} (received {self.n_frames} frames over {round(elapsed, 2)}s)")

            self.n_frames = 0
            self.start_time = now
