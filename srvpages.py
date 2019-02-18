from heatController import heatController
import datetime
import yaml


class pages():

    def __init__(self):
        with open('./config.yml', 'r') as confFile:
            conf = yaml.load(confFile)
        self.HC = heatController(
            conf['rooms'], conf['mode']['kt'], conf['mode']['scheduler'])

    def showIndex(self):
        try:
            with open('./WWW/index.html', 'r') as index:
                return index.read()
        except Exception as e:
            raise e

    def getCss(self):
        try:
            with open("./WWW/css/style.css") as f:
                return f.read()
        except Exception as e:
            raise e

    def getStatus(self):
        return self.HC.relay.getStatus()

    def getNextStep(self):
        return self.HC.nextStep()

    def getTemp(self):
        return self.HC.getT()

    def getHum(self):
        return self.HC.getH()

    def getRommsPage(self):
        pass

    def getConsumption(self):
        pass

    def getForecast(self):
        pass

    def getOperationMode(self):
        return self.HC.getOperationMode()

    def setRelayStatus(self, newdata):
        for key, value in newdata:
            if key == 's':
                print value[0]
                self.HC.relay.setStatus(value[0])

    def setHT(self, newdata):
        data = {'room': '', 'time': '', 'temp': '', 'humidity': ''}
        for key, value in newdata:
            if key == 't':
                data['temp'] = value[0]
            elif key == 'h':
                data['humidity'] = value[0]
            elif key == 'r':
                data['room'] = value[0]
            else:
                print value[0]
        data['time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.HC.setDataFromSensor(data)

    def setAuto(self, *args):
        self.HC.setOperationMode(2)

    def setAlwaysOn(self, *args):
        self.HC.setOperationMode(1)

    def setAlwaysOff(self, *args):
        self.HC.setOperationMode(0)

    def setKT(self, *args):
        self.HC.setOperationMode(3)

    def setError(self):
        pass

    def postHello(self, mac):
        self.HC.addSensor(mac)
