class Color:
    def __init__(self, r: int = 0, g: int = 0, b: int = 0) -> None:
        # Simulate Cython uint8_t bounds checking
        for c in (r, g, b):
            if c > 255:
                raise OverflowError("value too large to convert to uint8_t")

            if c < 0:
                raise OverflowError("can't convert negative value to uint8_t")

        self.red = r
        self.green = g
        self.blue = b
