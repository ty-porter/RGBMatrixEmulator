#!/usr/bin/env python
# Example of flipping between multiple canvases.
# Could be useful for double buffering purposes.
from samplebase import SampleBase
from RGBMatrixEmulator import graphics


class MultCanvas(SampleBase):
    def __init__(self, *args, **kwargs):
        super(MultCanvas, self).__init__(*args, **kwargs)

    def run(self):
        canvas1 = self.matrix.CreateFrameCanvas()
        canvas2 = self.matrix.CreateFrameCanvas()

        font = graphics.Font()
        font.LoadFont("./fonts/7x13.bdf")
        textColor = graphics.Color(255, 255, 0)

        i = 0
        j = 0
        while True:

            for num, canvas in enumerate([canvas1, canvas2]):

                i = 0

                while i < 50:
                    canvas.Clear()
                    graphics.DrawText(canvas, font, 10, 10, textColor, str(num))
                    self.matrix.SwapOnVSync(canvas)

                    i += 1


# Main function
if __name__ == "__main__":
    mc = MultCanvas()
    if (not mc.process()):
        mc.print_help()
