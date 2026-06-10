from typing import Any

import numpy as np
from PIL import Image, ImageEnhance
from RGBMatrixEmulator.emulation.options import RGBMatrixOptions


class Canvas:
    def __init__(self, options: RGBMatrixOptions) -> None:
        self.options = options
        self.__screen = options.screen

        self.width, self.height = self.__screen.pixel_buffer_size

        # 3D numpy array -- rows (H), columns (W), 3-tuple RGB
        self.__pdims = (self.height, self.width, 3)

        screen_w, screen_h = self.__screen.screen_size
        self.display_adapter = options.display_adapter.get_instance(
            screen_w, screen_h, options
        )

        self.Clear()

        self.display_adapter.load_emulator_window()

    def Clear(self) -> None:
        self.__pixels = np.full(self.__pdims, (0, 0, 0), dtype=np.uint8)

    def Fill(self, r: int, g: int, b: int) -> None:
        self.__pixels = np.full(self.__pdims, (r, g, b), dtype=np.uint8)

    def SetPixel(self, x: int, y: int, r: int, g: int, b: int) -> None:
        if 0 <= x < self.width and 0 <= y < self.height:
            self.__pixels[int(y), int(x)] = (r, g, b)

    def SetImage(
        self,
        image: Image.Image,
        offset_x: int = 0,
        offset_y: int = 0,
        unsafe: bool = True,
    ) -> None:
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

    # These are delegated to the display adapter to handle specific implementation.
    def draw_to_screen(self) -> None:
        # Handle brightness across the entire pixel buffer as soon as it's ready to draw.
        alpha = self.brightness / 100.0
        pixels = (self.__screen.render(self.__pixels) * alpha).astype(np.uint8)

        self.display_adapter.draw_to_screen(pixels)

    def check_for_quit_event(self) -> None:
        self.display_adapter.check_for_quit_event()
