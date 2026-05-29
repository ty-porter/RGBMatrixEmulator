import numpy as np

from RGBMatrixEmulator.pixel_mappers import PixelMapper


class StackToRowMapper(PixelMapper):
    """
    Lay parallel chains end-to-end as one wide horizontal row.

    Based on rpi-rgb-led-matrix's StackToRowMapper ("StackToRow"). This changes
    the aspect of the drawn image but the emulator does not model physical
    layout, so it is otherwise unchanged.
    """

    def __init__(self, chain_length: int = 1, parallel: int = 1):
        self.chain_length = chain_length
        self.bands = max(parallel, 1)

    def get_size_mapping(self, base_w: int, base_h: int) -> tuple[int, int]:
        return (base_w * self.bands, base_h // self.bands)

    def map_visible_to_screen(
        self, screen_w: int, screen_h: int, vx: np.ndarray, vy: np.ndarray
    ) -> tuple[np.ndarray, np.ndarray]:
        return (vx, vy)
