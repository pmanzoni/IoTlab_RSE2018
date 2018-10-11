# file: a_simple_pub.py

from mqtt import MQTTClient
import pycom
import sys
import time

import ufun

wifi_ssid = 'THE_NAME_OF_THE_AP'
wifi_passwd = 'THE_WIFI_PASSWORD'
broker_addr = 'THE_NAME_OF_THE_BROKER'
dev_id = 'NAME_YOUR_DEVICE'

def settimeout(duration):
   pass

def get_data_from_sensor(sensor_id="RAND"):
    if sensor_id == "RAND":
        return ufun.random_in_range()

### if __name__ == "__main__":

ufun.connect_to_wifi(wifi_ssid, wifi_passwd)

client = MQTTClient(dev_id, broker_addr, 1883)

print ("Connecting to broker: " + broker_addr)
try:
	client.connect()
except OSError:
	print ("Cannot connect to broker: " + broker_addr)
	sys.exit()	
print ("Connected to broker: " + broker_addr)

print('Sending messages...')
while True:
    # creating the data
    the_data = get_data_from_sensor()
    # publishing the data
    client.publish('THE_TOPIC_TO_BE_USED', str(the_data))
    time.sleep(1)
