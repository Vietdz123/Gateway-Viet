import json
from paho.mqtt import client as mqtt_client

import paho.mqtt.client as paho  		    #mqtt library
import os
import json
import time
from datetime import datetime
from threading import Thread
import threading


def check_state(fullstring: str, substring: str) :
    if fullstring.find(substring) != -1:
        payload_telemetry =  {"STATE": "ON"}
        payload_telemetry = json.dumps(payload_telemetry)       # return string
        return payload_telemetry
    else:
        payload_telemetry =  {"STATE": "OFF"}
        payload_telemetry = json.dumps(payload_telemetry)       # return string
        return payload_telemetry    

def init_responce() :
    payload = "{}"
    return payload

def add_json(key , value, responce: str):
    json_responce = json.loads(responce)
    json_responce[key] = value
    payload = json.dumps(json_responce)
    return payload