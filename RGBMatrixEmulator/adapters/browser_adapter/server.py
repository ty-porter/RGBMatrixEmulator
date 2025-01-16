import asyncio
import signal
import sys
import threading
import tornado.web
import tornado.ioloop

from os import path
from tornado.platform.asyncio import AnyThreadEventLoopPolicy

from RGBMatrixEmulator.adapters.browser_adapter.request_handlers import *
from RGBMatrixEmulator.logger import Logger


asyncio.set_event_loop_policy(AnyThreadEventLoopPolicy())


class Server:
    instance = None

    # Singleton class for the server.
    # No more than one webserver can be running at a given time.
    class __Singleton:
        def __init__(self, adapter):
            self.adapter = adapter
            self.io_loop = None
            self.listening = False

            MainHandler.register_adapter(self.adapter)
            ImageWebSocketHandler.register_adapter(self.adapter)
            ImageHandler.register_adapter(self.adapter)

            script_path = path.dirname(path.realpath(__file__))
            asset_path = path.normpath(script_path + "/static/assets/")

            self.app = tornado.web.Application(
                [
                    (r"/websocket", ImageWebSocketHandler),
                    (r"/image", ImageHandler),
                    (r"/", MainHandler),
                    (
                        r"/assets/(.*)",
                        tornado.web.StaticFileHandler,
                        {"path": asset_path, "default_filename": "client.js"},
                    ),
                ]
            )

    def __init__(self, adapter):
        if not Server.instance:
            Server.instance = Server.__Singleton(adapter)

    def run(self):
        if not self.instance.listening:
            Logger.info("Starting server...")

            self.instance.listening = True
            self.instance.app.listen(self.instance.adapter.options.browser.port)
            self.instance.io_loop = tornado.ioloop.IOLoop.current()
            thread = threading.Thread(
                target=self.instance.io_loop.start,
                name="RGBMEServerThread",
                daemon=True,
            )
            self.__initialize_interrupts()
            thread.start()

            Logger.info(
                "Server started and ready to accept requests on http://localhost:"
                + str(self.instance.adapter.options.browser.port)
                + "/"
            )

    def __initialize_interrupts(self):
        """
        Add custom signal handling to ensure webserver thread exits appropriately.

        Not thread-safe, signal handling must happen on the main thread.
        """
        if threading.current_thread() is threading.main_thread():
            signal.signal(signal.SIGINT, self.__kill)
            signal.signal(signal.SIGTERM, self.__kill)

    def __kill(self, *_args):
        self.instance.io_loop.add_callback(self.instance.io_loop.stop)
        sys.exit()
