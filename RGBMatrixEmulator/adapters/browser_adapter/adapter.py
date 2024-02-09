import io

import numpy as np

from PIL import Image, ImageDraw
from RGBMatrixEmulator.graphics import Color
from RGBMatrixEmulator.adapters.base import BaseAdapter
from RGBMatrixEmulator.adapters.browser_adapter.server import Server
from RGBMatrixEmulator.adapters.browser_adapter.web_socket import ImageWebSocket
from RGBMatrixEmulator.logger import Logger


class BrowserAdapter(BaseAdapter):

    SUPPORTS_ALTERNATE_PIXEL_STYLE = True

    def __init__(self, width, height, options):
        super().__init__(width, height, options)
        self.__server = None
        self.image = None

    def load_emulator_window(self):
        if self.loaded:
            return

        Logger.info(self.emulator_details_text())
        websocket = ImageWebSocket
        websocket.register_adapter(self)

        self.__server = Server(websocket, self.options)
        self.__server.run()

        self.loaded = True

    def draw_to_screen(self, pixels):
        image = self._get_masked_image(pixels)
        with io.BytesIO() as bytesIO:
            image.save(
                bytesIO, "JPEG", quality=self.options.browser.quality, optimize=True
            )
            self.image = bytesIO.getvalue()

