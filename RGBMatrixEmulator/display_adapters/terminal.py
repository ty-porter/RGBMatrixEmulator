import os
import sys

from RGBMatrixEmulator.display_adapters.base import BaseAdapter


class Terminal(BaseAdapter):

    SYMBOLS = {
        "circle": " ●",
        "square": "██"
    }

    def __init__(self, width, height, options):
        super().__init__(width, height, options)
        self.__symbol = self.SYMBOLS.get(self.options.pixel_style)

    def check_for_quit_event(self):
        pass

    def draw_to_screen(self, pixels):
        output = "\033[H\n"                                               # Move the cursor to the home position, add a little border
        for pixel_row in pixels:
            output += "  "                                                # Add a bit of border in case cursor causes line to wrap
            for pixel in pixel_row:
                self.adjust_pixel_brightness(pixel, to_int = True)
                output += "\033[38;2;{};{};{}m".format(*pixel.to_tuple()) # Set the cell to the pixel color
                output += self.__symbol                                   # Draw the pixel
                output += "\033[37m"                                      # Reset the color
            
            output += " \n"

        sys.stdout.write(output)

    def load_emulator_window(self):
        os.system('cls||clear')
        os.system('mode con: cols={} lines={}'.format(self.width * 2 + 5, self.height + 3))