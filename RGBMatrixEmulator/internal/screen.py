import numpy as np

from RGBMatrixEmulator.pixel_mappers import get_pixel_mapper


class Screen:
    """
    The emulated screen: how a program's drawn canvas is mapped into the
    displayed window.

    It resolves the configured pixel mapper once and snapshots the resulting
    geometry. The pipeline is:

      pixel_buffer_size  --(LUT)-->  screen_size  --(x pixel_size)-->  scaled

    Both sizes here are in LED units; scaling to on-screen pixels by pixel_size
    is a rendering concern owned by the display adapter.

      pixel_buffer_size  -- what the program draws into (SetPixel/SetImage),
                            and the size reported as RGBMatrix.width/height
      screen_size        -- what the screen shows after the mapper's LUT; a
                            content transform may change the aspect (e.g. a 90
                            degree rotation), so this can differ from the buffer
    """

    def __init__(self, options) -> None:
        base_w = options.cols * options.chain_length
        base_h = options.rows * options.parallel

        mapper = get_pixel_mapper(
            options.pixel_mapper_config, options.chain_length, options.parallel
        )

        self.pixel_buffer_size = mapper.get_size_mapping(base_w, base_h)
        self._lut, self.screen_size = mapper.build_lut(*self.pixel_buffer_size)

    def render(self, pixels: np.ndarray) -> np.ndarray:
        """Map a pixel buffer to screen pixels via the mapper's LUT."""
        if self._lut is None:
            return pixels

        vy_lut, vx_lut = self._lut

        return pixels[vy_lut, vx_lut]
