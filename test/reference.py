import sys, os, time, importlib, traceback, io, contextlib

from collections import namedtuple

from PIL import Image
import numpy as np
import random

from context import (
    REFERENCE_RANDOM_SEED,
    TEST_CONFIG_PATH,
    SAMPLE_CONFIG_PATH,
    TestConfigContext,
)

os.environ["RGBME_SUPPRESS_ADAPTER_LOAD_ERRORS"] = "true"

sys.path.append(os.path.abspath(os.path.join(__file__, "..", "..")))

import samples

sys.modules["samplebase"] = samples.samplebase

time.sleep = lambda _: 1 + 1

random.seed(REFERENCE_RANDOM_SEED)


class SampleExecutionHalted(Exception):
    pass


def halt_reference(*_args):
    raise SampleExecutionHalted


REFERENCE_SIZES = [(128, 32), (128, 64), (64, 32), (64, 64), (32, 32)]

Reference = namedtuple("Reference", ("file_name", "name", "frame", "halt_fn"))

_REFERENCES = [
    Reference("canvas-brightness", "CanvasBrightness", 256, halt_reference),
    Reference("graphics", "GraphicsTest", 140, halt_reference),
    Reference("grayscale-block", "GrayscaleBlock", 256, halt_reference),
    Reference("image-brightness", "ImageBrightness", 256, halt_reference),
    Reference("image-scroller", "ImageScroller", 50, halt_reference),
    Reference("pulsing-brightness", "GrayscaleBlock", 256, halt_reference),
    Reference("pulsing-colors", "PulsingColors", 256, halt_reference),
    Reference(
        "rotating-block-generator", "RotatingBlockGenerator", 256, halt_reference
    ),
    Reference("runtext", "RunText", 264, halt_reference),
    Reference("simple-square", "SimpleSquare", 256, halt_reference),
    Reference("singleton", "MultCanvas", 256, halt_reference),
    Reference("static", "Static", 256, halt_reference),
    # Not a class
    # Reference("image-draw", "ImageDraw", 256, halt_reference)
    # Needs an extra arg
    # Reference("image-viewer", "ImageViewer", 256, halt_reference)
]

REFERENCES = []

for reference in _REFERENCES:
    module = importlib.import_module(f"samples.{reference.file_name}")
    sample = getattr(module, reference.name)
    sample.name = reference.name
    sample.file_name = reference.file_name
    sample.frame = reference.frame
    sample.halt_fn = reference.halt_fn
    REFERENCES.append(sample)


def generate_reference(reference, refsize):
    run_sample(
        reference, refsize, screenshot_path=os.path.join(__file__, "..", "references")
    )


def generate_references(reference):
    for refsize in REFERENCE_SIZES:
        generate_reference(reference, refsize)


def run_sample(sample_class, size, screenshot_path=None):
    sys.argv = [
        f"{sample_class.file_name}.py",
        f"--led-cols={size[0]}",
        f"--led-rows={size[1]}",
    ]

    cwd = os.getcwd()
    os.chdir(os.path.abspath(os.path.join(__file__, "..", "..", "samples")))

    sample = sample_class()
    sample.usleep = lambda _: 1 + 1

    def mockedSetAttr(inst, name, value):
        if name == "matrix":
            inst.__dict__[name] = value

            inst.matrix.CreateFrameCanvas()
            adapter = inst.matrix.canvas.display_adapter
            adapter.halt_after = sample.frame
            adapter.halt_fn = sample.halt_fn
            adapter.width = inst.matrix.width
            adapter.height = inst.matrix.height
            adapter.options = inst.matrix.options
        else:
            super(inst.__class__, inst).__setattr__(name, value)

    sample_class.__setattr__ = mockedSetAttr

    try:
        sample.process()
    except SampleExecutionHalted:
        adapter = sample.matrix.canvas.display_adapter

        if screenshot_path:
            refdir = os.path.join(screenshot_path, sample_class.file_name)

            if not os.path.exists(refdir):
                os.mkdir(refdir)

            refpath = os.path.join(refdir, f"w{adapter.width}h{adapter.height}.png")
            adapter._dump_screenshot(refpath)

        return adapter._last_frame()
    except Exception:
        traceback.print_exc()
    finally:
        sample.matrix.canvas.display_adapter._reset()
        os.chdir(cwd)


def reference_to_nparray(sample, size):
    refpath = os.path.join(
        __file__, "..", "references", sample.file_name, f"w{size[0]}h{size[1]}.png"
    )
    refpath = os.path.abspath(refpath)

    if not os.path.exists(refpath):
        return None

    image = Image.open(refpath).convert("RGB")

    return np.array(image, dtype="uint8")


if __name__ == "__main__":
    with TestConfigContext(TEST_CONFIG_PATH, SAMPLE_CONFIG_PATH):
        for reference in REFERENCES:
            print(f"Generating references for {reference.file_name}...")
            # Suppress "Press CTRL-C to stop sample" messages
            with io.StringIO() as buf, contextlib.redirect_stdout(buf):
                generate_references(reference)
