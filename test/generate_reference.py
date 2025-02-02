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

def generate_reference(sample, frame, halt_fn):
    from samples.runtext import RunText

    os.chdir("samples")
    sys.argv = ['python runtext.py']
    rt = RunText()
    rt.usleep = lambda _: 1 + 1

    def mockedSetAttr(inst, name, value):
        if name == "matrix":
            inst.__dict__[name] = value

            inst.matrix.CreateFrameCanvas()
            inst.matrix.canvas.display_adapter.halt_after = frame
            inst.matrix.canvas.display_adapter.halt_fn = halt_fn
        else:
            super(inst.__class__, inst).__setattr__(name, value)

    RunText.__setattr__ = mockedSetAttr

    try:
        rt.process()
    except SampleExecutionHalted:
        refpath = os.path.join(__file__, "..", "reference", rt.__class__.__name__ + ".png")
        rt.matrix.canvas.display_adapter._dump_screenshot(refpath)

generate_reference(1, 264, simulateKeyboardInterrupt)