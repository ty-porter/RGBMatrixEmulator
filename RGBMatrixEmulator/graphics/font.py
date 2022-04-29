import bdfparser


class Font:
    def __init__(self):
        self.bdf_font = None
        self.headers = {}
        self.spacing = {}

    def LoadFont(self, path):
        self.bdf_font = bdfparser.Font(path)
        self.headers = self.bdf_font.headers
        self.props = self.bdf_font.props

        # All rpi-rgb-led-matrix fonts have a character at 0xFFFD to represent a missing character
        # Cache this for use later so we don't have to constantly look it up
        self.default_character = self.bdf_font.glyphbycp(0xFFFD)

    def CharacterWidth(self, char):
        # Missing glyphs return 0 width in rpi-rgb-led-matrix
        if self.bdf_font == None or not self.bdf_font.glyphbycp(char):
            return 0

        return self.bdf_font.glyphbycp(char).meta['dwx0']

    @property
    def height(self):
        if self.bdf_font is None: return -1
        return self.headers['fbby']

    @property
    def baseline(self):
        if self.bdf_font is None: return 0
        return self.headers['fbby'] + self.headers['fbbyoff']
