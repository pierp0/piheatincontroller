class pages():

    def showIndex(self):
        return 'hello world'




'''
import urlparse
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
'''