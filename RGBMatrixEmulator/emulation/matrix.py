from RGBMatrixEmulator.emulation.canvas import Canvas


class RGBMatrix:
    def __init__(self, options={}):
        self.options = options

        self.width = options.cols * options.chain_length
        self.height = options.rows * options.parallel

        self.canvas = None

    def CreateFrameCanvas(self):
        self.canvas = Canvas(options=self.options)

        return self.canvas

    def SwapOnVSync(self, canvas):
        canvas.check_for_quit_event()
        canvas.draw_to_screen()
        self.canvas = canvas

        return self.canvas

    def Clear(self):
        self.__sync_canvas()
        self.canvas.Clear()
        self.SwapOnVSync(self.canvas)

    def Fill(self, r, g, b):
        self.__sync_canvas()
        self.canvas.Fill(r, g, b)
        self.SwapOnVSync(self.canvas)

    def SetPixel(self, x, y, r, g, b):
        self.__sync_canvas()
        self.canvas.SetPixel(x, y, r, g, b)
        self.SwapOnVSync(self.canvas)

    def SetImage(self, image, offset_x=0, offset_y=0, *other):
        self.__sync_canvas()
        self.canvas.SetImage(image, offset_x, offset_y, *other)
        self.SwapOnVSync(self.canvas)

    def __sync_canvas(self):
        if not self.canvas:
            self.canvas = Canvas(options=self.options)

    @property
    def brightness(self):
        return self.options.brightness

    @brightness.setter
    def brightness(self, value):
        if not isinstance(value, (int, float)):
            raise ValueError(f"brightness must be a numeric value, received '{value}'")
        elif value < 0 or value > 100:
            raise ValueError(
                f"brightness must be a number between 0 and 100, received '{value}'"
            )

        self.options.brightness = value
