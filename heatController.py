from collections import deque
import os


class heatController():

    def __init__(self):
        self.avgT = 0
        self.avgH = 0
        self.rooms = {}
        self.relay = relay()
        self.roomsDown = 0

    def getT(self, room=0):
        return self.avgT

    def getH(self, room=0):
        return self.avgH

    def setDataFromSensor(self, data):
        print '\nprima di if'
        if data['room'] not in self.rooms:
            self.rooms[data['room']] = room(
                data['room'], data['temp'], data['humidity'])
        else:
            if self.rooms[data['room']].keepAlive < 1:
                self.roomsDown -= 1
            self.rooms[data['room']].updateRoom(data)
        self.updateRoomAlive(data['room'])
        self.updateTH()
        self.nextStatus()

    def updateRoomAlive(self, updatedroom):
        for room in self.rooms:
            if room != updatedroom:
                self.rooms[room].decreaseKA
                if self.rooms[room].keepAlive == 0:
                    self.roomsDown += 1

    def updateTH(self):
        t = 0
        h = 0
        print 'dentro updateTH'
        for room in self.rooms:
            t = t + float(self.rooms[room].getT())
            h = h + float(self.rooms[room].getH())
        print t
        print h
        self.avgT = int(float(t) / len(self.rooms) - self.roomsDown)
        self.avgH = int(float(h) / len(self.rooms) - self.roomsDown)

    def nextStatus(self):
        if self.nextStep() and self.arUatHome():
            self.relay.setNextStatus(True)

    def arUatHome(self):
        hosts = ['', '']
        if all(os.system("ping -c 1 " + host) for host in hosts):
            return False

    def nextStep(self):
        pass


class room():

    def __init__(self, r=0, t=0, h=0):
        self.r = r
        self.t = t
        self.h = h
        self.old = deque('', 5)
        self.keepAlive = 5

    def getT(self):
        if self.keepAlive > 0:
            return self.t
        else:
            return 0

    def getH(self):
        if self.keepAlive > 0:
            return self.h
        else:
            return 0

    def updateRoom(self, data):
        self.old.appendleft([self.t, self.h])
        self.t = data['temp']
        self.h = data['humidity']
        self.keepAlive = 5

    def decreaseKA(self):
        self.keepAlive -= 1


class relay():

    def __init__(self):
        # status : [True:UP, False:DOWN, None: not connected]
        self.status = None  # Not connected
        self.nextStatus = None
        self.keepAlive = 10

    def getStatus(self):
        return self.status

    def setStatus(self, status):
        self.status = status

    def setNextStatus(self, nstatus):
        self.nextStatus = nstatus
