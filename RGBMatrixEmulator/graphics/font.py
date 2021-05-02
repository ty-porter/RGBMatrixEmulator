import os
import bdfparser


class Font:
    def __init__(self):
        self.bdf_font = None

    def LoadFont(self, path):
        self.bdf_font = bdfparser.Font(path)

