import tornado.web


class ImageHandler(tornado.web.RequestHandler):
    def get(self):
        self.set_header(
            "Content-type", "image/{}".format(self.adapter.image_format.lower())
        )
        self.write(self.adapter.image)

    def register_adapter(adapter):
        ImageHandler.adapter = adapter
