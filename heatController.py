from collections import deque


class heatController():

    def __init__(self):
        self.avgT = 0
        self.avgH = 0
        self.rooms = {}
        self.relay = relay()

    def getT(self, room=0):
        return self.avgT

    def getH(self, room=0):
        return self.avgH

    def setDataFromSensor(self, data):
        print '\nprima di if'
        if data['room'] not in self.rooms:
            print '\ndentro if'
            self.rooms[data['room']] = room(data['room'], data['temp'], data['humidity'])
        else:
            print '\ndentro else'
            self.rooms[data['room']].rUpdate(data)
        print 'prima di updateTH'
        self.updateTH()

    def updateTH(self):
        t = 0
        h = 0
        print 'dentro updateTH'
        for key in self.rooms:
            t = t + float(self.rooms[key].getT())
            h = h + float(self.rooms[key].getH())
        print t
        print h
        self.avgT = int(float(t) / len(self.rooms))
        self.avgH = int(float(h) / len(self.rooms))

    def updateH():
        pass

    def nextStatus(self):
        pass

    def actualStatusRelay(self):
        pass


class room():

    def __init__(self, rnum=0, t=0, h=0):
        print 'dentro room'
        self.rnum = rnum
        self.t = t
        self.h = h
        self.old = deque('', 5)
        self.keepAlive = 5

    def getT(self):
        return self.t

    def getH(self):
        return self.h

    def rUpdate(self, data):
        self.old.appendleft([self.t, self.h])
        self.t = data['temp']
        self.h = data['humidity']
        self.keepAlive = 5


class relay():

    def __init__(self):
        # status : [True:UP, False:DOWN, None: not connected]
        self.status = None  # Not connected
        self.nextStatus = None
