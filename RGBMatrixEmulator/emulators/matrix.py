import pygame

from copy import copy

from RGBMatrixEmulator.emulators.canvas import Canvas
from RGBMatrixEmulator.graphics.color import Color


class RGBMatrix:
    def __init__(self, options = {}):
        self.options = options

        self.width = options.cols
        self.height = options.rows
        self.brightness = options.brightness

        self.canvas = None

    def CreateFrameCanvas(self):
        if self.canvas:
            return self.canvas

        return Canvas(options = self.options)
    
    def SwapOnVSync(self, canvas):
        # We don't have events, but this will keep the emulator from appearing as if it's not responding
        pygame.event.get()

        canvas.draw_to_screen()

        return canvas

    def Fill(self, r, g, b):
        new_opts = copy(self.options)
        new_opts.brightness = self.brightness

        if not self.canvas:
            self.canvas = Canvas(options = new_opts)
            
        self.canvas.Fill(r, g, b)
        self.SwapOnVSync(self.canvas)

    def SetPixel(self, x, y, r, g, b):
        new_opts = copy(self.options)
        new_opts.brightness = self.brightness

        if not self.canvas:
            self.canvas = Canvas(options = new_opts)

        self.canvas.SetPixel(x, y, r, g, b)
        self.SwapOnVSync(self.canvas)