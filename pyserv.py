from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from functools import partial
from SocketServer import ThreadingMixIn
from srvpages import pages
import urlparse
import yaml


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
        getPagesMap = {'/index.html': self._pages.showIndex,
                       '/index.htm': self._pages.showIndex,
                       '/index': self._pages.showIndex,
                       '/': self._pages.showIndex,
                       '': self._pages.showIndex,
                       '/getStatus': self._pages.getStatus,
                       '/getNextStatus': self._pages.getNextStatus,
                       '/getTemp': self._pages.getTemp,
                       '/getHum': self._pages.getHum,
                       '/roomsDatails': self._pages.getRommsPage,
                       '/updateConsumption': self._pages.getConsumption,
                       '/updateForecast': self._pages.getForecast,
                       '/getOperationMode': self._pages.getOperationMode
                       }
        try:
            if self.path in getPagesMap:
                self._set_headers()
                self.wfile.write(getPagesMap[self.path]())
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
        postPagesMap = {'/postStatus': self._pages.setRelayStatus,
                        '/postHT': self._pages.setHT,
                        '/auto': self._pages.setAuto,
                        '/alwayson': self._pages.setAlwaysOn,
                        '/alwaysoff': self._pages.setAlwaysOff,
                        '/keepTemperature': self._pages.setKT,
                        '/': self._pages.setError
                        }
        try:
            if self.path in postPagesMap:
                postPagesMap[self.path](self.parsePost())
                self._set_headers()
            else:
                self.send_error(404)
                self.end_headers()
        except IOError:
            self.send_error(500)
            self.end_headers()

    def parsePost(self):
        return urlparse.parse_qs(self.rfile.read(int(self.headers['Content-Length']))).items()


if __name__ == "__main__":
    with open('./config.yml', 'r') as confFile:
        conf = yaml.load(confFile)
    server_address = (conf['server']['ip'], int(conf['server']['port']))
    p = pages()
    handler = partial(pyserv, p)
    httpd = ThreadedHTTPServer(server_address, handler)
    print 'Starting httpd...'
    print 'Starting server, use <Ctrl-C> to stop'
    httpd.serve_forever()


'''
            if self.path == '/postStatus':
                self._pages.setRelayStatus(self.parsePost())
                self._set_headers()

            elif self.path == '/postHT':
                self._pages.setHT(self.parsePost())
                self._set_headers()

            elif self.path == '/auto':
                self._pages.setAuto()
                self._set_headers()

            elif self.path == '/alwayson':
                self._pages.setAlwayson()
                self._set_headers()

            elif self.path == '/alwaysoff':
                self._pages.setAlwaysoff()
                self._set_headers()

            elif self.path == '/keepTemperature':
                self._pages.setKT()
                self._set_headers()
            elif self.path == '/':
                self._pages.setError(self.parsePost())
                self._set_headers()
'''