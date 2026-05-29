import numpy as np

from RGBMatrixEmulator.pixel_mappers import PixelMapper


class StackToRowMapper(PixelMapper):
    """
    Lay parallel chains end-to-end as one wide horizontal row.

    Based on rpi-rgb-led-matrix's StackToRowMapper ("StackToRow"). This is an
    arrangement mapper: stacked parallel bands are presented side by side, but
    the physical placement is what the viewer sees, so on-screen content is
    unchanged -- only the aspect changes. The "Z"/"F" band-flip parameters are
    cabling concerns the emulator does not model.
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
