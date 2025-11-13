#!/usr/bin/env python
from samplebase import SampleBase
import random


class Static(SampleBase):
    def run(self):
        canvas = self.matrix.CreateFrameCanvas()

        while 1:
            for y in range(canvas.height):
                for x in range(canvas.width):
                    static = [random.randrange(0, 255)] * 3
                    canvas.SetPixel(x, y, *static)
            
            self.matrix.SwapOnVSync(canvas)

if __name__ == "__main__":
    static = Static()

    static.process()
