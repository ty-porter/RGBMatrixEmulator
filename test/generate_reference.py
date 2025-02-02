import sys, os, time, importlib, traceback

sys.path.append(os.path.join(__file__, "..", ".."))

import samples
sys.modules["samplebase"] = samples.samplebase

_sysexit = sys.exit
time.sleep = lambda _: 1 + 1

class SampleExecutionHalted(Exception):
    pass

def simulateKeyboardInterrupt():
    raise KeyboardInterrupt

def mockedExit(code):
    if code != 0:
        return _sysexit(code)

    raise SampleExecutionHalted

sys.exit = mockedExit

def generate_reference(file_name, sample_name, frame, halt_fn):
    module = importlib.import_module(f"samples.{file_name}")
    Sample = getattr(module, sample_name)

    os.chdir("samples")

    sample = Sample()
    sample.usleep = lambda _: 1 + 1

    def mockedSetAttr(inst, name, value):
        if name == "matrix":
            inst.__dict__[name] = value

            inst.matrix.CreateFrameCanvas()
            adapter = inst.matrix.canvas.display_adapter
            adapter.halt_after = frame
            adapter.halt_fn = halt_fn
            adapter.width = inst.matrix.width
            adapter.height = inst.matrix.height
            adapter.options = inst.matrix.options
        else:
            super(inst.__class__, inst).__setattr__(name, value)

    Sample.__setattr__ = mockedSetAttr

    try:
        sample.process()
    except SampleExecutionHalted:
        adapter = sample.matrix.canvas.display_adapter
        refdir = os.path.join(__file__, "..", "reference", sample_name)

        if not os.path.exists(refdir):
            os.mkdir(refdir)

        refpath = os.path.join(refdir, f"w{adapter.width}h{adapter.height}.png")
        adapter._dump_screenshot(refpath)
    except Exception:
        print(f"An error occurred generating a reference for {sample_name} ({file_name}, {sys.argv})")
        traceback.print_exc()
    finally:
        sample.matrix.canvas.display_adapter._reset()
        os.chdir("..")

REFERENCE_SIZES = [
    (128, 32),
    (128, 64),
    (64, 32),
    (64, 64),
    (32, 32)
]

def generate_references(file_name, sample_name, frame, halt_fn):
    for refsize in REFERENCE_SIZES:
        sys.argv = [f'{file_name}.py', f"--led-cols={refsize[0]}", f'--led-rows={refsize[1]}']
        print(f"generating a reference for {sample_name} ({file_name}, {sys.argv})")

        generate_reference(file_name, sample_name, frame, halt_fn)

generate_references("canvas-brightness", "CanvasBrightness", 256, simulateKeyboardInterrupt)
generate_references("graphics", "GraphicsTest", 140, simulateKeyboardInterrupt)
generate_references("grayscale-block", "GrayscaleBlock", 256, simulateKeyboardInterrupt)
generate_references("image-brightness", "ImageBrightness", 256, simulateKeyboardInterrupt)
generate_references("image-scroller", "ImageScroller", 50, simulateKeyboardInterrupt)
generate_references("pulsing-brightness", "GrayscaleBlock", 256, simulateKeyboardInterrupt)
generate_references("pulsing-colors", "PulsingColors", 256, simulateKeyboardInterrupt)
generate_references("rotating-block-generator", "RotatingBlockGenerator", 256, simulateKeyboardInterrupt)
generate_references("runtext", "RunText", 264, simulateKeyboardInterrupt)
generate_references("simple-square", "SimpleSquare", 256, simulateKeyboardInterrupt)
generate_references("singleton", "MultCanvas", 256, simulateKeyboardInterrupt)

# Not a class
# generate_reference("image-draw", "ImageDraw", 264, simulateKeyboardInterrupt)

# Needs an extra arg
# generate_reference("image-viewer", "ImageViewer", 264, simulateKeyboardInterrupt)
