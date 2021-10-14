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

        return self.bdf_font.glyphbycp(char).meta['dwx0']
