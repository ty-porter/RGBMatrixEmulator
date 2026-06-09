import sys, os, traceback, io, contextlib

from collections import namedtuple

from PIL import Image
import numpy as np

# Make the sibling test modules and the project root importable, whether this
# file is imported by the test runner (as pixel_mapper.mapper_reference) or
# executed directly to regenerate references.
SPECS_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_DIR = os.path.abspath(os.path.join(SPECS_DIR, ".."))
ROOT_DIR = os.path.abspath(os.path.join(TEST_DIR, ".."))
for path in (ROOT_DIR, TEST_DIR, SPECS_DIR):
    if path not in sys.path:
        sys.path.append(path)

from context import TEST_CONFIG_PATH, SAMPLE_CONFIG_PATH, TestConfigContext
from labeled_panels import LabeledPanels

from RGBMatrixEmulator.adapters.raw_adapter import RawAdapter

REFERENCE_DIR = os.path.join(TEST_DIR, "references", "pixel-mapper")
SAMPLES_DIR = os.path.join(ROOT_DIR, "samples")


class SampleExecutionHalted(Exception):
    pass


def halt_reference(*_args):
    raise SampleExecutionHalted


MapperSpec = namedtuple(
    "MapperSpec", ("name", "cols", "rows", "chain", "parallel", "mapper")
)

"""
Geometries follow the canonical examples in rpi-rgb-led-matrix's lib/README.md
(https://github.com/hzeller/rpi-rgb-led-matrix/blob/master/lib/README.md).

  identity      32x32, chain 4 x parallel 1 -> 128x32
  U-mapper      32x32, chain 4 x parallel 1 ->  64x64
  V-mapper      64x32, chain 2 x parallel 1 ->  64x64
  StackToRow    64x32, chain 1 x parallel 2 -> 128x32
  Rotate/Mirror 32x32, chain 2 x parallel 2 ->  64x64

Note: Some mappers cause panel layouts to behave differently than rpi-rgb-led-matrix

For instance:
V-mapper:Z is identical to V-mapper -- the Z (zigzag) flag only flips alternate
physical panels for cabling, which the emulator does not model.
"""
MAPPER_SPECS = [
    MapperSpec("identity", 32, 32, 4, 1, ""),
    MapperSpec("vmapper", 64, 32, 2, 1, "V-mapper"),
    MapperSpec("vmapper-z", 64, 32, 2, 1, "V-mapper:Z"),
    MapperSpec("umapper", 32, 32, 4, 1, "U-mapper"),
    MapperSpec("stacktorow", 64, 32, 1, 2, "StackToRow"),
    MapperSpec("rotate-90", 32, 32, 2, 2, "Rotate:90"),
    MapperSpec("rotate-180", 32, 32, 2, 2, "Rotate:180"),
    MapperSpec("rotate-270", 32, 32, 2, 2, "Rotate:270"),
    MapperSpec("mirror-h", 32, 32, 2, 2, "Mirror:H"),
    MapperSpec("mirror-v", 32, 32, 2, 2, "Mirror:V"),
]


def run_mapper_spec(spec, screenshot_path=None):
    """
    Render the LabeledPanels fixture once under the spec's mapper config through
    the raw adapter. Returns the screen pixel array (also dumps a PNG into
    screenshot_path when provided).
    """
    # Reset the adapter to force a correctly sized adapter (and mask) for this spec.
    RawAdapter.INSTANCE = None

    sys.argv = [
        "labeled_panels.py",
        f"--led-cols={spec.cols}",
        f"--led-rows={spec.rows}",
        f"--led-chain={spec.chain}",
        f"--led-parallel={spec.parallel}",
        f"--led-pixel-mapper={spec.mapper}",
    ]

    cwd = os.getcwd()
    # RGBMatrixEmulatorConfig.CONFIG_PATH is resolved relative to the cwd; the
    # raw-adapter test config is staged in samples/ by TestConfigContext.
    os.chdir(SAMPLES_DIR)

    sample = LabeledPanels()

    def mockedSetAttr(inst, name, value):
        if name == "matrix":
            inst.__dict__[name] = value

            inst.matrix.CreateFrameCanvas()
            adapter = inst.matrix.canvas.display_adapter
            adapter.halt_after = 1
            adapter.halt_fn = halt_reference
        else:
            super(inst.__class__, inst).__setattr__(name, value)

    LabeledPanels.__setattr__ = mockedSetAttr

    try:
        sample.process()
    except SampleExecutionHalted:
        adapter = sample.matrix.canvas.display_adapter

        if screenshot_path:
            if not os.path.exists(screenshot_path):
                os.makedirs(screenshot_path)

            adapter._dump_screenshot(os.path.join(screenshot_path, f"{spec.name}.png"))

        return adapter._last_frame()
    except Exception:
        traceback.print_exc()
    finally:
        adapter = sample.matrix.canvas.display_adapter
        type(adapter).INSTANCE = None
        LabeledPanels.__setattr__ = object.__setattr__
        os.chdir(cwd)


def reference_to_nparray(spec):
    refpath = os.path.join(REFERENCE_DIR, f"{spec.name}.png")

    if not os.path.exists(refpath):
        return None

    image = Image.open(refpath).convert("RGB")

    return np.array(image, dtype="uint8")


if __name__ == "__main__":
    with TestConfigContext(TEST_CONFIG_PATH, SAMPLE_CONFIG_PATH):
        for spec in MAPPER_SPECS:
            print(f"Generating reference for {spec.name}...")
            # Suppress "Press CTRL-C to stop sample" messages
            with io.StringIO() as buf, contextlib.redirect_stdout(buf):
                run_mapper_spec(spec, screenshot_path=REFERENCE_DIR)
