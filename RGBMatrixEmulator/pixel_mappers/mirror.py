import numpy as np

from RGBMatrixEmulator.pixel_mappers import PixelMapper


class MirrorMapper(PixelMapper):
    """
    Mirror the display horizontally (default) or vertically.

    Vectorized port of rpi-rgb-led-matrix's MirrorPixelMapper ("Mirror").
    Parameter "H" mirrors left/right, "V" mirrors top/bottom. Size-preserving.
    """

    def __init__(self, horizontal: bool = True):
        self.horizontal = horizontal

    def get_size_mapping(self, base_w: int, base_h: int) -> tuple[int, int]:
        return (base_w, base_h)

    def map_visible_to_screen(
        self, screen_w: int, screen_h: int, vx: np.ndarray, vy: np.ndarray
    ) -> tuple[np.ndarray, np.ndarray]:
        if self.horizontal:
            return (screen_w - 1 - vx, vy)
        return (vx, screen_h - 1 - vy)
