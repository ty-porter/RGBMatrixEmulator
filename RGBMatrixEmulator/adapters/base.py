import numpy as np

from PIL import Image, ImageDraw
from RGBMatrixEmulator import version
from RGBMatrixEmulator.logger import Logger
from RGBMatrixEmulator.adapters import PixelStyle


class BaseAdapter:
    SUPPORTED_PIXEL_STYLES = [PixelStyle.DEFAULT]
    INSTANCE = None

    DEFAULT_MASK_FN = "_draw_square_mask"
    MASK_FNS = {
        PixelStyle.SQUARE: "_draw_square_mask",
        PixelStyle.CIRCLE: "_draw_circle_mask",
        PixelStyle.REAL: "_draw_real_mask",
    }

    def __init__(self, width, height, options):
        self.width = width
        self.height = height
        self.options = options
        self.__black = Image.new("RGB", self.options.window_size(), "black")
        self.__mask = self.__draw_mask()
        self.loaded = False

    @classmethod
    def get_instance(cls, *args, **kwargs):
        if cls.INSTANCE is None:
            instance = cls(*args, **kwargs)
            cls.INSTANCE = instance

        return cls.INSTANCE

    def emulator_details_text(self):
        details_text = "RGBME v{} - {}x{} Matrix | {}x{} Chain | {}px per LED ({}) | {}"

        return details_text.format(
            version.__version__,
            self.options.cols,
            self.options.rows,
            self.options.chain_length,
            self.options.parallel,
            self.options.pixel_size,
            self.options.pixel_style.name,
            self.__class__.__name__,
        )

    # This method is required for the pygame adapter but nothing else, so just skip it if not defined.
    def check_for_quit_event(self):
        pass

    #############################################################
    # These methods must be implemented by BaseAdapter subclasses
    #############################################################
    def load_emulator_window(self):
        """
        Initialize the external dependency as a graphics display.

        This method is fired when the emulated canvas is initialized.
        """
        raise NotImplementedError

    def draw_to_screen(self, _pixels):
        """
        Accepts a 2D array of pixels of size height x width.

        Implements drawing each pixel to the screen via the external dependency loaded in load_emulator_window.
        """
        raise NotImplementedError

    #############################################################
    # These methods implement pixel masks (styles)
    #############################################################
    def _get_masked_image(self, pixels):
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
