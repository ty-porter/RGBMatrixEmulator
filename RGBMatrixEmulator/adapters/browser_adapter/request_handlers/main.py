from RGBMatrixEmulator.adapters.browser_adapter.request_handlers import NoCacheRequestHandler


class MainHandler(NoCacheRequestHandler):
    def get(self):
        self.render("./../static/index.html", adapter=MainHandler.adapter)

    def register_adapter(adapter):
        MainHandler.adapter = adapter
