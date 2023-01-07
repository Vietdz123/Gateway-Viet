import json
from paho.mqtt import client as mqtt_client

import paho.mqtt.client as paho  		    #mqtt library
import os
import json
import time
from datetime import datetime
from threading import Thread
import threading

def add_json(key , value, responce: str):
    json_responce = json.loads(responce)
    json_responce[key] = value
    payload = json.dumps(json_responce)
    return payload

x =  '{"method":"inf","params":{"TY":0,"EX":"0x00","ID":0}}'

# parse x:
vl = json.loads(x)
y = json.dumps(vl)

# the result is a Python dictionary:
print(vl["params"])


if "method" in x and "params" in x  and "TY" in x:
	print("exist>>>>")