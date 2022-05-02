import asyncio
import signal
import sys
import threading
import tornado.web
import tornado.ioloop

from os import path
from tornado.platform.asyncio import AnyThreadEventLoopPolicy


asyncio.set_event_loop_policy(AnyThreadEventLoopPolicy())

class Server:
    def __init__(self, websocket, options):
        self.websocket = websocket
        self.options   = options
        self.__io_loop = None

        MainHandler.register_options(options, websocket.adapter)

        script_path  = path.dirname(path.realpath(__file__))
        asset_path   = path.normpath(script_path + '/static/assets/')

        self.app = tornado.web.Application([
            (r"/websocket", websocket),
            (r"/", MainHandler),
            (r"/assets/(.*)", tornado.web.StaticFileHandler, { 'path': asset_path, 'default_filename': 'client.js' })
        ])
        self.app.listen(self.options.browser.port)

    def run(self):
        print("Starting server...")
        
        self.__io_loop = tornado.ioloop.IOLoop.current()
        thread = threading.Thread(target=self.__io_loop.start)
        self.__initialize_interrupts()
        thread.start()

        print("Server started and ready to accept requests on http://localhost:" + str(self.options.browser.port) + "/")

    def __initialize_interrupts(self):
        '''
        Add custom signal handling to ensure webserver thread exits appropriately.

        Not thread-safe, signal handling must happen on the main thread.
        '''
        if threading.current_thread() is threading.main_thread():
            signal.signal(signal.SIGINT , self.__kill)
            signal.signal(signal.SIGTERM, self.__kill)

    def __kill(self, *_args):
        self.__io_loop.add_callback(self.__io_loop.stop)
        sys.exit()

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('./static/index.html', adapter=MainHandler.adapter, options=MainHandler.options)

    def register_options(options, adapter):
        MainHandler.options = options
        MainHandler.adapter = adapter
