import numpy as np

from RGBMatrixEmulator.logger import Logger

class RendererBase:
    def __init__(self, options):
        self.options = options

    def _mask_fn(self, pixel_style):
        if pixel_style not in self.MASK_FNS:
            Logger.warning(
                f"Pixel style '{pixel_style.config_name}' mask function not found, defaulting to {self.DEFAULT_MASK_FN}..."
            )

        return getattr(self, self.MASK_FNS.get(pixel_style, self.DEFAULT_MASK_FN))

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
