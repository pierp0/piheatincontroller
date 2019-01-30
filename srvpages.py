from heatController import heatController
import datetime


class pages():

    def __init__(self):
        self.HC = heatController()

    def showIndex(self):
        try:
            with open('./WWW/index.html', 'r') as index:
                page = index.read()
                page = page.replace('TEMPERATURE', str(self.HC.getT()))
                page = page.replace('HUMIDITY', str(self.HC.getH()) + '%')
                # page.replace('', str(self.HC.getT()))
            return str(page)
        except Exception as e:
            raise e

    def getStatus(self):
        return self.HC.nextStatus()

    def getTemp(self):
        return self.HC.getT()

    def dump(self, newdata):
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
