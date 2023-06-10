import os
import sys
import io
import libsixel as sixel

from PIL import Image, ImageDraw, ImageEnhance
from typing import List

from RGBMatrixEmulator.adapters.base import BaseAdapter
from RGBMatrixEmulator.graphics.color import Color


def enlarge_pixels(pixels: List[List[Color]], scale: int, outline: int) -> Image.Image:
    outline_color = '#000000'
    w, h = len(pixels[0]), len(pixels)
    iw, ih = w * scale, h * scale
    i = Image.new('RGBA', (iw, ih))
    d = ImageDraw.Draw(i)

    for y, row in enumerate(pixels):
        for x, color in enumerate(row):
            rx, ry = x * scale, y * scale
            ex, ey = rx + (scale - 1), ry + (scale - 1)
            # todo: support circles
            d.rectangle([(rx, ry), (ex, ey)], fill=color.to_tuple(), outline=outline_color, width=outline)

    brightness = ImageEnhance.Brightness(i)
    i = brightness.enhance(1.5)
    contrast = ImageEnhance.Contrast(i)
    i = contrast.enhance(0.8)

    return i


def encode_sixels(pixels: List[List[Color]], scale=4, outline=1) -> str:
    '''Encodes given Image to a sixel string.'''
    img = enlarge_pixels(pixels, scale, outline)
    img_data = img.convert('RGB').tobytes()
    width = img.width
    height = img.height
    with io.BytesIO() as buf:
        output = sixel.sixel_output_new(lambda data, buffer: buffer.write(data), buf)
        dither = sixel.sixel_dither_new(256)
        sixel.sixel_dither_initialize(dither, img_data, width, height, sixel.SIXEL_PIXELFORMAT_RGB888)
        sixel.sixel_encode(img_data, width, height, 1, dither, output)

        encoded = buf.getvalue().decode('ascii')

        sixel.sixel_dither_unref(dither)
        sixel.sixel_output_unref(output)

    return encoded

class SixelAdapter(BaseAdapter):
    def draw_to_screen(self, pixels):
        sixel = encode_sixels(pixels,
                              scale=self.options.pixel_size,
                              outline=self.options.pixel_outline)
        output = f"\033[H\n{sixel}\n"
        sys.stdout.write(output)

    def load_emulator_window(self):
        os.system('cls||clear')
        os.system('mode con: cols={} lines={}'.format(self.width * 2 + 5, self.height + 3))
