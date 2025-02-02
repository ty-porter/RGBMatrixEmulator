from RGBMatrixEmulator.adapters.base import BaseAdapter

from PIL import Image

import numpy as np


class RawAdapter(BaseAdapter):
    MAX_FRAMES_STORED = 128
    DEFAULT_MAX_FRAME = -1  # Never halts

    def __init__(self, width, height, options):
        super().__init__(width, height, options)

        self._reset()

    def draw_to_screen(self, pixels):
        self.frames[self.frame] = pixels

        if self.frame - self.MAX_FRAMES_STORED in self.frames:
            del self.frames[self.frame - RawAdapter.MAX_FRAMES_STORED]

        self.frame += 1

        if self.halt_after > 0 and self.frame >= self.halt_after:
            self.halt_fn()

    def load_emulator_window(self):
        pass

    def _dump_screenshot(self, path):
        image = Image.fromarray(np.array(self._last_frame(), dtype="uint8"), "RGB")
        image.save(path)

    def _last_frame(self):
        return self.frames[self.frame - 1]

    def _reset(self):
        self.frames = {}
        self.frame = 0

        self.halt_after = RawAdapter.DEFAULT_MAX_FRAME
        self.halt_fn = lambda: 1 + 1
