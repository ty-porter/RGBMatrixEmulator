import asyncio
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

        MainHandler.register_options(options, websocket.adapter)

        script_path  = path.dirname(path.realpath(__file__))
        asset_path   = path.normpath(script_path + '/static/assets/')

        self.app = tornado.web.Application([
            (r"/websocket", websocket),
            (r"/", MainHandler),
            (r"/assets/(.*)", tornado.web.StaticFileHandler, { 'path': asset_path, 'default_filename': 'client.js' })
        ])
        self.app.listen(8888)

    def run(self):
        print("Starting server: http://localhost:" + str(8888) + "/")
        
        thread = threading.Thread(target=tornado.ioloop.IOLoop.current().start)
        thread.start()

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('./static/index.html', adapter=MainHandler.adapter, options=MainHandler.options)

    def register_options(options, adapter):
        MainHandler.options = options
        MainHandler.adapter = adapter