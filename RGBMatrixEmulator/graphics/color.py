class Color:
    def __init__(self, r = 0, g = 0, b = 0):
        self.red   = r
        self.green = g
        self.blue  = b

    def adjust_brightness(self, alpha, to_int = False):
        self.red   *= alpha
        self.green *= alpha
        self.blue  *= alpha

        if to_int:
            self.red   = int(self.red)
            self.green = int(self.green)
            self.blue  = int(self.blue)

    def to_tuple(self):
        return (int(self.red), int(self.green), int(self.blue))

    def to_hex(self):
        return "#%02x%02x%02x" % self.to_tuple()

    @classmethod
    def BLACK(cls):
        return Color(0, 0, 0)

    @classmethod
    def RED(cls):
        return Color(255, 0, 0)

    @classmethod
    def GREEN(cls):
        return Color(0, 255, 0)

    @classmethod
    def BLUE(cls):
        return Color(0, 0, 255)
