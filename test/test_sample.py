from unittest import TestCase, mock
import sys, os
from RGBMatrixEmulator import RGBMatrixOptions

breakpoint()
from samples import samplebase

class TestSampleRunMatchesReference(TestCase):

    def setUp(self):
        os.chdir("samples")
        sys.argv = ['python runtext.py']
        sys.modules["samplebase"] = samplebase

        self.options = RGBMatrixOptions()
        self.options.display_adapter  = "raw"

    def tearDown(self):
        os.chdir("..")
        sys.path.pop()

    def test_sample(self):
        from samples.runtext import RunText

        def _halt():
            raise KeyboardInterrupt

        rt = RunText()
        rt.usleep = lambda _: 1 + 1

        def mockedSetAttr(inst, name, value):
            if name == "matrix":
                inst.__dict__[name] = value

                inst.matrix.CreateFrameCanvas()
                inst.matrix.canvas.display_adapter.halt_after = 5
                inst.matrix.canvas.display_adapter.halt_fn = _halt
            else:
                super(inst.__class__, inst).__setattr__(name, value)

        RunText.__setattr__ = mockedSetAttr

        rt.process()
