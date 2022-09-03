from RGBMatrixEmulator.graphics.color import Color
from RGBMatrixEmulator.graphics.font import Font


def DrawText(canvas, font, x, y, color, text):
    # Early return for empty string prevents bugs in bdfparser library
    # and makes good sense anyway
    if len(text) == 0:
        return

    # Support multiple spacings based on device width
    character_widths = [font.CharacterWidth(ord(letter)) for letter in text]
    first_char_width = character_widths[0]
    max_char_width = max(character_widths)
    total_width = sum(character_widths)

    # Offscreen to the left, adjust by first character width
    if x < 0:
        adjustment = abs(x + first_char_width) // first_char_width
        text = text[adjustment:]
        if adjustment:
            x += first_char_width * adjustment

    # Offscreen to the right, rough adjustment by max width
    if (total_width + x) > canvas.width:
        text = text[: ((canvas.width + 1) // max_char_width) + 2]

    # Draw the text!
    if len(text) != 0:
        # Ensure text doesn't get drawn as multiple lines
        linelimit = len(text) * (font.headers['fbbx'] + 1)

        text_map = font.bdf_font.draw(text, linelimit, missing=font.default_character).todata(2)
        font_y_offset = -(font.headers['fbby'] + font.headers['fbbyoff'])

        for y2, row in enumerate(text_map):
            for x2, value in enumerate(row):
                if value == 1:
                    try:
                        if isinstance(color, tuple):
                            canvas.SetPixel(x + x2, y + y2 + font_y_offset, *color)
                        else:
                            canvas.SetPixel(x + x2, y + y2 + font_y_offset, color.red, color.green, color.blue)
                    except Exception:
                        pass

    return total_width

def DrawLine(canvas, x1, y1, x2, y2, color):
    int_points = __coerce_int(x1, y1, x2, y2)
    rows, cols = __line(*int_points)

    for point in zip(rows, cols):
        canvas.SetPixel(*point, color.red, color.green, color.blue)

def DrawCircle(canvas, x, y, r, color):
    int_points = __coerce_int(x, y)
    rows, cols = __circle_perimeter(*int_points, r)

    for point in zip(rows, cols):
        canvas.SetPixel(*point, color.red, color.green, color.blue)

def __coerce_int(*values):
    return [int(value) for value in values]

def __line(x1, y1, x2, y2):
    '''
    Line drawing algorithm

    Extracted from scikit-image:
    https://github.com/scikit-image/scikit-image/blob/00177e14097237ef20ed3141ed454bc81b308f82/skimage/draw/_draw.pyx#L44
    '''
    steep = 0
    r = x1
    c = y1
    dr = abs(x2 - x1)
    dc = abs(y2 - y1)

    rr = [0] * (max(dc, dr) + 1)
    cc = [0] * (max(dc, dr) + 1)

    if (y2 - c) > 0:
        sc = 1
    else:
        sc = -1
    if (x2 - r) > 0:
        sr = 1
    else:
        sr = -1
    if dr > dc:
        steep = 1
        c, r = r, c
        dc, dr = dr, dc
        sc, sr = sr, sc
    d = (2 * dr) - dc

    for i in range(dc):
        if steep:
            rr[i] = c
            cc[i] = r
        else:
            rr[i] = r
            cc[i] = c
        while d >= 0:
            r = r + sr
            d = d - (2 * dc)
        c = c + sc
        d = d + (2 * dr)

    rr[dc] = x2
    cc[dc] = y2

    return (rr, cc)

def __circle_perimeter(x, y, radius):
    '''
    Bresenham circle algorithm
    
    Extracted from scikit-image
    https://github.com/scikit-image/scikit-image/blob/00177e14097237ef20ed3141ed454bc81b308f82/skimage/draw/_draw.pyx#L248
    '''
    rr = list()
    cc = list()

    c = 0
    r = radius
    d = 3 - 2 * radius

    while r >= c:
        rr.extend([_ + x for _ in [r, -r, r, -r, c, -c, c, -c]])
        cc.extend([_ + y for _ in [c, c, -c, -c, r, r, -r, -r]])

        if d < 0:
            d += 4 * c + 6
        else:
            d += 4 * (c - r) + 10
            r -= 1
        c += 1

    return (rr, cc)
