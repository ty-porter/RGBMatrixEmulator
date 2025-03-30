import numpy as np

from PIL import Image, ImageDraw
from RGBMatrixEmulator.adapters import PixelStyle
from RGBMatrixEmulator.renderers.base import RendererBase

class GlobalMaskRenderer(RendererBase):

    DEFAULT_MASK_FN = "_draw_square_mask"
    MASK_FNS = {
        PixelStyle.SQUARE: "_draw_square_mask",
        PixelStyle.CIRCLE: "_draw_circle_mask",
        PixelStyle.REAL: "_draw_real_mask",
    }

    def __init__(self, options):
        super(GlobalMaskRenderer, self).__init__(options)

        self.__black = Image.new("RGB", self.options.window_size(), "black")
        self.__mask = self.__draw_mask()

    def render(self, pixels):
        image = Image.fromarray(np.array(pixels, dtype=np.uint8), "RGB")
        image = image.resize(self.options.window_size(), Image.NEAREST)

        return Image.composite(image, self.__black, self.__mask)

    def __draw_mask(self):
        mask = Image.new("L", self.options.window_size())

        draw_fn = self._mask_fn(self.options.pixel_style)
        draw_fn(mask)

        return mask

    def _draw_circle_mask(self, mask):
        pixel_size = self.options.pixel_size
        width, height = self.options.window_size()

        drawer = ImageDraw.Draw(mask)

        for y in range(0, height, pixel_size):
            for x in range(0, width, pixel_size):
                drawer.ellipse(
                    (x, y, x + pixel_size - 1, y + pixel_size - 1),
                    fill=255,
                    outline=255,
                )

    def _draw_square_mask(self, mask):
        pixel_size = self.options.pixel_size
        width, height = self.options.window_size()

        drawer = ImageDraw.Draw(mask)

        for y in range(0, height, pixel_size):
            for x in range(0, width, pixel_size):
                drawer.rectangle(
                    (x, y, x + pixel_size, y + pixel_size),
                    fill=255,
                    outline=255,
                )

    def _draw_real_mask(self, mask):
        pixel_size = self.options.pixel_size
        width, height = self.options.window_size()
        pixel_glow = self.options.pixel_glow

        if pixel_glow == 0:
            # Short circuit to a faster draw routine
            return self._draw_circle_mask(mask)

        # Create two gradients.
        # The first is the LED with a gradient amount of 1 to antialias the result.
        # The second is the actual glow given the setting.
        gradient = self._gradient_add(
            self._generate_gradient(pixel_size, 1),
            self._generate_gradient(pixel_size, pixel_glow),
        )

        pixel = Image.fromarray(gradient.astype(np.uint8))

        # Paste the pixel into the mask at each point.
        for y in range(0, height, pixel_size):
            for x in range(0, width, pixel_size):
                mask.paste(pixel, (x, y), pixel)
