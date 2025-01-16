import io

from RGBMatrixEmulator.adapters.base import BaseAdapter
from RGBMatrixEmulator.adapters.browser_adapter.server import Server
from RGBMatrixEmulator.logger import Logger


class BrowserAdapter(BaseAdapter):
    SUPPORTS_ALTERNATE_PIXEL_STYLE = True
    IMAGE_FORMATS = {"bmp": "BMP", "jpeg": "JPEG", "png": "PNG", "webp": "WebP"}

    def __init__(self, width, height, options):
        super().__init__(width, height, options)
        self.__server = None
        self.image = None
        self.default_image_format = "JPEG"

        image_format = options.browser.image_format
        if image_format.lower() in self.IMAGE_FORMATS:
            self.image_format = self.IMAGE_FORMATS[image_format.lower()]
        else:
            Logger.warning(
                "Invalid browser image format '{}', falling back to '{}'".format(
                    image_format, self.default_image_format
                )
            )
            self.image_format = self.IMAGE_FORMATS.get(
                self.default_image_format.lower()
            )

    def load_emulator_window(self):
        if self.loaded:
            return

        Logger.info(self.emulator_details_text())

        self.__server = Server(self)
        self.__server.run()

        self.loaded = True

    def draw_to_screen(self, pixels):
        image = self._get_masked_image(pixels)
        with io.BytesIO() as bytesIO:
            image.save(
                bytesIO,
                self.image_format,
                quality=self.options.browser.quality,
                optimize=True,
            )
            self.image = bytesIO.getvalue()
