import io

from PIL import Image

from RGBMatrixEmulator.adapters.base import BaseAdapter
from RGBMatrixEmulator.adapters.browser_adapter.server import Server
from RGBMatrixEmulator.adapters.browser_adapter.web_socket import ImageWebSocket


class BrowserAdapter(BaseAdapter):

    def __init__(self, width, height, options):
        super().__init__(width, height, options)
        self.__server = None
        self.image    = None

    def load_emulator_window(self):
        print(self.emulator_details_text())
        websocket = ImageWebSocket
        websocket.register_adapter(self)

        self.__server = Server(websocket, self.options)
        self.__server.run()

    def draw_to_screen(self, pixels):
        image = Image.new("RGB", (self.width, self.height))

        for row, pixel_row in enumerate(pixels):
            for col, pixel in enumerate(pixel_row):
                image.putpixel((col, row), pixel.to_tuple())

        image = image.resize(self.options.window_size(), resample=False)

        with io.BytesIO() as bytesIO:
            image.save(bytesIO, "JPEG", quality=70, optimize=True)
            self.image = bytesIO.getvalue()
