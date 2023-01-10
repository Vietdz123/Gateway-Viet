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

broker= "127.0.0.1"   			        #host name
port = 1883 					            #data listening port
ACCESS_TOKEN1 = 'ufgVcklJD3yoKTWSBoa9'    #Smart-lighting -VietPro -- Group Led 1
ACCESS_TOKEN2 ='8rQoOpUxcBmUVkkZaVOb'   # viet : group Led 2 
ACCESS_TOKEN3 = 'VPsng4Dk3KXh0NTKwhVt'   # Update infor
TELEMETRY = "v1/devices/me/telemetry"
ATTRIBUTE = "v1/devices/me/attributes"
topic = "v1/devices/me/rpc/request/+"

inf = 'inf'
conf = 'conf'
pin = 'pin'

# broker = "18.142.122.22"
# ACCESS_TOKEN1 = 'pxws00N2W6VWKQc1kTnC'    #Smart-lighting -VietPro -- Group Led 1
# ACCESS_TOKEN2 ='RJAkDkTtOJJmvfNGeC8x'   # viet : group Led 2 
# ACCESS_TOKEN3 = 'FlJRrrrrFFZs06ZVOdzr'   # Update infor

z1baudrate = 38400
z1port = '/dev/pts/4'

Group_Led_1 = "Group-Led-1"
Group_Led_2 = "Group-Led-2"
sensorTypeValue = "default"
serialNumber = "serialNumber"
sensorTypeKey = "sensorType"

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

# >>>>>>>>>>>>>>>>>>>>>>>>>>>> UART

def config_uart() :
    serial_connection = serial.Serial(port=z1port,
                                    baudrate = z1baudrate,
                                    bytesize=serial.EIGHTBITS,
                                    parity=serial.PARITY_NONE,
                                    stopbits=serial.STOPBITS_ONE,
                                    timeout=1)
    return serial_connection


def connect_broker() -> mqtt_client:
    client = mqtt_client.Client()  
    client.connect('127.0.0.1', 1884)
    return client

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

def publishTelemetryStatePin_to_broker(z: str, y: dict, responce, payload_responce) : 
    try: 
        print('E')
        y = convert_boolean(z)
        client = mqtt_client.Client()  
        client.connect('127.0.0.1', 1884)
        print('D')
        payload = default_messase_Group1()
        payload = add_json("enabled" + str(y["params"]["pin"]), y["params"]["enabled"], payload)
        payload = check_state(payload, "true")                    #return JSON
        
        print('payload ' + payload)
        
        #client.publish(TELEMETRY, payload)
        print(responce + ' >> ' + payload_responce)
        #client.publish(responce, payload_responce)
  
        # if y["params"]["pin"] == 1 : 
        #     payload = default_messase_Group1()
        #     payload = add_json("enabled" + str(y["params"]["pin"]), y["params"]["enabled"], payload)
        #     payload = check_state(payload, "true")                    #return JSON
            
        #     print('payload ' + payload)
            
        #     client.publish(TELEMETRY, payload)
        #     del client
        # elif y["params"]["pin"] == 2 : 
        #     payload = default_messase_Group2()
        #     payload = add_json("enabled" + str(y["params"]["pin"]), y["params"]["enabled"], payload)
        #     payload = check_state(payload, "true")                    #return JSON
        #     print('payload ' + payload)
        
        #     client.publish(TELEMETRY, payload)
        #     del client
        # else :
        #     payload = init_responce()
        #     payload = add_json("100", "true", payload)
        #     print('Default')
        #     client.publish(TELEMETRY, payload)
        #     del client
    except:
        client = connect_broker()
        payload = init_responce()
        payload = add_json("100", "true", payload)
        print('Default')
        client.publish(TELEMETRY, payload)
        del client

def run_uart(client) :
    z1serial = config_uart()

    if z1serial.is_open:
        while True:
            size = z1serial.inWaiting()
            if size:
                try:
                    data_uart = z1serial.readline(size)
                    data_uart = data_uart.decode()
                    data_uart_dic = json.loads(data_uart)
                    print("data:" + data_uart)
                    
                    if data_uart.count('ID') != 0 and "TY" in data_uart and "ON" in data_uart and "DI" in data_uart and "TI" in data_uart and "SE" in data_uart :
                        payload = pushUpdateConfigureToThingsboard(data_uart_dic["TY"], data_uart_dic["ID"] , data_uart_dic["ON"], data_uart_dic["DI"], data_uart_dic["TI"], data_uart_dic["SE"])
                        if data_uart_dic["ID"] == 0: 
                            print('Data uart ' + payload)
                            client[0].publish(TELEMETRY, payload)

                        elif data_uart_dic["ID"] == 1 :                  
                            print('Data uart ' + payload)
                            client[1].publish(TELEMETRY, payload)

                        elif data_uart_dic["ID"] == 2 :
                            print('Data uart ' + payload)
                            client[2].publish(TELEMETRY, payload)  

                    else :
                        print("Data Received Through UART Not Valid")              
                except:
                    print("Data Received Through UART Not Valid except")  

            else :
                time.sleep(1)
                
    else:
        print ('z1serial not open')



# >>>>>>>>>>>>>>>>>>>>>>>>>>>> JSON

def convert_boolean(json_string) : 
    python_object = json.loads(json_string)
    python_object['params']['enabled'] = str(python_object['params']['enabled']).lower()
    return python_object

def default_notValid(client: mqtt_client, responce) :
    payload = init_responce()
    payload = add_json("Key", "Json", payload)
    payload = add_json("Valid", "Not", payload)
    print('Default')
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
            # y = convert_boolean(z)     
            serial_uart = config_uart()
            payload = init_responce()
            print('A')
            payload_responce = add_json(y["params"]["pin"], y["params"]["enabled"], payload)
            print('B '+ payload)
            
            publishTelemetryStatePin_to_broker(z, y, responce, payload_responce)
            print('C')
            # client = connect_mqtt(ACCESS_TOKEN1)
            #client.publish(responce, payload)
            
            # y  = convert_boolean(z)  
            # payload_uart = init_responce()
            # payload_uart = add_json("ID", y["params"]["pin"], payload_uart)
            # payload_uart = add_json("TY", 1, payload_uart)
            # if str(y["params"]["enabled"]) == "true" :
            #     payload_uart = add_json("ON", 1, payload_uart)
            #     print('payload_uart control led: ' + payload_uart)
            #     payload_uart = payload_uart.encode("utf8")
            #     serial_uart.write(payload_uart)
            # else :
            #     payload_uart = add_json("ON", 0, payload_uart)
            #     print('payload_uart control led: ' + payload_uart)
            #     payload_uart = payload_uart.encode("utf8")
            #     serial_uart.write(payload_uart)                

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

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> MQTT


def connect_mqtt(TOKEN: str) -> mqtt_client:
    client = mqtt_client.Client()  
    client.username_pw_set(TOKEN)
    client.connect(broker, port, keepalive=60)
    return client

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
        
    print("CALLBACK>>>>>>>>>>>>>>>>>>>>>>>>")
    payload = init_responce()
    payload = add_json(1002, "false", payload)
    payload = add_json(2002, "false", payload)
    client.on_message = on_message
    client.subscribe(topic)

    # client.publish(TELEMETRY, payload)
    # client.publish(ATTRIBUTE, payload)
    
def run(client: mqtt_client) :
    client.loop_forever()


if __name__ == '__main__':


    client = connect_mqtt(ACCESS_TOKEN1)
    #client1 = connect_mqtt(ACCESS_TOKEN2)
    client2 = connect_mqtt(ACCESS_TOKEN3)
   
    subscribe(client)
    #subscribe(client1)
    subscribe(client2)

    uart_client = [client, client2]

    t1 = threading.Thread(target=run, args=(client,))
    #t2 = threading.Thread(target=run, args=(client1,))
    t3 = threading.Thread(target=run, args=(client2,))
    t4 = threading.Thread(target=run_uart, args=(uart_client,))

    t1.start()
    #t2.start()
    t3.start()
    t4.start()


