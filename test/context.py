import os, shutil

from pathlib import Path

REFERENCE_RANDOM_SEED = 0xC0FFEE

TEST_CONFIG_PATH = Path(__file__).parent / "test_config.json"
SAMPLE_CONFIG_PATH = Path(__file__).parent.parent / "samples" / "emulator_config.json"


class TestConfigContext:
    def __init__(self, src, dst):
        self.src = Path(src)
        self.dst = Path(dst)
        self.backup_path = self.dst.with_suffix(self.dst.suffix + ".bak")
        self.backup = False

    def __enter__(self):
        if os.path.exists(self.dst):
            shutil.copy2(self.dst, self.backup_path)
            self.backup = True

        shutil.copy2(self.src, self.dst)

    def __exit__(self, exc_type, exc_value, traceback):
        if os.path.exists(self.dst):
            os.remove(self.dst)

        if self.backup:
            shutil.move(self.backup_path, self.dst)

        return False
