from unittest import TestCase

import io, contextlib, os, shutil, json, random

import numpy as np

from PIL import Image

from reference import REFERENCES, REFERENCE_SIZES, run_sample, reference_to_nparray

from parameterized import parameterized

from RGBMatrixEmulator.emulation.options import RGBMatrixEmulatorConfig
from test.context import (
    REFERENCE_RANDOM_SEED,
    TEST_CONFIG_PATH,
    SAMPLE_CONFIG_PATH,
    TestConfigContext,
)

random.seed(REFERENCE_RANDOM_SEED)


class TestSampleRunMatchesReference(TestCase):

    TESTS = []

    for reference in REFERENCES:
        for refsize in REFERENCE_SIZES:
            TESTS.append(
                (f"{reference.name}-w{refsize[0]}h{refsize[1]}", reference, refsize)
            )

    @classmethod
    def setUpClass(cls):
        cls.temp_context = TestConfigContext(TEST_CONFIG_PATH, SAMPLE_CONFIG_PATH)
        cls.temp_path = cls.temp_context.__enter__()

    @classmethod
    def tearDownClass(cls):
        cls.temp_context.__exit__(None, None, None)

    @parameterized.expand(TESTS)
    def test_sample(self, name, sample, size):
        expected = reference_to_nparray(sample, size)

        if expected is None:
            print(f"\n{sample.file_name} {size} has no reference image. Skipping...")
            return

        # Suppress "Press CTRL-C to stop sample" messages
        with io.StringIO() as buf, contextlib.redirect_stdout(buf):
            actual = run_sample(sample, size)

        if not np.array_equal(expected, actual):
            image = Image.fromarray(np.array(actual, dtype="uint8"), "RGB")
            image.save(
                os.path.abspath(
                    os.path.join(
                        __file__,
                        "..",
                        "result",
                        f"{sample.file_name}-w{size[0]}h{size[1]}.png",
                    )
                )
            )

            self.assertTrue(
                False,
                f"Actual results do not match reference screenshot. See test/result/{sample.file_name}-w{size[0]}h{size[1]}.png to compare",
            )

        self.assertTrue(True)
