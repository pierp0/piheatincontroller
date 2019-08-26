from heatController import heatController
import datetime
import yaml

DEBUG = True


class pages():

    def __init__(self, config=False):
        with open('./config.yml', 'r') as confFile:
            conf = yaml.load(confFile)
        self.HC = heatController(
            conf['rooms'], conf['mode']['kt'], conf['mode']['auto'])
        self.config = bool(config)

    def showIndex(self):
        try:
            with open('./www/index.html', 'r') as index:
                return index.read()
        except Exception as e:
            raise e

    def getCss(self):
        try:
            with open("./www/css/style.css") as f:
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

    def getConsumption(self):
        # print "\nCONSUMO: " + str((self.HC.getConsumption() / 3600))
        return round((self.HC.getConsumption() / 3600), 1)

    def getRommsPage(self):
        pass

    def getForecast(self):
        pass

    def getOperationMode(self):
        return self.HC.getOperationMode()

    def setRelayStatus(self, newdata):
        for key, value in newdata:
            if key == 's':
                if DEBUG:
                    print "\nvsetRelayStatus : " + str(value[0])
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

    def setMode(self, m):
        try:
            self.HC.setOperationMode(int(m[0][1][0]))
            return self.showIndex()
        except Exception as e:
            raise e

    def setError(self):
        pass

    def postHello(self, mac):
        macaddr = str(mac[0][1][0])
        if self.config:
            label = raw_input('Plaese add label for sensor ' + macaddr + '\n')
            with open('./config.yml', 'r') as confFile:
                conf = yaml.load(confFile)
            conf['rooms'][macaddr] = label
            with open('./config.yml', 'w') as confFile:
                yaml.dump(conf, confFile, default_flow_style=False)
            print 'Sensor has been recorded. Please turn off this sensor and turn on the next one.'
            print 'If the process is completed press ^c to terminate'
        else:
            self.HC.addSensor(macaddr)
