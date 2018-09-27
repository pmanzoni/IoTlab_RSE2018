from mqtt import MQTTClient
import pycom
import sys
import time
import json


import ufun

from pysense import Pysense
from SI7006A20 import SI7006A20
import pycom
import micropython
import machine
import time

wifi_ssid = 'THE_NAME_OF_THE_AP'
wifi_passwd = 'THE_WIFI_PASSWORD'
broker_addr = 'THE_NAME_OF_THE_BROKER'
user_name = 'YOUR_UBIDOTS_USERNAME'
dev_id = 'NAME_YOUR_DEVICE'
topic_is = "TOPIC_TO_BE_USED"


def settimeout(duration):
   pass

### if __name__ == "__main__":

py = Pysense()
tempHum = SI7006A20(py)

ufun.connect_to_wifi(wifi_ssid, wifi_passwd)

client = MQTTClient(dev_id, broker_addr, 1883, user=user_name, password='None')

print ("Connecting to broker: " + broker_addr)
try:
	client.connect()
except OSError:
	print ("Cannot connect to broker: " + broker_addr)
	sys.exit()	
print ("Connected to broker: " + broker_addr)

print('Sending messages...')
while True:
    temperature = tempHum.temp()
    print("Temperature: {} Degrees".format(temperature))

    sensor_value = {'value': temperature}

    # publishing the data
    client.publish(topic_is, json.dumps(sensor_value))
    time.sleep(1)
