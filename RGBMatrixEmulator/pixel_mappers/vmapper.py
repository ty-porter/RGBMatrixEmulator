import numpy as np

from RGBMatrixEmulator.pixel_mappers import PixelMapper


class VMapper(PixelMapper):
    """
    Vertical mapper: a horizontal chain folded into vertical panel stacks.

    Based on rpi-rgb-led-matrix's VerticalMapper ("V-mapper"). This changes
    the aspect of the drawn image but the emulator does not model physical
    layout, so it is otherwise unchanged.
    """

    def __init__(self, chain_length: int = 1, parallel: int = 1, z: bool = False):
        self.chain_length = chain_length
        self.parallel = parallel
        self.z = z

    def get_size_mapping(self, base_w: int, base_h: int) -> tuple[int, int]:
        screen_w = base_w * self.parallel // self.chain_length
        screen_h = base_h * self.chain_length // self.parallel
        return (screen_w, screen_h)

    def map_visible_to_screen(
        self, screen_w: int, screen_h: int, vx: np.ndarray, vy: np.ndarray
    ) -> tuple[np.ndarray, np.ndarray]:
        return (vx, vy)
