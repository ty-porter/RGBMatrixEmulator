from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterator, Optional, Tuple, Union
from RGBMatrixEmulator.logger import Logger

# Keywords from the BDF spec that aren't needed for this library.
_IGNORED_KEYWORDS = {
    "COMMENT",
    "CONTENTVERSION",
    "METRICSSET",
    "SWIDTH1",
    "DWIDTH1",
    "VVECTOR",
}


def _split(raw: str) -> Tuple[str, str]:
    keyword, _, args = raw.strip().partition(" ")
    return keyword, args.strip()


def _ints(args: str) -> Tuple[int, ...]:
    return tuple(int(x) for x in args.split())


class BDFFont:
    """Minimal BDF (Glyph Bitmap Distribution Format) parser. Supports STARTFONT 2.x."""

    class UnsupportedFontVersion(Exception):
        pass

    class ParseError(Exception):
        pass

    @dataclass
    class Glyph:
        NAME: str
        ENCODING: int = -1
        SWIDTH: Tuple[int, ...] = ()
        DWIDTH: Tuple[int, ...] = ()
        BBX: Tuple[int, ...] = ()
        ATTRIBUTES: Optional[str] = None
        BITMAP: list = field(default_factory=list)
        BITMAP_ROW_BITS: int = 0

    # Keyword -> handler method name for top-level (font) lines.
    _FONT_HANDLERS = {
        "FONT": "_parse_font",
        "SIZE": "_parse_size",
        "FONTBOUNDINGBOX": "_parse_fontboundingbox",
        "STARTPROPERTIES": "_parse_properties",
        "CHARS": "_parse_chars",
        "STARTCHAR": "_parse_char",
    }

    # Keyword -> handler method name for lines inside a STARTCHAR block.
    _GLYPH_HANDLERS = {
        "ENCODING": "_parse_encoding",
        "SWIDTH": "_parse_swidth",
        "DWIDTH": "_parse_dwidth",
        "BBX": "_parse_bbx",
        "ATTRIBUTES": "_parse_attributes",
        "BITMAP": "_parse_bitmap",
    }

    FONT: str
    SIZE: Tuple[int, ...]
    FONTBOUNDINGBOX: Tuple[int, ...]
    CHARS: int

    def __init__(self):
        self.PROPERTIES: dict[str, Union[int, str]] = {}
        self._encoding_to_glyph: dict[int, BDFFont.Glyph] = {}
        self._cp_to_glyph: dict[int, BDFFont.Glyph] = {}
        self._name_to_glyph: dict[str, BDFFont.Glyph] = {}
        self._parsed_chars = 0

    @classmethod
    def load(cls, path) -> BDFFont:
        font = cls()

        # BDF is nominally ASCII, but comments/copyright often contain 8-bit text.
        with open(path, encoding="latin-1") as fp:
            lines = iter(fp)

            header = next(lines, "").strip()
            if not header.startswith("STARTFONT 2"):
                raise cls.UnsupportedFontVersion(
                    f"BDF font parsing supports 'STARTFONT 2.x' only, got '{header}'"
                )

            for raw in lines:
                keyword, args = _split(raw)

                if keyword == "ENDFONT":
                    break

                font._dispatch(cls._FONT_HANDLERS, keyword, args, lines)
            else:
                raise cls.ParseError("Reached end of file without ENDFONT")

        if hasattr(font, "CHARS") and font.CHARS != font._parsed_chars:
            Logger.warning(
                "Font declares %d chars but %d were parsed",
                font.CHARS,
                font._parsed_chars,
            )

        return font

    def _dispatch(
        self, handlers: dict, keyword: str, args: str, lines: Iterator[str], *extra
    ) -> None:
        name = handlers.get(keyword)

        if name is None:
            if keyword and keyword not in _IGNORED_KEYWORDS:
                Logger.warning("Unknown BDF keyword: %s", keyword)
            return

        try:
            getattr(self, name)(args, lines, *extra)
        except (ValueError, IndexError) as e:
            raise self.ParseError(f"Failed to parse '{keyword} {args}'") from e

    # Font-level handlers

    def _parse_font(self, args: str, _lines: Iterator[str]) -> None:
        self.FONT = args

    def _parse_size(self, args: str, _lines: Iterator[str]) -> None:
        self.SIZE = _ints(args)

    def _parse_fontboundingbox(self, args: str, _lines: Iterator[str]) -> None:
        self.FONTBOUNDINGBOX = _ints(args)

    def _parse_chars(self, args: str, _lines: Iterator[str]) -> None:
        self.CHARS = int(args)

    def _parse_properties(self, args: str, lines: Iterator[str]) -> None:
        expected = int(args)
        parsed = 0

        for raw in lines:
            line = raw.strip()

            if line == "ENDPROPERTIES":
                if parsed != expected:
                    Logger.warning("Expected %d properties, got %d", expected, parsed)
                return

            if not line or line.startswith("COMMENT"):
                continue

            name, _, value = line.partition(" ")
            value = value.strip()

            if value.startswith('"'):
                # Strings are quoted, with embedded quotes doubled.
                value = value[1:-1].replace('""', '"')
            else:
                value = int(value)

            self.PROPERTIES[name] = value
            parsed += 1

        raise self.ParseError("Reached end of file without ENDPROPERTIES")

    def _parse_char(self, args: str, lines: Iterator[str]) -> None:
        glyph = BDFFont.Glyph(NAME=args)

        for raw in lines:
            keyword, glyph_args = _split(raw)

            if keyword == "ENDCHAR":
                self._register(glyph)
                return

            self._dispatch(self._GLYPH_HANDLERS, keyword, glyph_args, lines, glyph)

        raise self.ParseError(
            f"Reached end of file without ENDCHAR (glyph '{glyph.NAME}')"
        )

    def _register(self, glyph: BDFFont.Glyph) -> None:
        self._parsed_chars += 1
        self._name_to_glyph[glyph.NAME] = glyph

        # ENCODING -1 means the glyph is unencoded; reachable by name only.
        if glyph.ENCODING < 0:
            return

        self._encoding_to_glyph[glyph.ENCODING] = glyph

        # Encoding is a Unicode codepoint only for ISO10646 fonts (or when unspecified).
        registry = str(self.PROPERTIES.get("CHARSET_REGISTRY", "ISO10646")).upper()
        if registry.startswith("ISO10646"):
            self._cp_to_glyph[glyph.ENCODING] = glyph

    # Glyph-level handlers

    def _parse_encoding(
        self, args: str, _lines: Iterator[str], glyph: BDFFont.Glyph
    ) -> None:
        # "ENCODING n" or "ENCODING -1 n"
        glyph.ENCODING = int(args.split()[0])

    def _parse_swidth(
        self, args: str, _lines: Iterator[str], glyph: BDFFont.Glyph
    ) -> None:
        glyph.SWIDTH = _ints(args)

    def _parse_dwidth(
        self, args: str, _lines: Iterator[str], glyph: BDFFont.Glyph
    ) -> None:
        glyph.DWIDTH = _ints(args)

    def _parse_bbx(
        self, args: str, _lines: Iterator[str], glyph: BDFFont.Glyph
    ) -> None:
        glyph.BBX = _ints(args)

    def _parse_attributes(
        self, args: str, _lines: Iterator[str], glyph: BDFFont.Glyph
    ) -> None:
        glyph.ATTRIBUTES = args

    def _parse_bitmap(
        self, _args: str, lines: Iterator[str], glyph: BDFFont.Glyph
    ) -> None:
        if len(glyph.BBX) != 4:
            raise self.ParseError(f"BITMAP before BBX (glyph '{glyph.NAME}')")

        # BITMAP is followed by exactly BBX height rows, one hex string per row.
        height = glyph.BBX[1]
        glyph.BITMAP = []

        for _ in range(height):
            row = next(lines, None)
            if row is None:
                raise self.ParseError(
                    f"Reached end of file inside BITMAP (glyph '{glyph.NAME}')"
                )

            row = row.strip()
            glyph.BITMAP.append(int(row, 16))
            glyph.BITMAP_ROW_BITS = len(row) * 4
