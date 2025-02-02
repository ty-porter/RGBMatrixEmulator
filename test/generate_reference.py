import sys, os, time, importlib

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
    sys.argv = [f'python {file_name}.py']
    sample = Sample()
    sample.usleep = lambda _: 1 + 1

    def mockedSetAttr(inst, name, value):
        if name == "matrix":
            inst.__dict__[name] = value

            inst.matrix.CreateFrameCanvas()
            inst.matrix.canvas.display_adapter.halt_after = frame
            inst.matrix.canvas.display_adapter.halt_fn = halt_fn
        else:
            super(inst.__class__, inst).__setattr__(name, value)

    Sample.__setattr__ = mockedSetAttr

    try:
        sample.process()
    except SampleExecutionHalted:
        refpath = os.path.join(__file__, "..", "reference", f"{sample_name}.png")
        sample.matrix.canvas.display_adapter._dump_screenshot(refpath)
    finally:
        sample.matrix.canvas.display_adapter._reset()
        os.chdir("..")

generate_reference("canvas-brightness", "CanvasBrightness", 256, simulateKeyboardInterrupt)
generate_reference("graphics", "GraphicsTest", 140, simulateKeyboardInterrupt)
generate_reference("grayscale-block", "GrayscaleBlock", 256, simulateKeyboardInterrupt)
generate_reference("image-brightness", "ImageBrightness", 256, simulateKeyboardInterrupt)
generate_reference("image-scroller", "ImageScroller", 50, simulateKeyboardInterrupt)
generate_reference("pulsing-brightness", "GrayscaleBlock", 256, simulateKeyboardInterrupt)
generate_reference("pulsing-colors", "PulsingColors", 256, simulateKeyboardInterrupt)
generate_reference("rotating-block-generator", "RotatingBlockGenerator", 256, simulateKeyboardInterrupt)
generate_reference("runtext", "RunText", 264, simulateKeyboardInterrupt)
generate_reference("simple-square", "SimpleSquare", 256, simulateKeyboardInterrupt)
generate_reference("singleton", "MultCanvas", 256, simulateKeyboardInterrupt)

# Not a class
# generate_reference("image-draw", "ImageDraw", 264, simulateKeyboardInterrupt)

# Needs an extra arg
# generate_reference("image-viewer", "ImageViewer", 264, simulateKeyboardInterrupt)
