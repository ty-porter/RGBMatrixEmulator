import os
import sys

# Try to suppress the pygame load warning if able.
try:
    os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
except Exception:
    pass

import pygame

from pygame.locals import QUIT
from RGBMatrixEmulator.adapters.base import BaseAdapter
from RGBMatrixEmulator.adapters import PixelStyle
from RGBMatrixEmulator.logger import Logger


class PygameAdapter(BaseAdapter):
    SUPPORTED_PIXEL_STYLES = [
        PixelStyle.SQUARE,
        PixelStyle.CIRCLE,
        PixelStyle.REAL,
    ]

    def __init__(self, width, height, options):
        super().__init__(width, height, options)
        self.__surface = None

    def load_emulator_window(self):
        if self.loaded:
            return

        Logger.info("Loading {}".format(self.emulator_title))
        self.__surface = pygame.display.set_mode(self.options.window_size())
        pygame.init()

        self.__set_emulator_icon()
        pygame.display.set_caption(self.emulator_title)

        self.loaded = True

    def draw_to_screen(self, pixels):
        image = self._get_masked_image(pixels)
        pygame_surface = pygame.image.fromstring(
            image.tobytes(), self.options.window_size(), "RGB"
        )
        self.__surface.blit(pygame_surface, (0, 0))

        pygame.display.flip()

    def check_for_quit_event(self):
        # We don't have events, but this will keep the emulator from appearing as if it's not responding.
        # This also enables closing the window to kill the emulator
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

    def __set_emulator_icon(self):
        icon = pygame.image.load(self.icon_path)
        pygame.display.set_icon(icon)
