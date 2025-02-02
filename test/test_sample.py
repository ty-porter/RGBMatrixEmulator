from unittest import TestCase

import io, contextlib, os

import numpy as np

from PIL import Image

from reference import REFERENCES, REFERENCE_SIZES, run_sample, reference_to_nparray

from parameterized import parameterized


class TestSampleRunMatchesReference(TestCase):

    TESTS = []

    for reference in REFERENCES:
        for refsize in REFERENCE_SIZES:
            TESTS.append(
                (f"{reference.name}-w{refsize[0]}h{refsize[1]}", reference, refsize)
            )

    @parameterized.expand(TESTS)
    def test_sample(self, name, sample, size):
        expected = reference_to_nparray(sample, size)

        if expected is None:
            return

        # Suppress "Press CTRL-C to stop sample" messages
        with io.StringIO() as buf, contextlib.redirect_stdout(buf):
            actual = run_sample(sample, size)

        if not np.array_equal(expected, actual):
            image = Image.fromarray(np.array(actual, dtype="uint8"), "RGB")
            image.save(
                os.path.join(
                    __file__,
                    "..",
                    "result",
                    f"{sample.file_name}-w{size[0]}h{size[1]}.png",
                )
            )

            self.assertTrue(
                False,
                f"Actual results do not match reference screenshot. See test/result/{sample.file_name}-w{size[0]}h{size[1]}.png to compare",
            )

        self.assertTrue(True)
