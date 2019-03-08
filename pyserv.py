#!/usr/bin/env python

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from functools import partial
from SocketServer import ThreadingMixIn
from srvpages import pages
import urlparse
import yaml

DEBUG = False


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
                       '/getNextStatus': self._pages.getNextStep,
                       '/getTemp': self._pages.getTemp,
                       '/getHum': self._pages.getHum,
                       '/roomsDatails': self._pages.getRommsPage,
                       '/updateConsumption': self._pages.getConsumption,
                       '/updateForecast': self._pages.getForecast,
                       '/getOperationMode': self._pages.getOperationMode
                       }
        try:
            if(DEBUG):
                print self.path
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
                        '/mode': self._pages.setMode,
                        '/postHello': self._pages.postHello,
                        '/': self._pages.setError
                        }
        try:
            if(DEBUG):
                print self.path
            if self.path in postPagesMap:
                self._set_headers()
                self.wfile.write(postPagesMap[self.path](self.parsePost()))
            else:
                self.send_error(404)
                self.end_headers()
        except IOError:
            self.send_error(500)
            self.end_headers()

    def parsePost(self):
        return urlparse.parse_qs(self.rfile.read(int(self.headers['Content-Length']))).items()

# Add configuration mode... load sensors one by one and record macaddress


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
