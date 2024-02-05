from RGBMatrixEmulator.graphics.color import Color


class Canvas:
    def __init__(self, options):
        self.options = options

        self.width = options.cols * options.chain_length
        self.height = options.rows * options.parallel
        self.display_adapter = options.display_adapter.get_instance(self.width, self.height, options)

        self.__pixels = [[Color.BLACK() for x in range(0, self.width)] for y in range(0, self.height)]

        self.display_adapter.load_emulator_window()

    def Clear(self):
        self.__pixels = [[Color.BLACK() for x in range(0, self.width)] for y in range(0, self.height)]

    def Fill(self, r, g, b):
        self.__pixels = [[Color(r, g, b) for x in range(0, self.width)] for y in range(0, self.height)]

    def SetPixel(self, x, y, r, g, b):
        if self.display_adapter.pixel_out_of_bounds(x, y):
            return

        pixel = self.__pixels[int(y)][int(x)]
        pixel.red = r
        pixel.green = g
        pixel.blue = b

    def SetImage(self, image, offset_x=0, offset_y=0, *other):
        pixel_index = 0
        pixels = [pixel for pixel in image.getdata()]

        for y in range(0, image.height):
            for x in range(0, image.width):
                self.SetPixel(x + offset_x, y + offset_y, *pixels[pixel_index])

                pixel_index += 1

    # These are delegated to the display adapter to handle specific implementation.
    def draw_to_screen(self):
        self.display_adapter.draw_to_screen(self.__pixels)

    def check_for_quit_event(self):
        self.display_adapter.check_for_quit_event()