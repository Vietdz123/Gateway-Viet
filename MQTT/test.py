import json
from paho.mqtt import client as mqtt_client
import paho.mqtt.client as mqtt
import paho.mqtt.client as paho  		    #mqtt library

import json
import time
from datetime import datetime
from threading import Thread
import threading
import re

# TELEMETRY = "v1/devices/me/telemetry"

# ACCESS_TOKEN1 ='ufgVcklJD3yoKTWSBoa9'

# topic = "v1/devices/me/rpc/request/+"

# def init_responce() :
#     payload = "{}"
#     return payload

# def add_json(key , value, responce: str):
#     json_responce = json.loads(responce)
#     json_responce[key] = value
#     payload = json.dumps(json_responce)
#     return payload

# def on_message(client, userdata, message):
#   print(f"Received message '{message.payload.decode()}' on topic '{message.topic}'")

# client = mqtt.Client()
# client.username_pw_set(ACCESS_TOKEN1)
# client.connect("127.0.0.1", 1883, 60)



# # Define the message to be published
# payload_uart = init_responce()
# payload_uart = add_json("DI", "12", payload_uart)
# payload_uart = add_json("TI", "aabb", payload_uart)
# message = {"DI" : "123"}

# # Publish the message
# client.publish(TELEMETRY, payload_uart)
# #client.subscribe(topic)
# #client.on_message = on_message
# client.loop_forever()
def check(message) :
  try:
    #data = json.loads(message)
    if isinstance(message, dict):
      print("The message is a dictionary")

    else:
      print("The message is not a dictionary")
  except json.JSONDecodeError:
    print("The message is not a valid JSON")

message = '{"TY":1,"ID":1,"ON":0,"DI":30, "TI":1}'
message2 =  '{"method":"config","params":"{\"TY\":0,\"EX\":\"0x00\",\"ID\":0"}'
message3 =  '{"method":"config","params":"{\"TY\":0,\"EX\":\"0x00\",\"ID\":0"}'
message4 = {'method': 'config', 'params': '{"TY":0,"EX":"0x00","ID":0'}

a = json.dumps(message4)
a = a.count("{") - a.count("}") 
print(a)
print("\"\"")

# check(message4)
# print(message4["params"]["TY"])