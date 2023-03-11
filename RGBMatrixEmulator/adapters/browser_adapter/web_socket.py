import tornado.websocket

from RGBMatrixEmulator.logger import Logger


class ImageWebSocket(tornado.websocket.WebSocketHandler):
    clients = set()
    adapter = None

    def check_origin(self, _origin):
        # Allow access from every origin
        return True

    def open(self):
        ImageWebSocket.clients.add(self)
        Logger.info("WebSocket opened from: " + self.request.remote_ip)

    def on_message(self, _message):
        if not ImageWebSocket.adapter.image:
            Logger.warning("No image received from {}!".format(ImageWebSocket.adapter.__class__.__name__))
            return

        jpeg_bytes = ImageWebSocket.adapter.image
        self.write_message(jpeg_bytes, binary=True)

    def on_close(self):
        ImageWebSocket.clients.remove(self)

    def register_adapter(adapter):
        ImageWebSocket.adapter = adapter
