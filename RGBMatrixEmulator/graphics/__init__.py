from skimage.draw import line as sk_line
from skimage.draw import circle_perimeter as sk_circle_perimeter

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

        text_map = font.bdf_font.draw(text, linelimit).todata(2)
        font_y_offset = -(font.headers['fbby'] + font.headers['fbbyoff'])

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

    return total_width

def DrawLine(canvas, x1, y1, x2, y2, color):
    int_points = __coerce_int(x1, y1, x2, y2)
    rows, cols = sk_line(*int_points)

    for point in zip(rows, cols):
        canvas.SetPixel(*point, color.r, color.g, color.b)

def DrawCircle(canvas, x, y, r, color):
    int_points = __coerce_int(x, y)
    rows, cols = sk_circle_perimeter(*int_points, r)
    
    for point in zip(rows, cols):
        canvas.SetPixel(*point, color.r, color.g, color.b)

def __coerce_int(*values):
    return [int(value) for value in values]
