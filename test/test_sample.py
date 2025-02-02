from unittest import TestCase

import io, contextlib

from reference import REFERENCES, REFERENCE_SIZES, run_sample, reference_to_nparray

from parameterized import parameterized

class TestSampleRunMatchesReference(TestCase):

    TESTS = []

    for reference in REFERENCES:
        for refsize in REFERENCE_SIZES:
            TESTS.append((reference, refsize))

    @parameterized.expand(TESTS)
    def test_sample(self, sample, size):
        expected = reference_to_nparray(sample, size)

        if expected is None:
            return

        # Suppress "Press CTRL-C to stop sample" messages
        with io.StringIO() as buf, contextlib.redirect_stdout(buf):
            actual = run_sample(sample, size)

        if (expected != actual).all():

            self.assertTrue(
                False,
                f"Actual results do not match reference screenshot. See test/result/{sample.file_name}/w{sample.width}h{sample.height}.png to compare"
            )

        self.assertTrue(True)