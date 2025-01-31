import numpy as np

from PIL import Image, ImageDraw
from RGBMatrixEmulator import version


def draw_circle_mask(drawer, x, y, pixel_size, color):
    drawer.ellipse(
        (x, y, x + pixel_size - 1, y + pixel_size - 1),
        fill=color,
        outline=color,
    )


def draw_square_mask(drawer, x, y, pixel_size, color):
    drawer.rectangle(
        (x, y, x + pixel_size, y + pixel_size),
        fill=color,
        outline=color,
    )


class BaseAdapter:
    SUPPORTS_ALTERNATE_PIXEL_STYLE = False
    INSTANCE = None

    def __init__(self, width, height, options):
        self.width = width
        self.height = height
        self.options = options
        self.__black = Image.new("RGB", self.options.window_size(), "black")
        self.__mask = self.__draw_mask()
        self.loaded = False

    def __draw_mask(self):
        mask = Image.new("L", self.options.window_size())
        drawer = ImageDraw.Draw(mask)
        pixel_size = self.options.pixel_size
        width, height = self.options.window_size()
        draw_mask_shape = (
            draw_circle_mask
            if self.options.pixel_style == "circle"
            else draw_square_mask
        )
        for y in range(0, height, pixel_size):
            for x in range(0, width, pixel_size):
                draw_mask_shape(drawer, x, y, pixel_size, 255)

        return mask

    @classmethod
    def get_instance(cls, *args, **kwargs):
        if cls.INSTANCE is None:
            instance = cls(*args, **kwargs)
            cls.INSTANCE = instance

        return cls.INSTANCE

    def _get_masked_image(self, pixels):
        image = Image.fromarray(np.array(pixels, dtype=np.uint8), "RGB")
        image = image.resize(self.options.window_size(), Image.NEAREST)

        return Image.composite(image, self.__black, self.__mask)

    def emulator_details_text(self):
        details_text = "RGBME v{} - {}x{} Matrix | {}x{} Chain | {}px per LED ({}) | {}"

        return details_text.format(
            version.__version__,
            self.options.cols,
            self.options.rows,
            self.options.chain_length,
            self.options.parallel,
            self.options.pixel_size,
            self.options.pixel_style.upper(),
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
