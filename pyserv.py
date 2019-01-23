from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from functools import partial
from SocketServer import ThreadingMixIn
from srvpages import pages
# import threading

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
                return
            elif self.path == '/getStatus':
                self._set_headers()
                return
            else:
                self.send_error(404)
                self.end_headers()
        except Exception as e:
            raise e

    def do_POST(self):
        try:
            if self.path == '/postStatus':
                self._set_headers()
                return
            if self.path == '/postHT':
                self._set_headers()
                return
            self.send_error(404)
            self.end_headers()
        except Exception as e:
            raise e


if __name__ == "__main__":
    server_address = (ADDR, PORT)
    p = pages()
    handler = partial(pyserv, p)
    httpd = ThreadedHTTPServer(server_address, handler)
    print 'Starting httpd...'
    print 'Starting server, use <Ctrl-C> to stop'
    httpd.serve_forever()
