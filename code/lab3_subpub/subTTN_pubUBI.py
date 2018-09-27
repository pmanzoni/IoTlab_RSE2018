import json
import sys
import time
import base64
import struct

import paho.mqtt.client as mqtt

TTN_BROKER = "eu.thethings.network"
TTN_TOPIC = "+/devices/+/up"

UBIDOTS_BROKER = "things.ubidots.com"

# SET HERE THE VALUES OF YOUR APP AND DEVICE
TTN_USERNAME = "VOID"
TTN_PASSWORD = "VOID"
UBIDOTS_USERNAME =  "VOID"


# The callback for when the client receives a CONNACK response from the server.
def on_connect_ttn(client, userdata, flags, rc):
    print("Connected to ", client._host, "port: ", client._port)
    print("Flags: ", flags, "return code: ", rc)

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(TTN_TOPIC)

def on_connect_ubi(client, userdata, flags, rc):
    print("Connected to ", client._host, "port: ", client._port)
    print("Flags: ", flags, "return code: ", rc)

def on_message_ttn(client, userdata, msg):

    themsg = json.loads(str(msg.payload))
    payload_raw = themsg["payload_raw"]
    payload_plain = base64.b64decode(payload_raw)

    vals = struct.unpack(">fff", payload_plain)

    print("Vals: temp. {} hum. {} lux: {}".format(vals[0], vals[1], vals[2]))

    # JSONining the values according to the Ubidots API indications 
    payload = {"temperature": vals[0], "humidity": vals[1], "luxx": vals[2]}

    client_ubi.connect(UBIDOTS_BROKER, 1883, 60)
    client_ubi.loop_start()

    client_ubi.publish("/v1.6/devices/pysense1", json.dumps(payload))

    client_ubi.loop_stop()


client_ttn = mqtt.Client()
client_ubi = mqtt.Client()

# Let's see if you inserted the required data
if TTN_USERNAME == 'VOID':
    print("\nYou must set the values of your app and device first!!\n")
    sys.exit()
client_ttn.username_pw_set(TTN_USERNAME, password=TTN_PASSWORD)

# Let's see if you inserted the required data
if UBIDOTS_USERNAME == 'VOID':
    print("\nYou must set the values of Ubidots user first!!\n")
    sys.exit()
client_ubi.username_pw_set(UBIDOTS_USERNAME, password=None)

client_ttn.on_connect = on_connect_ttn
client_ubi.on_connect = on_connect_ubi
client_ttn.on_message = on_message_ttn

client_ttn.connect(TTN_BROKER, 1883, 60)

client_ttn.loop_forever()
