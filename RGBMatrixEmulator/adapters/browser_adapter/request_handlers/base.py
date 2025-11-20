import tornado.web


class NoCacheRequestHandler(tornado.web.RequestHandler):
    """Base handler that adds no-cache headers to all responses."""

    def set_default_headers(self):
        """Set headers to prevent browser caching."""
        self.set_header(
            "Cache-Control", "no-store, no-cache, must-revalidate, max-age=0"
        )
        self.set_header("Pragma", "no-cache")
        self.set_header("Expires", "0")


class NoCacheStaticFileHandler(tornado.web.StaticFileHandler):
    """Static file handler that adds no-cache headers to all responses."""

    def set_default_headers(self):
        """Set headers to prevent browser caching."""
        self.set_header(
            "Cache-Control", "no-store, no-cache, must-revalidate, max-age=0"
        )
        self.set_header("Pragma", "no-cache")
        self.set_header("Expires", "0")
