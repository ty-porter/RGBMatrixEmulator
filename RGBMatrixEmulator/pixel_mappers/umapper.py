import numpy as np

from RGBMatrixEmulator.pixel_mappers import PixelMapper


class UMapper(PixelMapper):
    """
    U-arrangement mapper: a long chain folded back on itself into a U.

    Based on rpi-rgb-led-matrix's UArrangementMapper ("U-mapper"). This is an
    arrangement mapper: the fold makes a long chain into a squarer block, but
    the physical placement is what the viewer sees, so on-screen content is
    unchanged -- only the aspect changes.

    Requires an even chain of at least 2 panels; the upstream wiring caveats are
    not modeled since the emulator only cares about the resulting screen.
    """

    def __init__(self, chain_length: int = 1, parallel: int = 1):
        self.chain_length = chain_length
        self.parallel = parallel

    def get_size_mapping(self, base_w: int, base_h: int) -> tuple[int, int]:
        return (base_w // 2, base_h * 2)

    def map_visible_to_screen(
        self, screen_w: int, screen_h: int, vx: np.ndarray, vy: np.ndarray
    ) -> tuple[np.ndarray, np.ndarray]:
        return (vx, vy)
