import abc

import numpy as np

#: A gather LUT: a pair of integer index arrays (vy_lut, vx_lut), each shaped
#: like the screen, holding the visible coordinate that feeds each screen pixel.
#: Apply with ``screen_pixels = visible_pixels[vy_lut, vx_lut]``.
LUT = tuple[np.ndarray, np.ndarray]


class PixelMapper(abc.ABC):
    """
    A pixel mapper, modeled on rpi-rgb-led-matrix's PixelMapper.

    The emulator assumes panels are physically arranged as an upright,
    rectangular matrix (the common case; arbitrary layouts are not modeled).
    Under that assumption a mapper has two orthogonal effects:

    - it may *resize* the canvas relative to the base panel grid
      (``get_size_mapping`` -- V/U/StackToRow do this), and
    - it may *transform the content* the viewer sees within that size
      (``map_visible_to_screen`` -- Mirror/Rotate do this).

    The emulator never drives real LEDs, so the electrical wiring order is not
    modeled: mappers describe what ends up on screen, not the matrix layout.

    See docs/chainable-pixel-mappers.md.
    """

    @abc.abstractmethod
    def get_size_mapping(self, base_w: int, base_h: int) -> tuple[int, int]:
        """Return the screen (W, H) produced from the base panel grid size."""

    @abc.abstractmethod
    def map_visible_to_screen(
        self, draw_w: int, draw_h: int, vx: np.ndarray, vy: np.ndarray
    ) -> tuple[np.ndarray, np.ndarray]:
        """
        Map drawn coordinates to displayed-screen coordinates, elementwise.

        ``vx`` / ``vy`` are integer arrays of matching shape holding coordinates
        in the *drawn* canvas (the ``get_size_mapping`` size the user draws
        into). The return is a pair of same-shape arrays holding screen
        coordinates. ``draw_w`` / ``draw_h`` are the drawn-canvas dimensions.

        Arrangement mappers that only resize return their inputs unchanged. A
        content transform may change the aspect (e.g. a 90 degree rotation), in
        which case the displayed size differs from the drawn size; callers infer
        the displayed size from the output range.
        """

    def build_lut(self, draw_w: int, draw_h: int) -> tuple[LUT | None, tuple[int, int]]:
        """
        Compile this mapper's coordinate transform, over a drawn canvas of
        ``draw_w`` x ``draw_h``, into a gather LUT plus the resulting displayed
        (W, H).

        Both fall out of a single evaluation of ``map_visible_to_screen`` over
        the canvas: the displayed size is the bounding box of the outputs, and
        the LUT is their scatter-inversion (so ``pixels[vy_lut, vx_lut]`` gathers
        the right drawn pixel for each displayed pixel).

        The LUT is ``None`` when the transform is the identity (arrangement
        mappers, which only resize) so callers can skip remapping; the displayed
        size then equals the drawn size.
        """
        vy_grid, vx_grid = np.indices((draw_h, draw_w))
        sx, sy = self.map_visible_to_screen(draw_w, draw_h, vx_grid, vy_grid)

        # Identity content transform -> no remapping needed; display matches draw.
        if np.array_equal(sx, vx_grid) and np.array_equal(sy, vy_grid):
            return None, (draw_w, draw_h)

        display_w = int(sx.max()) + 1
        display_h = int(sy.max()) + 1

        vx_lut = np.empty((display_h, display_w), dtype=np.intp)
        vy_lut = np.empty((display_h, display_w), dtype=np.intp)
        vx_lut[sy, sx] = vx_grid
        vy_lut[sy, sx] = vy_grid

        return (vy_lut, vx_lut), (display_w, display_h)


def get_pixel_mapper(
    config: str, chain_length: int = 1, parallel: int = 1
) -> PixelMapper:
    """
    Build a single pixel mapper from a config string ("Name" or "Name:param").

    Composition (semicolon-separated chains) is not handled yet; only the first
    mapper in the string is used.
    """
    from RGBMatrixEmulator.pixel_mappers.identity import IdentityMapper
    from RGBMatrixEmulator.pixel_mappers.mirror import MirrorMapper
    from RGBMatrixEmulator.pixel_mappers.rotate import RotateMapper
    from RGBMatrixEmulator.pixel_mappers.stack_to_row import StackToRowMapper
    from RGBMatrixEmulator.pixel_mappers.umapper import UMapper
    from RGBMatrixEmulator.pixel_mappers.vmapper import VMapper

    if not config:
        return IdentityMapper()

    spec = config.split(";")[0].strip()
    name, _, param = spec.partition(":")
    key = name.lower().replace("-", "")
    param = param.strip()

    if key == "mirror":
        return MirrorMapper(horizontal=(param.upper() != "V"))
    if key == "rotate":
        return RotateMapper(angle=int(param) if param else 0)
    if key == "vmapper":
        return VMapper(chain_length, parallel, z=(param.upper() == "Z"))
    if key == "umapper":
        return UMapper(chain_length, parallel)
    if key == "stacktorow":
        return StackToRowMapper(chain_length, parallel)

    return IdentityMapper()
