from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from functools import partial
from SocketServer import ThreadingMixIn
from srvpages import pages
import urlparse


ADDR = '192.168.1.100'
PORT = 12345


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""


class pyserv(BaseHTTPRequestHandler):

    def __init__(self, pages, *args):
        self._pages = pages
        BaseHTTPRequestHandler.__init__(self, *args)

    def _set_headers(self, ct='text/html'):
        self.send_response(200)
        self.send_header('Content-type', ct)
        self.end_headers()

    def do_HEAD(self):
        self._set_headers()

    def do_GET(self):
        getPagesMap = {'/index.html': self._pages.showIndex(),
                       '/index.htm': self._pages.showIndex(),
                       '/index': self._pages.showIndex(),
                       '/': self._pages.showIndex(),
                       '': self._pages.showIndex(),
                       '/getStatus': self._pages.getStatus(),
                       '/getTemp': self._pages.getTemp(),
                       '/getHum': self._pages.getHum(),
                       }
        try:
            if self.path in getPagesMap:
                self._set_headers()
                self.wfile.write(getPagesMap[self.path])
            elif self.path.endswith('.css'):
                self._set_headers('text/css')
                self.wfile.write(self._pages.getCss())
        except IOError:
            self.send_error(404)
            self.end_headers()
        #else:
        #    print 'Error, request not parsed :\n' + str(self.path)

    def do_POST(self):
        try:
            print self.path
            print 'qui'
            if self.path == '/postStatus':
                #da finire
                self._set_headers()
            elif self.path == '/':
                print 'hhhhhhhhhh'
                print self.path
                print self.headers
                print self.headers['Content-Type']
                print self.rfile
                self._set_headers()
            elif self.path == '/postHT':
                data = dict(urlparse.parse_qs(self.rfile.read(
                    int(self.headers['Content-Length'])))).items()
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
