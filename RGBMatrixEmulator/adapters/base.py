from RGBMatrixEmulator import version


class BaseAdapter:

    SUPPORTS_ALTERNATE_PIXEL_STYLE = False
    INSTANCE = None

    def __init__(self, width, height, options):
        self.width   = width
        self.height  = height
        self.options = options

        self.loaded  = False

    @classmethod
    def get_instance(cls, *args, **kwargs):
        if cls.INSTANCE is None:
            instance = cls(*args, **kwargs)
            cls.INSTANCE = instance
        
        return cls.INSTANCE

    def adjust_pixel_brightness(self, pixel, to_int = False):
        alpha = self.options.brightness / 100.0
        pixel.adjust_brightness(alpha, to_int = to_int)

    def pixel_out_of_bounds(self, x, y):
        if x < 0 or x >= self.width:
            return True

        if y < 0 or y >= self.height:
            return True

        return False

    def emulator_details_text(self):
        details_text = 'RGBME v{} - {}x{} Matrix | {}x{} Chain | {}px per LED ({}) | {}'

        return details_text.format(version.__version__,
                                   self.options.cols,
                                   self.options.rows,
                                   self.options.chain_length,
                                   self.options.parallel,
                                   self.options.pixel_size,
                                   self.options.pixel_style.upper(),
                                   self.__class__.__name__)

    # This method is required for the pygame adapter but nothing else, so just skip it if not defined.
    def check_for_quit_event(self):
        pass

    #############################################################
    # These methods must be implemented by BaseAdapter subclasses
    #############################################################
    def load_emulator_window(self):
        '''
        Initialize the external dependency as a graphics display.

        This method is fired when the emulated canvas is initialized.
        '''
        raise NotImplementedError

    def draw_to_screen(self, _pixels):
        '''
        Accepts a 2D array of pixels of size height x width.

        Implements drawing each pixel to the screen via the external dependency loaded in load_emulator_window.
        Before drawing, use adjust_pixel_brightness() on each pixel if your display adapter supports it.
        '''
        raise NotImplementedError
