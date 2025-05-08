class Color:
    def __init__(self, r=0, g=0, b=0):
        # Simulate Cython uint8_t bounds checking
        for c in (r, g, b):
            if c > 255:
                raise OverflowError("value too large to convert to uint8_t")

            if c < 0:
                raise OverflowError("can't convert negative value to uint8_t")

        self.red = r
        self.green = g
        self.blue = b

    @classmethod
    def adjust_brightness(cls, pixel, alpha, to_int=False):
        if to_int:
            return tuple(int(channel) for channel in pixel)

        return tuple(channel * alpha for channel in pixel)

    @classmethod
    def to_hex(cls, pixel):
        return "#%02x%02x%02x" % pixel

    @classmethod
    def BLACK(cls):
        return (0, 0, 0)

    @classmethod
    def RED(cls):
        return (255, 0, 0)

    @classmethod
    def GREEN(cls):
        return (0, 255, 0)

    @classmethod
    def BLUE(cls):
        return (0, 0, 255)
