from RGBMatrixEmulator.graphics.color import Color
import numpy as np

def shift_array(arr, x, y, K):
    shifted_arr = np.full_like(arr, K)  # Create a new array filled with K

    if x > 0:
        shifted_arr[:, x:] = arr[:, :-x]
    elif x < 0:
        shifted_arr[:, :x] = arr[:, -x:]
    else:
        shifted_arr[:, :] = arr[:, :]

    if y > 0:
        shifted_arr[y:, :] = shifted_arr[:-y, :]
        shifted_arr[:y, :] = K
    elif y < 0:
        shifted_arr[:y, :] = shifted_arr[-y:, :]
        shifted_arr[y:, :] = K

    return shifted_arr


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
        pixels = np.asarray(image)
        if offset_x != 0 or offset_y != 0:
            pixels = shift_array(pixels, offset_x, offset_y, (0,0,0))
        self.__pixels = pixels

    # These are delegated to the display adapter to handle specific implementation.
    def draw_to_screen(self):
        self.display_adapter.draw_to_screen(self.__pixels)

    def check_for_quit_event(self):
        self.display_adapter.check_for_quit_event()