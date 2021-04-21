class Color:
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

    def adjust_brightness(self, alpha):
        # Super hacky, pygame.draw.rect() doesn't support alpha blending
        self.r *= alpha
        self.g *= alpha
        self.b *= alpha

    def to_tuple(self):
        return (self.r, self.g, self.b)

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
