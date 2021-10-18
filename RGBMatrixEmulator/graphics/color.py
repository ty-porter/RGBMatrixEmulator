class Color:
    def __init__(self, r, g, b):
        self.red = r
        self.green = g
        self.blue = b

    def adjust_brightness(self, alpha):
        # Super hacky, pygame.draw.rect() doesn't support alpha blending
        self.red *= alpha
        self.green *= alpha
        self.blue *= alpha

    def to_tuple(self):
        return (self.red, self.green, self.blue)

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
