import numpy as np
from PIL import Image
from RGBMatrixEmulator.graphics.color import Color

class Canvas:
    def __init__(self, options):
        self.options = options

        self.width = options.cols * options.chain_length
        self.height = options.rows * options.parallel
        self.display_adapter = options.display_adapter.get_instance(self.width, self.height, options)

        self.__pixels = [[Color.BLACK() for x in range(0, self.width)] for y in range(0, self.height)]

        self.display_adapter.load_emulator_window()

    def Clear(self):
        self.__pixels = [[Color.BLACK() for x in range(0, self.width)] for y in range(0, self.height)]

    def Fill(self, r, g, b):
        self.__pixels = [[(r, g, b) for x in range(0, self.width)] for y in range(0, self.height)]

    def SetPixel(self, x, y, r, g, b):
        if self.display_adapter.pixel_out_of_bounds(x, y):
            return

        pixel = self.__pixels[int(y)][int(x)] = (r, g, b)

    def SetImage(self, image, offset_x=0, offset_y=0, *other):
        original = Image.fromarray(np.array(self.__pixels, dtype=np.uint8), "RGB")
        original.paste(image, (offset_x, offset_y))
        self.__pixels = np.asarray(original)

    # These are delegated to the display adapter to handle specific implementation.
    def draw_to_screen(self):
        self.display_adapter.draw_to_screen(self.__pixels)

    def check_for_quit_event(self):
        self.display_adapter.check_for_quit_event()