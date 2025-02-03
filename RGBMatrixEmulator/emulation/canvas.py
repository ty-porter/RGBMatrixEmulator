import numpy as np
from PIL import Image, ImageEnhance
from RGBMatrixEmulator.graphics.color import Color


class Canvas:
    def __init__(self, options):
        self.options = options

        self.width = options.cols * options.chain_length
        self.height = options.rows * options.parallel

        # 3D numpy array -- rows (H), columns (W), 3-tuple RGB
        self.__pdims = (self.height, self.width, 3)

        self.display_adapter = options.display_adapter.get_instance(
            self.width, self.height, options
        )

        self.Clear()

        self.display_adapter.load_emulator_window()

    def Clear(self):
        self.__pixels = np.full(
            self.__pdims, self.__create_pixel(Color.BLACK()), dtype=np.uint8
        )

    def Fill(self, r, g, b):
        self.__pixels = np.full(
            self.__pdims, self.__create_pixel((r, g, b)), dtype=np.uint8
        )

    def SetPixel(self, x, y, r, g, b):
        if self.__pixel_out_of_bounds(x, y):
            return

        self.__pixels[int(y)][int(x)] = self.__create_pixel((r, g, b))

    def SetImage(self, image, offset_x=0, offset_y=0, *other):
        enhancer = ImageEnhance.Brightness(image)
        image = enhancer.enhance(self.brightness / 100.0)

        original = Image.fromarray(self.__pixels, "RGB")
        original.paste(image, (offset_x, offset_y))
        self.__pixels = np.copy(original)

    @property
    def brightness(self):
        return self.options.brightness

    @brightness.setter
    def brightness(self, value):
        if not isinstance(value, (int, float)):
            raise ValueError(f"brightness must be a numeric value, received '{value}'")
        elif value < 0 or value > 100:
            raise ValueError(
                f"brightness must be a number between 0 and 100, received '{value}'"
            )

        self.options.brightness = value

    def __create_pixel(self, pixel):
        return Color.adjust_brightness(tuple(pixel), self.brightness / 100.0)

    def __pixel_out_of_bounds(self, x, y):
        if x < 0 or x >= self.width:
            return True

        if y < 0 or y >= self.height:
            return True

        return False

    # These are delegated to the display adapter to handle specific implementation.
    def draw_to_screen(self):
        self.display_adapter.draw_to_screen(self.__pixels)

    def check_for_quit_event(self):
        self.display_adapter.check_for_quit_event()
