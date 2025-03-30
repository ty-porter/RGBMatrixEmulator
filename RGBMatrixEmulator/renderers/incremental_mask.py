import numpy as np

from PIL import Image, ImageOps
from RGBMatrixEmulator.adapters import PixelStyle
from RGBMatrixEmulator.renderers.base import RendererBase

class IncrementalMaskRenderer(RendererBase):

    DEFAULT_MASK_FN = "_draw_real_mask"
    MASK_FNS = {
        PixelStyle.REAL: "_draw_real_mask",
    }

    def __init__(self, options):
        super(IncrementalMaskRenderer, self).__init__(options)

        self.__mask = self.__draw_mask()

        self.iter = 0

    def render(self, pixels):
        self.__canvas = Image.new("RGB", self.options.window_size(), "black")
        offset = self.options.pixel_size + self.options.pixel_glow // 2

        self.iter += 1

        for y, row in enumerate(pixels):
            for x, pixel in enumerate(row):
                led = ImageOps.colorize(self.__mask, "black", pixel)

                self.__canvas.paste(led, (x * offset, y * offset), self.__mask)

        return self.__canvas

    def __draw_mask(self):
        draw_fn = self._mask_fn(self.options.pixel_style)

        return draw_fn()

    def _draw_real_mask(self, _mask=None):
        pixel_size = self.options.pixel_size
        pixel_glow = self.options.pixel_glow

        # Create two gradients.
        # The first is the LED with a gradient amount of 1 to antialias the result.
        # The second is the actual glow given the setting.
        pixel = self._generate_gradient(pixel_size, 1)
        glow = self.radial_gradient(pixel_size + pixel_glow)

        offset = pixel_glow // 2

        pixel = np.pad(pixel, ((offset, offset), (offset, offset)), mode="constant", constant_values=0)
        
        gradient = self._gradient_add(pixel, glow)

        return Image.fromarray(gradient.astype(np.uint8))

    def radial_gradient(self, size):
        # Create coordinate grids
        x = np.linspace(-1, 1, size)  # X values from -1 to 1
        y = np.linspace(-1, 1, size)  # Y values from -1 to 1
        X, Y = np.meshgrid(x, y)

        # Compute radial distance from the center
        radius = np.sqrt(X ** 2 + Y ** 2)

        # Normalize the gradient (0 at center, 1 at edges)
        return 255 - np.clip(radius, 0, 1) * 255
