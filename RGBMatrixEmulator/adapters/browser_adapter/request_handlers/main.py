import tornado.web


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("./../static/index.html", adapter=MainHandler.adapter)

    def register_adapter(adapter):
        MainHandler.adapter = adapter
