from iqoptionapi.stable_api import IQ_Option
from dotenv import load_dotenv
from datetime import datetime
import time
import os

load_dotenv()

Iq=IQ_Option(os.getenv("USER"),os.getenv("PASS"))
Iq.connect()#connect to iqoption

while True:
    minutos = float(((datetime.now()).strftime('%M.%S')))
    print(minutos)
    time.sleep(60)
velas=Iq.get_candles("EURUSD", 300, 5, time.time())
print(velas)
for i in range(5):
    velas[i] = 'g' if velas[i]['open'] < velas[i]['close'] else 'r' if velas[i]['open'] > velas[i]['close'] else 'd'
		

cores = f'{velas[0]} {velas[1]} {velas[2]} {velas[3]} {velas[4]}'
print(cores)