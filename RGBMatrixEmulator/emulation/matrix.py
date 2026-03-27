from PIL import Image

from RGBMatrixEmulator.emulation.canvas import Canvas
from RGBMatrixEmulator.emulation.options import RGBMatrixOptions


class RGBMatrix:
    def __init__(self, options: RGBMatrixOptions = RGBMatrixOptions()) -> None:
        self.options = options

        self.width = options.cols * options.chain_length
        self.height = options.rows * options.parallel

    def CreateFrameCanvas(self) -> Canvas:
        self.canvas = Canvas(options=self.options)

        return self.canvas

    # TODO: framerate_fraction support not yet implemented
    # https://github.com/hzeller/rpi-rgb-led-matrix/commit/f88355e46faafb9de7f1e59dd258ab36c7e7b097
    def SwapOnVSync(self, canvas: Canvas, framerate_fraction: int = 1) -> Canvas:
        canvas.check_for_quit_event()
        canvas.draw_to_screen()
        self.canvas = canvas

        return self.canvas

    def Clear(self) -> None:
        self.__sync_canvas()
        self.canvas.Clear()
        self.SwapOnVSync(self.canvas)

    def Fill(self, r: int, g: int, b: int) -> None:
        self.__sync_canvas()
        self.canvas.Fill(r, g, b)
        self.SwapOnVSync(self.canvas)

    def SetPixel(self, x: int, y: int, r: int, g: int, b: int) -> None:
        self.__sync_canvas()
        self.canvas.SetPixel(x, y, r, g, b)
        self.SwapOnVSync(self.canvas)

    def SetImage(
        self,
        image: Image.Image,
        offset_x: int = 0,
        offset_y: int = 0,
        unsafe: bool = True,
    ) -> None:
        self.__sync_canvas()
        self.canvas.SetImage(image, offset_x, offset_y, unsafe)
        self.SwapOnVSync(self.canvas)

    def __sync_canvas(self) -> None:
        if not self.canvas:
            self.canvas = Canvas(options=self.options)

    @property
    def brightness(self) -> int:
        return self.options.brightness

    @brightness.setter
    def brightness(self, value: int) -> None:
        if not isinstance(value, (int, float)):
            raise ValueError(f"brightness must be a numeric value, received '{value}'")
        elif value < 0 or value > 100:
            raise ValueError(
                f"brightness must be a number between 0 and 100, received '{value}'"
            )

        self.options.brightness = value
