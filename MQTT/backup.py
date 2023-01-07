import json
from paho.mqtt import client as mqtt_client

import paho.mqtt.client as paho  		    #mqtt library
import os
import json
import time
from datetime import datetime
from threading import Thread
import threading
import mqtt
import lib

topic = "v1/devices/me/rpc/request/+"

def connect_mqtt() -> mqtt_client:
    client = mqtt_client.Client()  
    client.connect('127.0.0.1', 1884)
    return client

def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received {msg.payload.decode()} from `{msg.topic}` topic")
        y = json.loads(msg.payload.decode())                        #convert sang dicionary
        z = json.dumps(y)                                           #convert to string

        if (y["ID"] == 1) :
            print("1")

        if (y["ID"] == 2) :
            print("2")       

    print("CALLBACK>>>>>>>>>>>>>>>>>>>>>>>>")
    client.on_message = on_message
    client.subscribe(topic)

def run(client: mqtt_client) :
    client.loop_forever()

client = connect_mqtt()
subscribe(client=client)
run(client=client)


