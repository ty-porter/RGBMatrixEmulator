import os
from RGBMatrixEmulator.adapters.browser_adapter.request_handlers import (
    NoCacheRequestHandler,
)


class SingleFileHandler(NoCacheRequestHandler):
    def initialize(self, file_path):
        self.file_path = file_path

    async def get(self):
        if not os.path.exists(self.file_path):
            self.set_status(404)
            return

        self.set_header("Content-Type", "image/x-icon")

        with open(self.file_path, "rb") as f:
            self.write(f.read())
