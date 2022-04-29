import os
import sys

# Try to suppress the pygame load warning if able.
try:
    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
except Exception:
    pass

import pygame

from pygame.locals import QUIT
from RGBMatrixEmulator.adapters.base import BaseAdapter


class PygameAdapter(BaseAdapter):

    SUPPORTS_ALTERNATE_PIXEL_STYLE = True

    def __init__(self, width, height, options):
        super().__init__(width, height, options)
        self.__surface = None

    def load_emulator_window(self):
        print('EMULATOR: Loading {}'.format(self.emulator_details_text()))
        self.__surface = pygame.display.set_mode(self.options.window_size())
        pygame.init()

        self.__set_emulator_icon()
        pygame.display.set_caption(self.emulator_details_text())

    def draw_to_screen(self, pixels):
        for row, pixel_row in enumerate(pixels):
            for col, pixel in enumerate(pixel_row):
                self.__draw_pixel(pixel, col, row)

        pygame.display.flip()

    def check_for_quit_event(self):
        # We don't have events, but this will keep the emulator from appearing as if it's not responding.
        # This also enables closing the window to kill the emulator
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

    def __set_emulator_icon(self):
        emulator_path = os.path.abspath(os.path.dirname(__file__))
        icon_path = os.path.join(emulator_path, '..', 'icon.png')
        icon = pygame.image.load(os.path.normpath(icon_path))

        pygame.display.set_icon(icon)

    def __pygame_pixel(self, col, row):
        return pygame.Rect(
            col * self.options.pixel_size,
            row * self.options.pixel_size,
            self.options.pixel_size,
            self.options.pixel_size
        )

    def __draw_pixel(self, pixel, x, y):
        self.adjust_pixel_brightness(pixel)
        pixel_rect = self.__pygame_pixel(x, y)
        if self.options.pixel_style == 'circle':
            radius = int(pixel_rect.width / 2)
            center_x = pixel_rect.x + radius
            center_y = pixel_rect.y + radius
            pygame.draw.circle(self.__surface, pixel.to_tuple(), (center_x, center_y), radius)
        else:
            pygame.draw.rect(self.__surface, pixel.to_tuple(), pixel_rect)
