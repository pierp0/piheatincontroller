import datetime
import urlparse
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer


class pyserv(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self._avgtemp = 0.00
        self._avghumidity = 0.00

    def do_GET(self):
        self._set_headers()
        f = open("index.html", "r")
        self.wfile.write(f.read())

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        self._set_headers()
        self.send_response(200)
        self.end_headers()
        dump(self)
        return


def run(server_class=HTTPServer, handler_class=pyserv, port=12345):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print 'Starting httpd...'
    httpd.serve_forever()


def dump(self):
    data = {'room': '', 'time': '', 'temp': '', 'humidity': ''}
    for key, value in dict(urlparse.parse_qs(self.rfile.read(int(self.headers['Content-Length'])))).items():
        if key == 't':
            data['temp'] = value[0]
            print value[0]
        elif key == 'h':
            data['humidity'] = value[0]
        elif key == 'r':
            data['room'] = value[0]
        else:
            print value[0]
    data['time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("temperature.txt", "a+") as outfile:
        outfile.write(str(data) + '\n')


if __name__ == "__main__":
    from sys import argv

if len(argv) == 2:
    run(port=int(argv[1]))
else:
    run()
