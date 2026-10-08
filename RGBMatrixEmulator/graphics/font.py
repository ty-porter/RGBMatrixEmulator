from typing import Optional

from RGBMatrixEmulator.emulation.canvas import Canvas
from RGBMatrixEmulator.graphics.color import Color
from RGBMatrixEmulator.internal.bdf_font import BDFFont

# Unicode replacement character, drawn in place of glyphs the font doesn't have
REPLACEMENT_CODEPOINT = 0xFFFD


class Font:
    _bdf_font: Optional[BDFFont] = None

    def LoadFont(self, file: str) -> None:
        try:
            self._bdf_font = BDFFont.load(file)
        except (OSError, BDFFont.UnsupportedFontVersion, BDFFont.ParseError) as e:
            raise Exception("Couldn't load font " + file) from e

    def CharacterWidth(self, char: int) -> int:
        glyph = self._glyph(char)

        # Missing glyphs return -1 in rpi-rgb-led-matrix
        if glyph is None:
            return -1

        return glyph.DWIDTH[0]

    def DrawGlyph(self, c: Canvas, x: int, y: int, color: Color, char: int) -> int:
        """Draws a single glyph with its baseline at y. Returns the advance width."""
        glyph = self._glyph(char) or self._glyph(REPLACEMENT_CODEPOINT)

        if glyph is None:
            return 0

        width, height, x_offset, y_offset = glyph.BBX
        advance = glyph.DWIDTH[0]
        top = y - height - y_offset

        for row_index, row in enumerate(glyph.BITMAP):
            for col in range(width):
                # Pixels past the advance width are dropped
                if x_offset + col >= advance:
                    break

                if (row >> (glyph.BITMAP_ROW_BITS - 1 - col)) & 1:
                    c.SetPixel(
                        x + x_offset + col,
                        top + row_index,
                        color.red,
                        color.green,
                        color.blue,
                    )

        return advance

    @property
    def height(self) -> int:
        if self._bdf_font is None:
            return -1
        return self._bdf_font.FONTBOUNDINGBOX[1]

    @property
    def baseline(self) -> int:
        if self._bdf_font is None:
            return 0
        _, height, _, y_offset = self._bdf_font.FONTBOUNDINGBOX
        return height + y_offset

    def _glyph(self, codepoint: int) -> Optional[BDFFont.Glyph]:
        if self._bdf_font is None:
            return None

        return self._bdf_font._cp_to_glyph.get(codepoint)
