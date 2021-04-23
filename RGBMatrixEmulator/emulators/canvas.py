import os
import pygame

from RGBMatrixEmulator.graphics.color import Color
from RGBMatrixEmulator import version


class Canvas:
    def __init__(self, options):
        self.options = options

        self.width = options.cols
        self.height = options.rows
        self.brightness = options.brightness
        
        self.__pixels = [[Color.BLACK() for x in range(0, self.options.cols)] for y in range(0, self.options.rows)]
        self.__surface = None

        self.__load_emulator_window()

    def __load_emulator_window(self):
        load_text = 'EMULATOR: Loading window {} ({}px per LED) for {}x{} matrix...'
        print(load_text.format(self.options.window_size(), self.options.pixel_size, self.options.cols,  self.options.rows))
        self.__surface = pygame.display.set_mode(self.options.window_size())
        pygame.init()
        
        pygame.display.set_caption('RPI LED Matrix Emulator v{}'.format(version.__version__))

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
        pygame.draw.rect(self.__surface, pixel.to_tuple(), pixel_rect)

    def __adjust_pixel_brightness(self, pixel):
        alpha = self.brightness / 100.0
        pixel.adjust_brightness(alpha)

    def draw_to_screen(self):
        for row, pixels in enumerate(self.__pixels):
            for col, pixel in enumerate(pixels):
                self.__draw_pixel(pixel, col, row)
        
        pygame.display.flip()

    def Clear(self):
        self.__pixels = [[Color.BLACK() for x in range(0, self.options.cols)] for y in range(0, self.options.rows)]

    def Fill(self, r, g, b):
        self.__pixels = [[Color(r, g, b) for x in range(0, self.options.cols)] for y in range(0, self.options.rows)]

    def SetPixel(self, x, y, r, g, b):
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
