from RGBMatrixEmulator import version

class BaseAdapter:
    def __init__(self, width, height, options):
        self.width   = width
        self.height  = height
        self.options = options

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
        details_text = 'RGBME v{} - {}x{} Matrix | {}x{} Chain | {}px per LED ({}) | {}x{} Window'

        return details_text.format(version.__version__,
                                   self.options.cols,
                                   self.options.rows,
                                   self.options.chain_length,
                                   self.options.parallel,
                                   self.options.pixel_size,
                                   self.options.pixel_style.upper(),
                                   *self.options.window_size())

    # These methods must be implemented by BaseAdapter subclasses
    def check_for_quit_events(self):
        raise NotImplementedError

    def draw_to_screen(self):
        raise NotImplementedError

    def load_emulator_window(self):
        raise NotImplementedError
