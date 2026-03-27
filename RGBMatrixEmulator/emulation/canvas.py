from typing import Any

import numpy as np
from PIL import Image, ImageEnhance
from RGBMatrixEmulator.emulation.options import RGBMatrixOptions


class Canvas:
    def __init__(self, options: RGBMatrixOptions) -> None:
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

    def Clear(self) -> None:
        self.__pixels = np.full(
            self.__pdims, self.__create_pixel((0, 0, 0)), dtype=np.uint8
        )

    def Fill(self, r: int, g: int, b: int) -> None:
        self.__pixels = np.full(
            self.__pdims, self.__create_pixel((r, g, b)), dtype=np.uint8
        )

    def SetPixel(self, x: int, y: int, r: int, g: int, b: int) -> None:
        if self.__pixel_out_of_bounds(x, y):
            return

        self.__pixels[int(y)][int(x)] = self.__create_pixel((r, g, b))

    def SetImage(
        self,
        image: Image.Image,
        offset_x: int = 0,
        offset_y: int = 0,
        unsafe: bool = True,
    ) -> None:
        enhancer = ImageEnhance.Brightness(image)
        image = enhancer.enhance(self.brightness / 100.0)

        original = Image.fromarray(self.__pixels, "RGB")
        original.paste(image, (offset_x, offset_y))
        self.__pixels = np.copy(original)  # type: ignore

    @property
    def brightness(self) -> int:
        return self.options.brightness

    @brightness.setter
    def brightness(self, value: int) -> None:
        if not isinstance(value, (int, float)):
            raise ValueError(f"brightness must be a numeric value, received '{value}'")
        elif value < 0 or value > 100:
            raise ValueError(
                f"brightness must be a number between 0 and 100, received '{value}'"
            )

        self.options.brightness = value

    def __create_pixel(self, pixel):
        return __adjust_brightness(tuple(pixel), self.brightness / 100.0)

    def __pixel_out_of_bounds(self, x, y):
        if x < 0 or x >= self.width:
            return True

        if y < 0 or y >= self.height:
            return True

        return False

    # These are delegated to the display adapter to handle specific implementation.
    def draw_to_screen(self) -> None:
        self.display_adapter.draw_to_screen(self.__pixels)

    def check_for_quit_event(self) -> None:
        self.display_adapter.check_for_quit_event()


def __adjust_brightness(pixel, alpha, to_int=False):
    if to_int:
        return tuple(int(channel) for channel in pixel)

    return tuple(channel * alpha for channel in pixel)
