import numpy as np

from RGBMatrixEmulator.pixel_mappers import PixelMapper


class RotateMapper(PixelMapper):
    """
    Rotate the display by a multiple of 90 degrees.

    Based on rpi-rgb-led-matrix's RotatePixelMapper ("Rotate"). This is a
    content mapper: with panels in a normal upright arrangement the viewer sees
    the rotated image. At 90/270 degrees the rotation also swaps the aspect, so
    the drawn canvas and the displayed screen have transposed dimensions.
    """

    def __init__(self, angle: int = 0):
        if angle % 90 != 0:
            raise ValueError("Rotate angle must be a multiple of 90 degrees")
        self.angle = (angle + 360) % 360

    def get_size_mapping(self, base_w: int, base_h: int) -> tuple[int, int]:
        if self.angle % 180 == 0:
            return (base_w, base_h)
        return (base_h, base_w)

    def map_visible_to_screen(
        self, draw_w: int, draw_h: int, vx: np.ndarray, vy: np.ndarray
    ) -> tuple[np.ndarray, np.ndarray]:
        if self.angle == 90:
            return (draw_h - 1 - vy, vx)
        if self.angle == 180:
            return (draw_w - 1 - vx, draw_h - 1 - vy)
        if self.angle == 270:
            return (vy, draw_w - 1 - vx)
        return (vx, vy)
