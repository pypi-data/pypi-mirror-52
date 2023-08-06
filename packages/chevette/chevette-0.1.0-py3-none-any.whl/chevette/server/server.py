import os
from http.server import HTTPServer, SimpleHTTPRequestHandler


class ChevetteRequestHandler(SimpleHTTPRequestHandler):

    def do_GET(self):

        if not os.path.exists(self.path):
            self.path = '404.html'

        SimpleHTTPRequestHandler.do_GET(self)


class ChevetteServer(HTTPServer):

    def __init__(self, config, address, port):
        self.config = config
        HTTPServer.__init__(
            self,
            (address, port),
            ChevetteRequestHandler
        )
