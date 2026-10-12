import os
import tempfile
import unittest

from RGBMatrixEmulator.graphics.color import Color
from RGBMatrixEmulator.graphics.font import Font
from RGBMatrixEmulator.internal.bdf_font import BDFFont

# 4x6 font with one glyph ("A", U+0041) whose bitmap is a 4x6 box with a diagonal
TEST_BDF = """STARTFONT 2.1
FONT -test-Fixed-Medium-R-Normal--6-60-75-75-C-40-ISO10646-1
SIZE 6 75 75
FONTBOUNDINGBOX 4 6 0 -1
STARTPROPERTIES 1
CHARSET_REGISTRY "ISO10646"
ENDPROPERTIES
CHARS 1
STARTCHAR A
ENCODING 65
SWIDTH 666 0
DWIDTH 4 0
BBX 4 6 0 -1
BITMAP
F0
80
90
A0
C0
F0
ENDCHAR
ENDFONT
"""


class FakeCanvas:
    def __init__(self):
        self.pixels = {}

    def SetPixel(self, x, y, r, g, b):
        self.pixels[(x, y)] = (r, g, b)


class TestFontParsing(unittest.TestCase):
    def setUp(self):
        fd, self.path = tempfile.mkstemp(suffix=".bdf")
        with os.fdopen(fd, "w") as fp:
            fp.write(TEST_BDF)

        self.addCleanup(os.remove, self.path)

    def test_bdf_parse(self):
        bdf = BDFFont.load(self.path)

        self.assertEqual(bdf.FONTBOUNDINGBOX, (4, 6, 0, -1))
        self.assertEqual(bdf.CHARS, 1)
        self.assertEqual(bdf.PROPERTIES["CHARSET_REGISTRY"], "ISO10646")

        glyph = bdf._cp_to_glyph[ord("A")]
        self.assertEqual(glyph.NAME, "A")
        self.assertEqual(glyph.DWIDTH, (4, 0))
        self.assertEqual(glyph.BBX, (4, 6, 0, -1))
        self.assertEqual(glyph.BITMAP, [0xF0, 0x80, 0x90, 0xA0, 0xC0, 0xF0])

    def test_font_metrics(self):
        font = Font()
        font.LoadFont(self.path)

        self.assertEqual(font.width, 4)
        self.assertEqual(font.height, 6)
        self.assertEqual(font.baseline, 5)
        self.assertEqual(font.CharacterWidth(ord("A")), 4)
        self.assertEqual(font.CharacterWidth(ord("Z")), -1)

    def test_draw_glyph(self):
        font = Font()
        font.LoadFont(self.path)
        canvas = FakeCanvas()

        advance = font.DrawGlyph(canvas, 10, 20, Color(1, 2, 3), ord("A"))

        self.assertEqual(advance, 4)

        # Baseline at y=20, bbox y offset -1 => glyph rows span y=15..20
        expected_rows = {
            15: [0, 1, 2, 3],
            16: [0],
            17: [0, 3],
            18: [0, 2],
            19: [0, 1],
            20: [0, 1, 2, 3],
        }
        expected = {
            (10 + col, y): (1, 2, 3) for y, cols in expected_rows.items() for col in cols
        }

        self.assertEqual(canvas.pixels, expected)

    def test_missing_font_file(self):
        with self.assertRaises(Exception):
            Font().LoadFont(self.path + ".missing")

    def test_unsupported_version(self):
        with open(self.path, "w") as fp:
            fp.write("STARTFONT 1.0\nENDFONT\n")

        with self.assertRaises(Exception):
            Font().LoadFont(self.path)


if __name__ == "__main__":
    unittest.main()
