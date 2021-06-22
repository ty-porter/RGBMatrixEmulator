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

