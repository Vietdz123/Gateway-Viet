import json
from paho.mqtt import client as mqtt_client
import paho.mqtt.client as mqtt
import paho.mqtt.client as paho  		    #mqtt library

import json
import time
from datetime import datetime
from threading import Thread
import threading
import time
import serial
import re

broker = "127.0.0.1"
port = 1884

TELEMETRY = "v1/devices/me/telemetry"
ATTRIBUTE = "v1/devices/me/attributes"
topic_connect = "sensor/connect"

topic = 'v1/device/+/request/+/+'

inf = 'inf'
conf = 'conf'
pin = 'pin'

Group_Led_1 = "Group-Led-1"
Group_Led_2 = "Group-Led-2"
sensorTypeValue = "default"
serialNumber = "serialNumber"
sensorTypeKey = "sensorType"

z1baudrate = 38400
z1port = '/dev/pts/4'

def pushUpdateConfigureToThingsboard(TY, ID ,ON, DI,  TI, SE) :
    payload = init_responce()
    payload = add_json('TY', str(TY), payload)
    payload = add_json('ID', str(ID), payload)
    payload = add_json('ON', str(ON), payload)
    payload = add_json('DI', str(DI), payload)
    payload = add_json('TI', str(TI), payload)
    payload = add_json('SE', str(SE), payload)
    return payload 

def pushUpdateConfigureToDevice(TY, ID ,ON, DI,  TI) :
    payload = init_responce()
    payload = add_json('TY', str(TY), payload)
    payload = add_json('ID', str(ID), payload)
    payload = add_json('ON', str(ON), payload)
    payload = add_json('DI', str(DI), payload)
    payload = add_json('TI', str(TI), payload)
    return payload      

def pushUpdateInformationToDevice(TY, ID, EX) :
    payload = init_responce()
    payload = add_json('TY', str(TY), payload)
    payload = add_json('ID', str(ID), payload)
    payload = add_json('EX', str(EX), payload)
    print(payload)
    return payload  


def config_uart() :
    serial_connection = serial.Serial(port=z1port,
                                    baudrate = z1baudrate,
                                    bytesize=serial.EIGHTBITS,
                                    parity=serial.PARITY_NONE,
                                    stopbits=serial.STOPBITS_ONE,
                                    timeout=1)
    return serial_connection


def respond_message(z: str, y: dict, responce: str, client: mqtt_client):
    try: 
        if z.count(inf) != 0 and "TY" in z and "EX" in z and "ID" in z :
            serial_uart = config_uart()
            payload = pushUpdateInformationToDevice(y["params"]["TY"], y["params"]["ID"], y["params"]["EX"])

            client.publish(TELEMETRY, payload)
            client.publish(responce, payload)

            print('Set information: ' + payload)
            payload = payload.encode("utf-8")
            serial_uart.write(payload)
            
            
        elif z.count(conf) != 0 and "TY" in z and "ID" in z and "ON" in z and "DI" in z and "TI" in z:    
            serial_uart = config_uart()
            payload = pushUpdateConfigureToDevice(y["params"]["TY"], y["params"]["ID"], y["params"]["ON"], y["params"]["DI"], y["params"]["TI"])
            
            client.publish(TELEMETRY, payload)
            client.publish(responce, payload)

            print('Set configuration: ' + payload)
            payload = payload.encode("utf8")
            serial_uart.write(payload)
            

        elif z.count(pin) != 0 and "enabled" in z : #and "Group" in z:  
            
            print("Controled PIN >>>>>>>>")    
            serial_uart = config_uart()
            
            payload = default_messase_Group1()
            payload = add_json(y["pin"], y["enabled"], payload)
            temp = convert_boolean(z)                   #convert true to "true"
            payload = add_json("enabled" + str(temp["pin"]), temp["enabled"], payload)
            payload = check_state(payload, "true")  
            print(payload)
            client.publish(responce, payload)
            client.publish(TELEMETRY, payload)

            y  = convert_boolean(z)  
            payload_uart = init_responce()
            payload_uart = add_json("ID", y["pin"], payload_uart)
            payload_uart = add_json("TY", 1, payload_uart)

            if str(y["enabled"]) == "true" :
                payload_uart = add_json("ON", 1, payload_uart)
                print('payload_uart control led: ' + payload_uart)
                payload_uart = payload_uart.encode("utf8")
                serial_uart.write(payload_uart)
            else :
                payload_uart = add_json("ON", 0, payload_uart)
                print('payload_uart control led: ' + payload_uart)
                payload_uart = payload_uart.encode("utf8")
                serial_uart.write(payload_uart)                

        elif y["method"] == "dim0" : 
            serial_uart = config_uart()
            payload_uart = init_responce()
                
            payload_uart = add_json("ID", 0, payload_uart)
            payload_uart = add_json("TY", 1, payload_uart)
            payload_uart = add_json("DI", y["params"], payload_uart)

            print('Payload_uart control dim: ' + payload_uart)

            client.publish("v1/devices/me/telemetry", payload_uart)
            client.publish(responce, payload_uart)

            payload = payload_uart.encode("utf8")
            serial_uart.write(payload)
            

        elif y["method"] == "dim1" : 
            serial_uart = config_uart()
            payload_uart = init_responce()
                
            payload_uart = add_json("ID", 1, payload_uart)
            payload_uart = add_json("TY", 1, payload_uart)
            payload_uart = add_json('DI', str(y["params"]), payload_uart)
            print('payload_uart control dim: ' + payload_uart)

            client.publish(TELEMETRY, payload_uart)  
            client.publish(responce, payload_uart)

            payload = payload_uart.encode("utf-8")
            serial_uart.write(payload) 
                        
        else :
            default_notValid(client, responce)
    
    except:
        default_notValid(client, responce)        




def connect_group1() :
    payload = init_responce()
    payload = add_json("SerialNumber", Group_Led_1, payload)
    return payload

def connect_group2() :
    payload = init_responce()
    payload = add_json("SerialNumber", Group_Led_2, payload)
    return payload

def connect_mqtt() -> mqtt_client:
    uart = mqtt_client.Client()  
    uart.connect('127.0.0.1', 1884)
    return uart

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
def is_json(message) :
    try:
        data = json.loads(message)
        if isinstance(data, dict):
            a = json.dumps(data)
            kq = a.count("{") - a.count("}") 
            if kq != 0 or a.count("\\") != 0 :
                return None
            return True
        else:
            return  None
    except json.JSONDecodeError:
            print("The message is not a valid JSON")
            return None

def init_responce() :
    payload = "{}"
    return payload

def add_json(key , value, responce: str):
    json_responce = json.loads(responce)
    json_responce[key] = value
    payload = json.dumps(json_responce)
    return payload


def convert_boolean(json_string) : 
    python_object = json.loads(json_string)
    python_object['enabled'] = str(python_object['enabled']).lower()
    return python_object

def default_messase_Group1() : 
    payload = init_responce()
    payload = add_json(serialNumber, Group_Led_1, payload)
    payload = add_json(sensorTypeKey, sensorTypeValue, payload)
    return payload

def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic") 
        isJson = is_json(msg.payload.decode())
        repsonTopic = str(msg.topic)
        responce =  repsonTopic.replace("request", "response")
        if isJson == True :   
            y = json.loads(msg.payload.decode())                         #convert sang json  
            z = json.dumps(y)                                            #convert to string                       
            respond_message(z, y, responce, client)
        else :
            default_notValid(client, responce)


    client.on_message = on_message
    
    client.subscribe(topic)
    client.publish(topic_connect, connect_group1())
    client.publish(TELEMETRY, '{"serialNumber": "Group-Led-1", "sensorType": "default", "trash": "trash"}')
    client.publish(topic_connect, connect_group2())
    client.publish(TELEMETRY, '{"serialNumber": "Group-Led-2", "sensorType": "default", "trash": "trash"}')

if __name__ == '__main__':
    client = connect_mqtt()

    subscribe(client)
    t1 = threading.Thread(target=run, args=(client,))
    t1.start()
    while True : 
        time.sleep(10)
        client.publish(TELEMETRY, '{"serialNumber": "Group-Led-2", "sensorType": "default", "trash": "trash"}')

    
