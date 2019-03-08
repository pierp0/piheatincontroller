from collections import deque
import datetime


class heatController():

    def __init__(self, roomslist, ktmode, automode):
        self.avgT, self.avgH = (0.00, 0.00)
        self.rooms = {}
        for r in roomslist:
            self.rooms[r] = room(roomslist[r], 3 * len(roomslist))
        self.relay = relay()
        self.kttemperature = ktmode['temperature']
        self.kttollerance = ktmode['tollerance']
        self.automode = automode
        # 0 = alwaysOff 1 = alwaysOn, 2 = auto, 3 = keepTemp
        self.operationmode = 0
        self.relayNextStep = False

    def addSensor(self, mac):
        if not self.rooms[mac].isActive():
            self.rooms[mac].setActive(True)

    def setDataFromSensor(self, data):
        self.rooms[data['room']].updateRoom(data)
        self.decreaseRoomAlive(data['room'])
        self.updateTH()
        self.updateStatus()

    def decreaseRoomAlive(self, updatedroom):
        for room in self.rooms:
            if room != updatedroom and self.rooms[room] is not None:
                self.rooms[room].decreaseKA

    def updateTH(self):
        self.avgT, self.avgH = self.calculateTH()

    def calculateTH(self, rooms=None):
        t, h = (0.0, 0.0)
        c = 0
        if rooms is None:
            rooms = self.rooms
        for room in rooms:
            if self.rooms[room].isActive():
                t = t + float(rooms[room].getT())
                h = h + float(rooms[room].getH())
                c += 1
        return (int(float(t) / c), int(float(h) / c))

    def getT(self, room=None):
        return int(self.avgT)

    def getH(self, room=None):
        return int(self.avgH)

    def getOperationMode(self):
        return self.operationmode

    def setOperationMode(self, opm):
        print "OPERATION MODE : " + str(opm)
        self.operationmode = opm

    def updateStatus(self):
        # AlwaysOn
        if self.operationmode == 1:
            self.relayNextStep = self.allwaysOn()
        # Auto
        elif self.operationmode == 2:
            self.relayNextStep = self.auto()
        # keepTemp
        elif self.operationmode == 3:
            self.relayNextStep = self.keepTemp()
        # AlwaysOff
        else:
            self.relayNextStep = self.allwaysOff()
        '''
        if self.nextStep() and self.arUatHome():
            self.relay.setNextStatus(True)
        else:
            self.relay.setNextStatus(False)
    def arUatHome(self):
        return True

        hosts = ['', '']
        if all(os.system("ping -c 1 " + host) for host in hosts):
            return False
        '''

    def nextStep(self):
        self.chkToday()
        if self.relay.getStatus():
            self.CalculateConsumption()
        self.relay.setTime()
        return self.relayNextStep

    def CalculateConsumption(self):
        
        self.relay.addConsumption()


    def chkToday(self):
        today = datetime.datetime.today().date()
        if today != self.relay.getDay():
            self.relay.resetDay()
            self.relay.resetConsumption()
            self.relay.restTime()

    def allwaysOff(self):
        return False

    def allwaysOn(self):
        return True

    def auto(self):
        weekday = {
            0: 'monday',
            1: 'tuesday',
            2: 'wednesday',
            3: 'thursday',
            4: 'friday',
            5: 'saturday',
            6: 'sunday'
        }
        now = datetime.datetime.now()
        # looking for today
        day = weekday[now.weekday()]
        useconf = ''
        rooms = {}
        tSet = ''
        # if today is active I'll use today, otherwise default
        try:
            if self.automode[day]["active"]:
                useconf = day
            else:
                useconf = 'default'
        except Exception as e:
            raise e
        # I select the temperature to maintain now
        for t in self.automode[useconf]['ht']:
            # se ora attuale < orario allora assegno temp
            if datetime.datetime.strptime(str(t), "%H:%M") > datetime.datetime.strptime(str(now.hour) + ":" + str(now.minute), "%H:%M"):
                tSet = float(self.automode[useconf]['ht'][t])
        rooms = 'assegno stanze'
        t, h = self.calculateTH(rooms)
        if tSet <= t + self.kttollerance:
            return True
        else:
            return False

    def keepTemp(self):
        if self.getT() <= (float(self.kt) + self.kttollerance):
            return True
        else:
            return False


class room():

    def __init__(self, ka, label=''):
        self.label = label
        self.active = False
        self.t, self.h = (0.00, 0.00)
        self.old = deque('', 5)
        self.ka = ka
        self.keepAlive = ka

    def isActive(self):
        return self.active

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
        self.keepAlive = self.ka
        self.setActive(True)

    def decreaseKA(self):
        if not self.isActive():
            self.keepAlive = 0
        else:
            self.keepAlive -= 1
            if self.keepAlive < 1:
                self.setActive(False)

    def setActive(self, a):
        self.active = a


class relay():

    def __init__(self):
        # status : [True:UP, False:DOWN, None: not connected]
        self.status = None  # Not connected
        self.keepAlive = 10
        self.consumption = 0.00
        self.lastTimestamp = ''
        self.day = ''

    def getStatus(self):
        return self.status

    def getTime(self):
        return self.lastTimestamp

    def getDay(self):
        return self.day

    def setStatus(self, status):
        self.status = status

    def addConsumption(self, c):
        self.consumption += c

    def resetConsumption(self)
        self.consumption = 0.00

    def resetDay(self):
        self.day = datetime.datetime.today().date()

    def resetTime(self):
        today = datetime.datetime.today().date()
        hourzero = datetime.datetime.strptime('00:00:00', '%H:%M:%S').time()
        self.lastTimestamp = datetime.datetime.combine(today, hourzero) 

    def setTime(self):
        self.lastTimestamp = datetime.datetime.now()
