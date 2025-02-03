from unittest import TestCase

import io, contextlib, os, shutil, json

import numpy as np

from PIL import Image

from reference import REFERENCES, REFERENCE_SIZES, run_sample, reference_to_nparray

from parameterized import parameterized

from RGBMatrixEmulator.emulation.options import RGBMatrixEmulatorConfig

# Tests will be run from the samples directory
CONFIG_PATH = os.path.join("samples", RGBMatrixEmulatorConfig.CONFIG_PATH)
BACKUP_PATH = CONFIG_PATH + ".bak"


class TestSampleRunMatchesReference(TestCase):

    TESTS = []

    for reference in REFERENCES:
        for refsize in REFERENCE_SIZES:
            TESTS.append(
                (f"{reference.name}-w{refsize[0]}h{refsize[1]}", reference, refsize)
            )

    def setUp(self):
        self.emulator_config = RGBMatrixEmulatorConfig.DEFAULT_CONFIG | {
            "suppress_adapter_load_errors": True,
            "display_adapter": "raw",
        }

        if os.path.exists(CONFIG_PATH):
            shutil.move(CONFIG_PATH, BACKUP_PATH)

        with open(CONFIG_PATH, "w") as f:
            json.dump(self.emulator_config, f, indent=4)

    def tearDown(self):
        if os.path.exists(CONFIG_PATH):
            os.remove(CONFIG_PATH)

        if os.path.exists(BACKUP_PATH):
            shutil.move(BACKUP_PATH, CONFIG_PATH)

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
