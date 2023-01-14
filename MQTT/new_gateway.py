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
port = 1885

TELEMETRY = "v1/devices/me/telemetry"
ATTRIBUTE = "v1/devices/me/attributes"
topic_connect = "sensor/connect"
topic = 'v1/device/+/request/+/+'

inf = 'inf'
conf = 'conf'
pin = 'pin'

Group_Led_1 = "Group-Led-1"
sensorTypeValue = "default"
serialNumber = "serialNumber"
sensorTypeKey = "sensorType"

z1baudrate = 38400
z1port = '/dev/ttyUSB0'

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Helpers
def pushUpdateConfigureToThingsboard(ID ,ON, DI,  TI, SE) :
    payload = default_messase_Group1()
    payload = add_json('ID', str(ID), payload)
    payload = add_json('ON', str(ON), payload)
    payload = add_json('DI', str(DI), payload)
    payload = add_json('TI', str(TI), payload)
    payload = add_json('SE', str(SE), payload)
    return payload 

def pushUpdateConfigureToDevice(TY, ID , ON, DI,  TI) :
    payload = default_messase_Group1()
    payload = add_json('TY', str(TY), payload)
    payload = add_json('ID', str(ID), payload)
    payload = add_json('ON', str(ON), payload)
    payload = add_json('DI', str(DI), payload)
    payload = add_json('TI', str(TI), payload)
    return payload      

def pushUpdateInformationToDevice(TY, ID, EX) :
    payload = default_messase_Group1()
    payload = add_json('TY', str(TY), payload)
    payload = add_json('ID', str(ID), payload)
    payload = add_json('EX', str(EX), payload)
    return payload  

def default_notValid(client: mqtt_client, responce) :
    payload = default_messase_Group1()
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
                print("Not valid Format")
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

def checkTypeMessage(ID = 0, TY = 0, ON = 0, DI = 10.5, TI = 5, SE = 6, EX = "0x12") : 
    EX = int(EX, 16)
    EX = hex(EX)    # Check is hex or not
    if isinstance(ID, int) and isinstance(TY, int) and isinstance(ON, int) and isinstance(DI, (float, int)) and isinstance(TI, int) :
        return True
    else :
        print("Not Type")
        return None

def checkValidMessage(TY = 0, ON = 1, DI = 50.5, TI = 10, SE = 100) : 
    print(  TY + DI + TI + SE + SE)
    if TY != 0 and TY != 1 :
        return None

    if ON != 0 and ON != 1 :
        return None

    if DI < 0 or DI > 100:
        return None
    
    if TI < 10 :
        return None
    
    if SE < 0:
        return None
    
    return True

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> UART
def config_uart() :
    serial_connection = serial.Serial(port=z1port,
                                    baudrate = z1baudrate,
                                    bytesize=serial.EIGHTBITS,
                                    parity=serial.PARITY_NONE,
                                    stopbits=serial.STOPBITS_ONE,
                                    timeout=1)
    return serial_connection

def run_uart(client: mqtt_client) :
    z1serial = config_uart()

    if z1serial.is_open:
        while True:
            size = z1serial.inWaiting()
            if size:
                try:
                    data_uart = z1serial.readline(size)
                    data_uart = data_uart.decode()
                    print(data_uart)

                    data_uart_dic = json.loads(data_uart)
                    if data_uart.count('ID') != 0 and "ON" in data_uart and "DI" in data_uart and "TI" in data_uart and "SE" in data_uart :
                        payload = pushUpdateConfigureToThingsboard(data_uart_dic["ID"] , data_uart_dic["ON"], data_uart_dic["DI"], data_uart_dic["TI"], data_uart_dic["SE"])
                        
                        client.publish(TELEMETRY, payload)

                    else :
                        print("Data Received Through UART Not Valid")              
                except:
                    print("Data Received Through UART Not Valid except")  

            else :
                time.sleep(1)
                
    else:
        print ('z1serial not open')


#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Hanlde Responce RPC To Thingsboard and Send Configure to Device
def respond_message(z: str, y: dict, responce: str, client: mqtt_client):
    try: 
        if z.count(inf) != 0 and "TY" in z and "EX" in z and "ID" in z :
            check = checkTypeMessage(ID = y["params"]["ID"], TY = y["params"]["TY"], EX = y["params"]["EX"])
            if check == None :
                default_notValid(client, responce)
                return
            check = checkValidMessage(TY = y["params"]["TY"])
            if check == None :
                default_notValid(client, responce)
                return

            serial_uart = config_uart()
            payload = pushUpdateInformationToDevice(y["params"]["TY"], y["params"]["ID"], y["params"]["EX"])

            client.publish(TELEMETRY, payload)
            client.publish(responce, payload)

            print('Set information: ' + payload)

            payload = "{}"
            payload = add_json('TY', y["params"]["TY"], payload)
            payload = add_json('ID', y["params"]["ID"], payload)
            payload = add_json('EX', str(y["params"]["EX"]), payload)

            payload.replace(" ", "")
            print(payload)
            payload = payload.encode("utf-8")
            serial_uart.write(payload)
            
        #Dieu khien cac thong so cho Led
        elif z.count(conf) != 0 and "TY" in z and "ID" in z and "ON" in z and "DI" in z and "TI" in z:    
            check = checkTypeMessage(ID = y["params"]["ID"], TY = y["params"]["TY"], ON = y["params"]["ON"], DI = y["params"]["DI"], TI = y["params"]["TI"])
            if check == None :
                default_notValid(client, responce)
                return
            check = checkValidMessage(TY = y["params"]["TY"], ON = y["params"]["ON"], DI = y["params"]["DI"], TI = y["params"]["TI"])
            if check == None :
                default_notValid(client, responce)
                return
            
            
            serial_uart = config_uart()
            payload = pushUpdateConfigureToDevice(y["params"]["TY"], y["params"]["ID"], y["params"]["ON"], y["params"]["DI"], y["params"]["TI"])
            
            client.publish(TELEMETRY, payload)
            client.publish(responce, payload)
            print('Set configuration: ' + payload)

            payload = "{}"
            payload = add_json('TY', y["params"]["TY"], payload)
            payload = add_json('ID', y["params"]["ID"], payload)
            payload = add_json('ON', y["params"]["ON"], payload)
            payload = add_json('DI', y["params"]["DI"], payload)
            payload = add_json('TI', y["params"]["TI"], payload)
            payload.replace(" ", "")
            print(payload)

            payload = payload.encode("utf8")
            serial_uart.write(payload)
            
        #Dieu khien tat bat led
        elif z.count(pin) != 0 and "enabled" in z :           
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

        #Dieu khien Dim Led
        elif "dim" in y["method"] or y["method"].find("dim")!=-1 :
            try :
                index = y["method"].find("dim")
                numberDim = y["method"][index+3:]
                numberDim = int(numberDim) 
                value_params = y["params"]

                value_params = float(value_params)
                a = isinstance(value_params, float)
                if a == True :
                    serial_uart = config_uart()
                    payload_responce_thingsboard = default_messase_Group1()
                    payload_responce_thingsboard = add_json("ID", numberDim, payload_responce_thingsboard)
                    #payload_responce_thingsboard = add_json("TY", 1, payload_responce_thingsboard)
                    payload_responce_thingsboard = add_json('DI', value_params, payload_responce_thingsboard)                    

                    client.publish(TELEMETRY, payload_responce_thingsboard)  
                    client.publish(responce, payload_responce_thingsboard)

                    payload_uart = init_responce()
                    payload_uart = add_json("ID", numberDim, payload_uart)
                    #payload_uart = add_json("TY", 1, payload_uart)
                    payload_uart = add_json('DI', value_params, payload_uart)
                    print('payload_uart control dim: ' + payload_uart)
                    payload = payload_uart.encode("utf-8")
                    serial_uart.write(payload) 
                
                else :
                    default_notValid(client, responce)
            
            except :
                default_notValid(client, responce)
                        
        else :
            default_notValid(client, responce)
    
    except:
        default_notValid(client, responce)        


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Connect Broker and Thingsboard
def connect_group1() :
    payload = init_responce()
    payload = add_json("SerialNumber", Group_Led_1, payload)
    return payload

def default_messase_Group1() : 
    payload = init_responce()
    payload = add_json(serialNumber, Group_Led_1, payload)
    payload = add_json(sensorTypeKey, sensorTypeValue, payload)
    return payload

def connect_mqtt() -> mqtt_client:
    uart = mqtt_client.Client()  
    uart.connect(broker, port)
    return uart

def run(client: mqtt_client) :
    client.loop_forever()

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

if __name__ == '__main__':
    client = connect_mqtt()
    client_uart = connect_mqtt()

    client.publish(topic_connect, connect_group1())
    client.publish(TELEMETRY, '{"serialNumber": "Group-Led-1", "sensorType": "default", "trash": "trash"}')

    subscribe(client)

    t1 = threading.Thread(target=run, args=(client,))
    t2 = threading.Thread(target=run_uart, args=(client_uart,))
    t1.start()
    t2.start()

    while True : 
        time.sleep(20)
        client.publish(TELEMETRY, '{"serialNumber": "Group-Led-1", "sensorType": "default", "trash": "trash"}')
        client_uart.publish(TELEMETRY, '{"serialNumber": "Group-Led-1", "sensorType": "default", "trash": "trash"}')
    
