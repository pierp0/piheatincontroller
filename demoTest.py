#!/usr/bin/env python

from functools import partial
from srvpages import pages
from random import randint
import requests
import thread
import time
import yaml
import pyserv


def runRelay(ip, port, status, sleep):
    s = status
    while True:
        time.sleep(sleep)
        requests.post("http://" + str(ip) + ":" +
                      str(port) + "/postStatus", data={"s": s})
        s = requests.get("http://" + str(ip) + ":" +
                         str(port) + "/getNextStatus").content
        if int(s == 'True'):
            print (str(time.strftime("\n%d/%m/%Y %H:%M:%S"))) + \
                " -- Status from relay : Active"
        else:
            print (str(time.strftime("\n%d/%m/%Y %H:%M:%S"))) + \
                " -- Status from relay : Unactive"


def runSensor(ip, port, mac, sleep):
    time.sleep(randint(1, 10))
    requests.post("http://" + str(ip) + ":" + str(port) +
                  "/postHello", data={"hello": mac})
    while True:
        time.sleep(sleep + randint(1, 10))
        t = randint(16, 30)
        h = randint(40, 60)
        requests.post("http://" + str(ip) + ":" + str(port) +
                      "/postHT", data={"r": mac, "t": t, "h": h})
        print (str(time.strftime("\n%d/%m/%Y %H:%M:%S"))) + \
            " -- MAC:" + str(mac) + " Temp: " + str(t) + " Hum: " + str(h)


if __name__ == "__main__":
    with open('./config.yml', 'r') as confFile:
        conf = yaml.load(confFile)
    ip = conf['server']['ip']
    port = int(conf['server']['port'])
    server_address = (ip, port)
    p = pages()
    handler = partial(pyserv.pyserv, p)
    httpd = pyserv.ThreadedHTTPServer(server_address, handler)
    print 'Starting httpd...'
    print 'Starting server, use <Ctrl-C> to stop'
    try:
        thread.start_new_thread(runRelay, (ip, port, False, 15))
        thread.start_new_thread(runSensor, (ip, port, "mac1", 10))
        thread.start_new_thread(runSensor, (ip, port, "mac2", 10))
        thread.start_new_thread(runSensor, (ip, port, "mac3", 10))
    except Exception as e:
        print "Error: unable to start thread"
    httpd.serve_forever()
