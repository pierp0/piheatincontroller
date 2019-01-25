from collections import deque


class heatController():
    def __init__(self):
        self.avg_temp = 0
        self.rooms = {}

    def getT(self):
        return 20

    def getH(self, room=0):
        pass

    def setDataFromSensor(self, data):
        if data['room'] not in self.rooms:
            self.rooms[data['room']] = room(data['room'], data['temp'], data['humidity'])

    def nextStatus(self):
        pass

    def actualStatusRelay(self):
        pass


class room():

    def __init__(self, rnum=0, t=0, h=0):
        self.rnum = rnum
        self.t = t
        self.h = h


class relay():

    def __init__(self):
        # status : [True:UP, False:DOWN, None: not connected]
        self.status = None  # Not connected
        self.nextStatus = None
