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

message = {"method":"dim0","DI":43.33}

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

#data_uart = {"TY":2, "ID": 1, "ON":"0", "DI":30, "TI":10, "SE":100}
z1baudrate = 38400
#z1port = '/dev/pts/5'  # set the correct port before run it
z1port = '/dev/pts/4'

# >>>>>>>>>>>>>>>>>>>>>>>>>>>> UART

def config_uart() :
    serial_connection = serial.Serial(port=z1port,
                                    baudrate = z1baudrate,
                                    bytesize=serial.EIGHTBITS,
                                    parity=serial.PARITY_NONE,
                                    stopbits=serial.STOPBITS_ONE,
                                    timeout=1)
    return serial_connection


def connect_uart() -> mqtt_client:
    uart = mqtt_client.Client()  
    uart.connect('127.0.0.1', 1884)
    return uart

def pushUpdateConfigureToThingsboard(TY, ON, DI,  TI, SE) :
    payload = init_responce()
    payload = add_json('TY', str(TY), payload)
    payload = add_json('ON', str(ON), payload)
    payload = add_json('DI', str(DI), payload)
    payload = add_json('TI', str(TI), payload)
    payload = add_json('SE', str(SE), payload)
    return payload    


def convertData(data_uart: str) :
    print ('Data received through uart: ' + data_uart)
    result = re.findall(r"\b\w+:\s*\d+\b", data_uart)

    for item in result:
        key, value = item.split(':')
        value = int(value)
        if key == 'TY':
            TY = value
        elif key == 'ID':
            ID = value
        elif key == 'ON':
            ON = value
        elif key == 'DI':
            DI = value
        elif key == 'TI':
            TI = value                        
        elif key == 'SE':
            SE = value
    
    if 'TY' in locals() and 'ID' in locals() and 'ON' in locals() and 'DI' in locals() and 'TI' in locals() and 'SE' in locals() :
        print('exist')
        payload = pushUpdateConfigureToThingsboard(TY, ON, DI, TI, SE)
        return ID, payload
    else: 
        ID = -102
        payload = init_responce()
        return ID, payload


def run_uart(client) :
    z1serial = config_uart()

    print ('Serial Opened')  # True for opened
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
                        payload = pushUpdateConfigureToThingsboard(data_uart_dic["TY"], data_uart_dic["ON"], data_uart_dic["DI"], data_uart_dic["TI"], data_uart_dic["SE"])
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
                #print("No Data")
                
    else:
        print ('z1serial not open')



# >>>>>>>>>>>>>>>>>>>>>>>>>>>> JSON

def default_notValid(client: mqtt_client, responce) :
    payload = init_responce()
    payload = add_json("Key", "Json", payload)
    payload = add_json("Valid", "Not", payload)

    client.publish(ATTRIBUTE, payload)
    client.publish(responce, payload)   

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

def is_json(message) :
    
    try:
        data = json.loads(message)
        if isinstance(data, dict):
            a = json.dumps(data)
            print(a)
            kq = a.count("{") - a.count("}") 
            if kq != 0 or a.count("\\") != 0 :
                return None
            return True
        else:
            return  None
    except json.JSONDecodeError:
            print("The message is not a valid JSON")
            return None

def is_json2(string):
  pattern = r'^\s*\{.*\}\s*$'
  return re.match(pattern, string) is not None

def respond_message(z: str, y: dict, responce: str, client: mqtt_client):
    try: 
        if "TY" in z and "EX" in z and "ID" in z :
            serial_uart = config_uart()
            payload = y["params"]
            str_payload = json.dumps(payload)

            client.publish(TELEMETRY, str_payload)
            client.publish(responce, str_payload)

            print('Set information: ' + str_payload)
            str_payload = str_payload.encode("utf-8")

            serial_uart.write(str_payload)
            
            
        elif z.count(conf) != 0 and "TY" in z and "ID" in y and "ON" in y and "DI" in y and "TI" in y:    
            serial_uart = config_uart()
            payload = y["params"]
            str_payload = json.dumps(payload)

            client.publish(TELEMETRY, str_payload)
            client.publish(responce, str_payload)

            print('Set configuration: ' + str_payload + ' from ' + responce)
            str_payload = str_payload.encode("utf8")
            serial_uart.write(str_payload)
            

        elif z.count(pin) != 0 and "enabled" in z : #and "Group" in z:           
            serial_uart = config_uart()
            payload = init_responce()

            payload = add_json(y["params"]["pin"], y["params"]["enabled"], payload)
            payload_telemetry = check_state(payload, "true")                    #return JSON
            print('Control Pin: ' + payload_telemetry)
            print('payload ' + payload)
            client.publish(ATTRIBUTE, payload)
            client.publish(TELEMETRY, payload_telemetry)
            client.publish(responce, payload)

            payload_uart = init_responce()
            payload_uart = add_json("ID", y["params"]["pin"], payload_uart)
            payload_uart = add_json("TY", 1, payload_uart)
            payload_uart = add_json("ON", y["params"]["enabled"],payload_uart)
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
            client.publish(ATTRIBUTE, payload_uart)

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
            client.publish(ATTRIBUTE, payload_uart)

            payload = payload_uart.encode("utf-8")
            serial_uart.write(payload) 
            
             
        else :
            print('CAC')
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

        if isJson == True :   
            y = json.loads(msg.payload.decode())                         #convert sang json  
            z = json.dumps(y)                                            #convert to string                       
            responce =  repsonTopic.replace("request", "response")
            respond_message(z, y, responce, client)
        else :
            print("else")
            responce =  repsonTopic.replace("request", "response")
            default_notValid(client, responce)
        
    print("CALLBACK>>>>>>>>>>>>>>>>>>>>>>>>")
    payload = init_responce()
    payload = add_json(1, "false", payload)
    payload = add_json(2, "false", payload)
    client.on_message = on_message
    client.subscribe(topic)

    client.publish(TELEMETRY, payload)
    client.publish(ATTRIBUTE, payload)
    
def run(client: mqtt_client) :
    client.loop_forever()

if __name__ == '__main__':
    client = connect_mqtt(ACCESS_TOKEN1)
    client1 = connect_mqtt(ACCESS_TOKEN2)
    client2 = connect_mqtt(ACCESS_TOKEN3)

    # client = connect_uart()
    # client1 = connect_uart()
    # client2 = connect_uart()
    
    subscribe(client)
    subscribe(client1)
    subscribe(client2)

    uart_client = [client, client1, client2]

    t1 = threading.Thread(target=run, args=(client,))
    t2 = threading.Thread(target=run, args=(client1,))
    t3 = threading.Thread(target=run, args=(client2,))
    t4 = threading.Thread(target=run_uart, args=(uart_client,))
    
    t1.start()
    t2.start()
    t3.start()
    t4.start()



