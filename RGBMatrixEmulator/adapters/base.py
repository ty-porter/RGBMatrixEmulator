from RGBMatrixEmulator import version
from RGBMatrixEmulator.adapters import PixelStyle


class BaseAdapter:
    SUPPORTED_PIXEL_STYLES = [PixelStyle.DEFAULT]
    INSTANCE = None

    def __init__(self, width, height, options):
        self.width = width
        self.height = height
        self.options = options
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
