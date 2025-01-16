import tornado.websocket

from RGBMatrixEmulator.logger import Logger


class ImageWebSocketHandler(tornado.websocket.WebSocketHandler):
    clients = set()
    adapter = None

    def check_origin(self, _origin):
        # Allow access from every origin
        return True

    def open(self):
        ImageWebSocketHandler.clients.add(self)
        Logger.info("WebSocket opened from: " + self.request.remote_ip)

    def on_message(self, _message):
        if not ImageWebSocketHandler.adapter.image:
            Logger.warning(
                "No image received from {}!".format(
                    ImageWebSocketHandler.adapter.__class__.__name__
                )
            )
            return

        image_bytes = ImageWebSocketHandler.adapter.image
        self.write_message(image_bytes, binary=True)

    def on_close(self):
        ImageWebSocketHandler.clients.remove(self)

    def register_adapter(adapter):
        ImageWebSocketHandler.adapter = adapter
