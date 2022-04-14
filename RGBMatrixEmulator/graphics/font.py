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

    def CharacterWidth(self, char):
        if self.bdf_font == None:
            return 0

        if not self.bdf_font.glyphbycp(char):
            return self.headers['fbbx']

        return self.bdf_font.glyphbycp(char).meta['dwx0']

    @property
    def height(self):
        if self.bdf_font is None: return -1
        return self.headers['fbby']

    @property
    def baseline(self):
        if self.bdf_font is None: return 0
        return self.headers['fbby'] + self.headers['fbbyoff']
