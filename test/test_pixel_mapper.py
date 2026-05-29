from unittest import TestCase

import io, contextlib, os

import numpy as np

from PIL import Image

from specs.mapper_reference import MAPPER_SPECS, run_mapper_spec, reference_to_nparray

from parameterized import parameterized

from test.context import (
    TEST_CONFIG_PATH,
    SAMPLE_CONFIG_PATH,
    TestConfigContext,
)


class TestPixelMapperMatchesReference(TestCase):

    TESTS = [(spec.name, spec) for spec in MAPPER_SPECS]

    @classmethod
    def setUpClass(cls):
        cls.temp_context = TestConfigContext(TEST_CONFIG_PATH, SAMPLE_CONFIG_PATH)
        cls.temp_context.__enter__()

    @classmethod
    def tearDownClass(cls):
        cls.temp_context.__exit__(None, None, None)

    @parameterized.expand(TESTS)
    def test_pixel_mapper(self, name, spec):
        expected = reference_to_nparray(spec)

        if expected is None:
            print(f"\n{spec.name} has no reference image. Skipping...")
            return

        # Suppress "Press CTRL-C to stop sample" messages
        with io.StringIO() as buf, contextlib.redirect_stdout(buf):
            actual = run_mapper_spec(spec)

        if not np.array_equal(expected, actual):
            image = Image.fromarray(np.array(actual, dtype="uint8"), "RGB")
            image.save(
                os.path.abspath(
                    os.path.join(__file__, "..", "result", f"{spec.name}.png")
                )
            )

            self.assertTrue(
                False,
                f"Actual results do not match reference screenshot. See test/result/{spec.name}.png to compare",
            )

        self.assertTrue(True)
