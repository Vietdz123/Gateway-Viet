import json
from paho.mqtt import client as mqtt_client
import paho.mqtt.client as mqtt
import paho.mqtt.client as paho  		    #mqtt library

import json
from datetime import datetime
from threading import Thread
import threading
import time


broker = "127.0.0.1"
port = 1883 
topic = "v1/devices/me/rpc/request/+"
ACCESS_TOKEN2 ='ufgVcklJD3yoKTWSBoa9'
TELEMETRY = "v1/devices/me/telemetry"
ATTRIBUTE = "v1/devices/me/attributes"


inf = 'inf'
conf = 'conf'
pin = 'pin'

Group_Led_1 = "Group-Led-1"
Group_Led_2 = "Group-Led-2"
sensorTypeValue = "default"
serialNumber = "serialNumber"
sensorTypeKey = "sensorType"

def convert_boolean(json_string) : 
    python_object = json.loads(json_string)
    python_object['params']['enabled'] = str(python_object['params']['enabled']).lower()
    return python_object

def default_messase_Group1() : 
    payload = init_responce()
    payload = add_json(serialNumber, Group_Led_1, payload)
    payload = add_json(sensorTypeKey, sensorTypeValue, payload)
    return payload

def default_messase_Group2() : 
    payload = init_responce()
    payload = add_json(serialNumber, Group_Led_2, payload)
    payload = add_json(sensorTypeKey, sensorTypeValue, payload)
    return payload

def publishTelemetryStatePin_to_broker(z: str, y: dict) : 
    print("A")
    y = convert_boolean(z)
    client = mqtt_client.Client() 
    client.connect(broker, 1884)
    client.publish(TELEMETRY, '{"serialNumber": "Group-Led-1", "sensorType": "default", "enabled2": "false", "STATE": "ON"}')
    del client
    print("F")
    # if y["params"]["pin"] == 1 : 
    #     payload = default_messase_Group1()

    #     payload = add_json("enabled" + str(y["params"]["pin"]), y["params"]["enabled"], payload)
    #     payload = check_state(payload, "true")                   
    #     print('payload ' + payload)
    #     client.publish(TELEMETRY, payload)

    # elif y["params"]["pin"] == 2 : 
    #     payload = default_messase_Group2()
    #     payload = add_json("enabled" + str(y["params"]["pin"]), y["params"]["enabled"], payload)
    #     payload = check_state(payload, "true")                   
    #     print('payload ' + payload)
       
    #     client.publish(TELEMETRY, payload)

def connect_mqtt() -> mqtt_client:
    uart = mqtt_client.Client()  
    uart.connect('127.0.0.1', 1884)
    return uart

def connect_mqtt_token(TOKEN: str) -> mqtt_client:
    client = mqtt_client.Client()  
    client.username_pw_set(TOKEN)
    client.connect(broker, port, keepalive=60)
    return client

def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic") 
        y = json.loads(msg.payload.decode())                         #convert sang json  
        z = json.dumps(y)  
        print("B")
        publishTelemetryStatePin_to_broker(z, y)
    
    client.on_message = on_message
    client.subscribe(topic)



def run(client: mqtt_client) :
    client.loop_forever()


def default_notValid(client: mqtt_client, responce) :
    payload = init_responce()
    payload = add_json("Key", "Json", payload)
    payload = add_json("Valid", "Not", payload)

    client.publish(ATTRIBUTE, payload)
    client.publish(responce, payload)   

def check_state(fullstring: str, substring: str) :
    if fullstring.find(substring) != -1:

        fullstring = add_json("STATE", "ON", fullstring)
        return fullstring
    else:
        fullstring = add_json("STATE", "OFF", fullstring)
        return fullstring    

def init_responce() :
    payload = "{}"
    return payload

def add_json(key , value, responce: str):
    json_responce = json.loads(responce)
    json_responce[key] = value
    payload = json.dumps(json_responce)
    return payload

if __name__ == '__main__':
    # client = connect_mqtt()
    client_token = connect_mqtt_token(ACCESS_TOKEN2)
    # client_arr = [client, client_token]

    # subscribe(client)
    subscribe(client_token)
    #t1 = threading.Thread(target=run, args=(client,))
    t2 = threading.Thread(target=run, args=(client_token,))
    #t1.start()
    t2.start()