from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from functools import partial
from SocketServer import ThreadingMixIn
from srvpages import pages
import cgi
from urllib.parse import urlparse, parse_qs


ADDR = '127.0.0.1'
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
            else:
                self.send_error(404)
                self.end_headers()
        except IOError:
            self.send_error(500)
            self.end_headers()

    def do_POST(self):
        try:
            if self.path == '/postStatus':
                status = self.parsePost()
                print status
                self._set_headers()
            elif self.path == '/postHT':
                data = dict(urlparse.parse_qs(self.rfile.read(
                    int(self.headers['Content-Length'])))).items()
                print data
                self._pages.dump(data)
                self._set_headers()
            elif self.path == '/':
                status = self.parsePost()
                print status
                self._set_headers()
            else:
                self.send_error(404)
                self.end_headers()
        except IOError:
            self.send_error(500)
            self.end_headers()

    def parsePost(self):
        ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
        return cgi.parse_multipart(self.rfile, pdict)


if __name__ == "__main__":
    server_address = (ADDR, PORT)
    p = pages()
    handler = partial(pyserv, p)
    httpd = ThreadedHTTPServer(server_address, handler)
    print 'Starting httpd...'
    print 'Starting server, use <Ctrl-C> to stop'
    httpd.serve_forever()
