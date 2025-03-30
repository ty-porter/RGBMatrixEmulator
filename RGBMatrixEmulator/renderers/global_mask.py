import numpy as np

from PIL import Image, ImageDraw
from RGBMatrixEmulator.logger import Logger
from RGBMatrixEmulator.adapters import PixelStyle

class GlobalMaskRenderer:

    DEFAULT_MASK_FN = "_draw_square_mask"
    MASK_FNS = {
        PixelStyle.SQUARE: "_draw_square_mask",
        PixelStyle.CIRCLE: "_draw_circle_mask",
        PixelStyle.REAL: "_draw_real_mask",
    }

    def __init__(self, options):
        self.options = options

        self.__black = Image.new("RGB", self.options.window_size(), "black")
        self.__mask = self.__draw_mask()

    def render(self, pixels):
        image = Image.fromarray(np.array(pixels, dtype=np.uint8), "RGB")
        image = image.resize(self.options.window_size(), Image.NEAREST)

        return Image.composite(image, self.__black, self.__mask)

    def __mask_fn(self, pixel_style):
        if pixel_style not in self.MASK_FNS:
            Logger.warning(
                f"Pixel style '{pixel_style.config_name}' mask function not found, defaulting to {self.DEFAULT_MASK_FN}..."
            )

        return getattr(self, self.MASK_FNS.get(pixel_style, self.DEFAULT_MASK_FN))

    def __draw_mask(self):
        mask = Image.new("L", self.options.window_size())

        draw_fn = self.__mask_fn(self.options.pixel_style)
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

    def _generate_gradient(self, sz, amt):
        """
        Generates a radial gradient of size sz with glow amt.

        The resulting array is normalized between [0, 255].
        """
        # Calculate our own radial gradient to use in the mask.
        # PIL.Image.radial_gradient() produces subpar results (LEDs look blocky)
        x = np.linspace(0, sz, sz)
        y = np.linspace(0, sz, sz)

        # Discrete points (x, y) between 0 and pixel_size
        X, Y = np.meshgrid(x, y)

        # Distance of point to center
        center = sz / 2
        D = np.sqrt((X - center) ** 2 + (Y - center) ** 2)

        # LED radius
        L = (sz - amt) / 2
        G = amt

        # Calculate the radial gradient glow, clip it between 0 and 1, scale by 255 (WHITE), and get the additive inverse
        gradient = 255 - np.clip((D - L) / G, 0, 1) * 255

        return gradient

    def _gradient_add(self, g1, g2):
        """
        Adds two arrays g1 and g2 with equal weight, and normalizes between [0, 255].
        Assumes the input arrays are normalized between [0, 255].

        Each pair of points is added with equal weight by first subtracting 128,
        which produces fewer graphical artifacts than summation by average of the two points.
        """
        return np.clip((g1 - 128) + (g2 - 128), 0, 255)

