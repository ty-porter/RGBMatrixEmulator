from bresenham import bresenham

from RGBMatrixEmulator.graphics.color import Color
from RGBMatrixEmulator.graphics.font import Font

def DrawText(canvas, font, x, y, color, text):
    text_map = font.bdf_font.draw(text).todata(2)
    font_y_offset = -(font.bdf_font.headers['fbby'] + font.bdf_font.headers['fbbyoff'])

    for y2, row in enumerate(text_map):
        for x2, value in enumerate(row):
            if value == 1:
                try:
                    if isinstance(color, tuple):
                        canvas.SetPixel(x + x2, y + y2 + font_y_offset, *color)
                    else:
                        canvas.SetPixel(x + x2, y + y2 + font_y_offset, color.r, color.g, color.b)
                except Exception:
                    pass

    return len(text_map[0]) * font.bdf_font.headers['fbbx']

def DrawLine(canvas, x1, y1, x2, y2, color):
    int_points = __coerce_int(x1, y1, x2, y2)
    line_points = list(bresenham(*int_points))

    for point in line_points:
        canvas.SetPixel(*point, color.r, color.g, color.b)


def DrawCircle(canvas, x1, y1, r, color):
    # This needs to be implemented!
    pass

def __coerce_int(*values):
    return [int(value) for value in values]