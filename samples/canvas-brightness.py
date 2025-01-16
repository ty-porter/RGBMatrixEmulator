#!/usr/bin/env python
from samplebase import SampleBase


class CanvasBrightness(SampleBase):
    def __init__(self, *args, **kwargs):
        super(CanvasBrightness, self).__init__(*args, **kwargs)

    def run(self):
        canvas = self.matrix.CreateFrameCanvas()
        channel = 255
        count = 0

        while True:
            if count % 4 == 0:
                canvas.Fill(channel, 0, 0)
            elif count % 4 == 1:
                canvas.Fill(0, channel, 0)
            elif count % 4 == 2:
                canvas.Fill(0, 0, channel)
            elif count % 4 == 3:
                canvas.Fill(channel, channel, channel)

            if canvas.brightness == 0:
                canvas.brightness = 100
                count += 1

            canvas.brightness -= 1

            self.matrix.SwapOnVSync(canvas)

            self.usleep(20 * 1000)

# Main function
if __name__ == "__main__":
    grayscale_block = CanvasBrightness()
    if (not grayscale_block.process()):
        grayscale_block.print_help()
