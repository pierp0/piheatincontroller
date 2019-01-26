import requests
from random import randint
import time

while True:
    sl = randint(5, 15)
    t = randint(1500, 2500) / 100
    h = randint(50, 100)
    st = randint(1, 5)
    time.sleep(sl)
    requests.post("http://127.0.0.1:12345/postHT", data={"t": t, "h": h, "s": st, "r": 1})


    # curl -d 'r=6&t=0&h=0' http://localhost:12345/postHT
