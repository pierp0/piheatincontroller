from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from functools import partial
from SocketServer import ThreadingMixIn
from srvpages import pages
import urlparse


ADDR = 'localhost'
PORT = 12345


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""


class pyserv(BaseHTTPRequestHandler):

    def __init__(self, pages, *args):
        self._pages = pages
        BaseHTTPRequestHandler.__init__(self, *args)

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_HEAD(self):
        self._set_headers()

    def do_GET(self):
        try:
            if self.path in ('/index.html', '/index.htm', '/index', '/', ''):
                self._set_headers()
                self.wfile.write(self._pages.showIndex())
                # self.wfile.write('hello world')
            elif self.path == '/getStatus':
                self._set_headers()
                self.wfile.write(self._pages.getStatus())
            if self.path.endswith(".css"):
                with open("./WWW/css/style.css") as f:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/css')
                    self.end_headers()
                    self.wfile.write(f.read())
        except IOError:
            self.send_error(404)
            self.end_headers()

    def do_POST(self):
        try:
            if self.path == '/postStatus':
                self._set_headers()
            elif self.path == '/postHT':
                data = dict(urlparse.parse_qs(self.rfile.read(int(self.headers['Content-Length'])))).items()
                self._pages.dump(data)
                self._set_headers()
        except IOError:
            self.send_error(404)
            self.end_headers()


if __name__ == "__main__":
    server_address = (ADDR, PORT)
    p = pages()
    handler = partial(pyserv, p)
    httpd = ThreadedHTTPServer(server_address, handler)
    print 'Starting httpd...'
    print 'Starting server, use <Ctrl-C> to stop'
    httpd.serve_forever()
