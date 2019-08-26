from collections import deque
import os
import datetime

DEBUG = False

class heatController():

    def __init__(self, roomslist, ktmode, automode):
        self.avgT, self.avgH = (0.00, 0.00)
        self.rooms = {}
        for r in roomslist:
            self.rooms[r] = room(roomslist[r], 3 * len(roomslist))
        self.relay = relay()
        # self.kttemperature = ktmode['temperature']
        self.ktmode = ktmode
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
        if DEBUG:
            print "\nOperation mode : " + str(self.operationmode)
        return self.operationmode

    def getConsumption(self):
        return self.relay.getConsumption()

    def setOperationMode(self, opm):
        if DEBUG:
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
        
    def arUatHome(self):
        # List of configured IPs. mobile, laptop or someone else. If one of those IP is up, u ar at home  
        hosts = self.automode['whoisathome']
        # This function return true if ping fail. if all ping fail noone is at home
        if all(os.system("ping -c 1 " + host) for host in hosts):
            # All IPs ar down
            return False
        else:
            # There is one or more IPs up
            return True

    def nextStep(self):
        now = datetime.datetime.now()
        self.chkToday(now)
        if DEBUG:
            print "\nGetstatus : " + str(self.relay.getStatus())
        if self.relay.getStatus():
            self.relay.addTodayOn(now)
        else:
            self.relay.addTodayOff(now)
        self.relay.setChkPoint(now)
        return self.relayNextStep

    def chkToday(self, now):
        if now.date() != self.relay.getDtChkPoint().date():
            self.relay.resetDtChkPoint()

    def allwaysOff(self):
        return False

    def allwaysOn(self):
        return True

    def auto(self):
        try:
            # If noone is at home auto mode shift to lowdefault temperature
            if self.arUatHome(): 
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
                # rooms = {}
                # if today is active I'll use today, otherwise default
                try:
                    if self.automode[day]["active"]:
                        useconf = day
                    else:
                        useconf = 'default'
                except Exception as e:
                    raise e
                # mindelta value is from 0 to 24h in ms. it's used to determinate the correct interval in conf file
                mindelta = 86400000
                # I select the temperature to maintain now
                # Store actual hous and minutes in actualtime
                actualtime = datetime.datetime.strptime(str(now.hour) + ":" + str(now.minute), "%H:%M")
                # The for cicle have not ordered elements thus we need to find the max configurated hour that is minus then actualhour 
                for t in self.automode[useconf]['ht']:
                    # Store configured hour and minute in configuredtime
                    configuredtime = datetime.datetime.strptime(str(t), "%H:%M")
                    # Envalue only configuredtime minus then actualtime
                    if  configuredtime < actualtime:
                        # Delta in milliseconds
                        delta = (actualtime - configuredtime).total_seconds()
                        # If this delta is better then mindelta I've found a new tSet
                        if delta < mindelta:
                            mindelta = delta
                            tSet = float(self.automode[useconf]['ht'][t])
                            if DEBUG:
                                print tSet 
                # rooms = 'assegno stanze'
            else:
                tSet = float(self.automode['lowdefault'])
                if DEBUG:
                    print '\n\nLOWDEFAULT'
            t, h = self.calculateTH()  # (rooms)
            if DEBUG:
                print "\nTSET : " + str(tSet)
            if float(t) <= tSet + float(self.automode['tollerance']):
                return True
            else:
                return False
        
        except Exception as e:
           raise e
        

    def keepTemp(self):
        if self.getT() <= (float(self.ktmode[temperature]) + float(self.ktmode[tollerance])):
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
        self.status = False  # Not connected
        self.keepAlive = 10
        self.dtChkPoint = datetime.datetime.now()
        self.todayOn = 0.00
        self.todayOff = 0.00
        self.oldOn = deque('', 5)
        self.oldOff = deque('', 5)

    def getStatus(self):
        if DEBUG:
            print "\nSTATUS : " + str(self.status)
        return bool(self.status)

    def getDtChkPoint(self):
        return self.dtChkPoint

    def getConsumption(self):
        return self.todayOn

    def setStatus(self, status):
        self.status = bool(status)
        if DEBUG:
            print "\n SetStatus : " + str(status)

    def addTodayOn(self, now):
        if DEBUG:
            print "\nNow : " + str(now)
            print "\nCHKPOINT : " + str(self.dtChkPoint)
            print "\nAdd today : " + str((now - self.dtChkPoint).total_seconds())
        self.todayOn += (now - self.dtChkPoint).total_seconds()

    def addTodayOff(self, now):
        self.todayOff += (now - self.dtChkPoint).total_seconds()

    def resetDtChkPoint(self):
        self.dtChkPoint = datetime.datetime.now()
        self.oldOn.appendleft(self.todayOn)
        self.oldOff.appendleft(self.todayOff)
        self.todayOn = 0
        self.todayOff = 0

    def setChkPoint(self, now):
        self.dtChkPoint = now
