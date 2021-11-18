from RGBMatrixEmulator.emulators.canvas import Canvas


class RGBMatrix:
    def __init__(self, options = {}):
        self.options = options

        self.width = options.cols * options.chain_length
        self.height = options.rows * options.parallel
        self.brightness = options.brightness

        self.canvas = None

    def CreateFrameCanvas(self):
        if self.canvas:
            return self.canvas

        return Canvas(options = self.options)
    
    def SwapOnVSync(self, canvas):
        canvas.check_for_quit_event()
        canvas.draw_to_screen()

        return canvas

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
            self.canvas = Canvas(options = self.options)

        self.canvas.display_adapter.options.brightness = self.brightness