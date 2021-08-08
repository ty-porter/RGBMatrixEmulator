import os
import pygame

from RGBMatrixEmulator.graphics.color import Color
from RGBMatrixEmulator import version


class Canvas:
    def __init__(self, options):
        self.options = options

        self.width = options.cols * options.chain_length
        self.height = options.rows * options.parallel
        self.brightness = options.brightness
        
        self.__pixels = [[Color.BLACK() for x in range(0, self.width)] for y in range(0, self.height)]
        self.__surface = None

        self.__load_emulator_window()

    def __load_emulator_window(self):
        load_text = 'EMULATOR: Loading {}'.format(self.__emulator_details_text())
        print(load_text)
        self.__surface = pygame.display.set_mode(self.options.window_size())
        pygame.init()
        
        self.__set_emulator_icon()
        pygame.display.set_caption(self.__emulator_details_text())

    def __emulator_details_text(self):
        details_text = 'RGBME v{} - {}x{} Matrix | {}x{} Chain | {}px per LED ({}) | {}x{} Window'

        return details_text.format(version.__version__,
                                   self.options.cols,
                                   self.options.rows,
                                   self.options.chain_length,
                                   self.options.parallel,
                                   self.options.pixel_size,
                                   self.options.pixel_style.upper(),
                                   *self.options.window_size())

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
        self.__adjust_pixel_brightness(pixel)
        pixel_rect = self.__pygame_pixel(x, y)
        if self.options.pixel_style == 'circle':
            radius = int(pixel_rect.width / 2)
            center_x = pixel_rect.x + radius
            center_y = pixel_rect.y + radius
            pygame.draw.circle(self.__surface, pixel.to_tuple(), (center_x, center_y), radius)
        else:
            pygame.draw.rect(self.__surface, pixel.to_tuple(), pixel_rect)

    def __adjust_pixel_brightness(self, pixel):
        alpha = self.brightness / 100.0
        pixel.adjust_brightness(alpha)

    def __pixel_out_of_bounds(self, x, y):
        if x < 0 or x >= self.width:
            return True
        
        if y < 0 or y >= self.height:
            return True

        return False

    def draw_to_screen(self):
        for row, pixels in enumerate(self.__pixels):
            for col, pixel in enumerate(pixels):
                self.__draw_pixel(pixel, col, row)
        
        pygame.display.flip()

    def Clear(self):
        self.__pixels = [[Color.BLACK() for x in range(0, self.width)] for y in range(0, self.height)]

    def Fill(self, r, g, b):
        self.__pixels = [[Color(r, g, b) for x in range(0, self.width)] for y in range(0, self.height)]

    def SetPixel(self, x, y, r, g, b):
        if self.__pixel_out_of_bounds(x, y):
            return

        try:
            pixel = self.__pixels[int(y)][int(x)]
            pixel.r = r
            pixel.g = g
            pixel.b = b
        except Exception:
            pass

    def SetImage(self, image, offset_x=0, offset_y=0, *other):
        pixel_index = 0
        pixels = [pixel for pixel in image.getdata()]

        self.Clear()
        for y in range(0, self.height):
            for x in range(0, self.width):
                try:
                    self.SetPixel(x + offset_x, y + offset_y, *pixels[pixel_index])
                except Exception:
                    pass

                pixel_index += 1
