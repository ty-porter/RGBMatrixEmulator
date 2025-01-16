#!/usr/bin/env python
import time
from samplebase import SampleBase
from PIL import Image


class ImageBrightness(SampleBase):
    def __init__(self, *args, **kwargs):
        super(ImageBrightness, self).__init__(*args, **kwargs)
        self.parser.add_argument("-i", "--image", help="The image to display", default="./images/raspberry.ppm")

    def run(self):
        if not 'image' in self.__dict__:
            self.image = Image.open(self.args.image).convert('RGB')
        self.image.resize((self.matrix.width, self.matrix.height), Image.LANCZOS)

        canvas = self.matrix.CreateFrameCanvas()

        while True:
            canvas.SetImage(self.image, 0)

            if canvas.brightness == 0:
                canvas.brightness = 100

            canvas.brightness -= 1

            canvas = self.matrix.SwapOnVSync(canvas)
            time.sleep(0.01)

if __name__ == "__main__":
    image_scroller = ImageBrightness()
    if (not image_scroller.process()):
        image_scroller.print_help()
