import numpy as np

from RGBMatrixEmulator.pixel_mappers import PixelMapper


class IdentityMapper(PixelMapper):
    """No-op mapper. The drawn canvas and the displayed screen are identical."""

    def get_size_mapping(self, base_w: int, base_h: int) -> tuple[int, int]:
        return (base_w, base_h)

    def map_visible_to_screen(
        self, screen_w: int, screen_h: int, vx: np.ndarray, vy: np.ndarray
    ) -> tuple[np.ndarray, np.ndarray]:
        return (vx, vy)
