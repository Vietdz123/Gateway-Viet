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

class ThingsboardGateway :
    broker = "127.0.0.1"
    port = 1884

    TELEMETRY = "v1/devices/me/telemetry"
    ATTRIBUTE = "v1/devices/me/attributes"
    topic_connect = "sensor/connect"
    topic = 'v1/device/+/request/+/+'

    inf = 'inf'
    conf = 'conf'
    pin = 'pin'

    Group_Led = ["Group-Led-1", "Group-Led-2"]

    sensorTypeValue = "default"
    serialNumber = "serialNumber"
    sensorTypeKey = "sensorType"

    z1baudrate = 38400
    z1port = '/dev/pts/3'

    ID_Led = [0, 1]

    client: mqtt_client

    def pushUpdateConfigureToThingsboard(self, ID, ON, DI,  TI, SE, nameGroup) :
        print("pushUpdateConfigureToThingsboard")
        payload = self.initGroup(nameGroup)
        payload = self.add_json('ID', str(ID), payload)
        payload = self.add_json('ON', str(ON), payload)
        payload = self.add_json('DI', str(DI), payload)
        payload = self.add_json('TI', str(TI), payload)
        payload = self.add_json('SE', str(SE), payload)
        return payload 

    def pushUpdateConfigureToDevice(self, TY, ID , ON, DI,  TI, nameGroup) :
        print("pushUpdateConfigureToDevice")
        payload = self.initGroup(nameGroup)
        payload = self.add_json('TY', str(TY), payload)
        payload = self.add_json('ID', str(ID), payload)
        payload = self.add_json('ON', str(ON), payload)
        payload = self.add_json('DI', str(DI), payload)
        payload = self.add_json('TI', str(TI), payload)
        return payload      

    def pushUpdateInformationToDevice(self, TY, ID, EX, nameGroup) :
        payload = self.initGroup(nameGroup)
        payload = self.add_json('TY', str(TY), payload)
        payload = self.add_json('ID', str(ID), payload)
        payload = self.add_json('EX', str(EX), payload)
        print(payload)
        return payload  

    def default_notValid(self, responce, nameGroup, client: mqtt_client) :
        payload = self.init_responce()
        payload = self.add_json(self.serialNumber, nameGroup, payload)
        payload = self.add_json(self.sensorTypeKey, self.sensorTypeValue, payload)
        payload = self.add_json("Key", "Json", payload)
        payload = self.add_json("Valid", "Not", payload)

        client.publish(self.ATTRIBUTE, payload)
        client.publish(responce, payload)   

    def check_state(self, fullstring: str, substring: str) :  
        if fullstring.find(substring) != -1:
            fullstring = self.add_json("STATE", "ON", fullstring)
            return fullstring
        else:
            fullstring = self.add_json("STATE", "OFF", fullstring)
            return fullstring    

    def is_json(self, message) :
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

    def saveID(self, nameGroup: str, ID: int) :
        print(nameGroup)
        for i in range(len(self.Group_Led)):
            print(self.Group_Led[i])
            if self.Group_Led[i] == nameGroup :
                for k in range(len(self.Group_Led)) : 
                    if k != i and self.ID_Led[k] == ID :    
                        print("Exist ID")
                        return None
                print("Save success")
                self.ID_Led[i] = ID
                return True

    def convertIDtoGroupLed(self, ID) :
        for i in range(len(self.ID_Led)):
            if self.ID_Led[i] == ID:
                return self.Group_Led[i]      
    
    def convertGroupToID(self, nameGroup) : 
        for i in range(len(self.Group_Led)):
            if self.Group_Led[i] == nameGroup:
                return self.ID_Led[i]      

    def init_responce(self) :
        payload = "{}"
        return payload

    def add_json(self, key , value, responce: str):
        json_responce = json.loads(responce)
        json_responce[key] = value
        payload = json.dumps(json_responce)
        return payload

    def convert_boolean(self, json_string) : 
        python_object = json.loads(json_string)
        python_object['enabled'] = str(python_object['enabled']).lower()
        return python_object

    def checkTypeMessage(self, ID = 0, TY = 5, ON = 1, DI = 30.8, TI = 10, EX = "0x12") : 
        EX = int(EX, 16)
        EX = hex(EX)                 # Check is hex or not
        if isinstance(ID, int) and isinstance(TY, int) and isinstance(ON, int) and isinstance(DI, (float, int)) and isinstance(TI, int) :
            return True
        else :
            return None

    def checkValidMessage(self, TY = 0, ON = 1, DI = 50.5, TI = 15, SE = 100) : 
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
    def config_uart(self) :
        serial_connection = serial.Serial(port=self.z1port,
                                        baudrate = self.z1baudrate,
                                        bytesize=serial.EIGHTBITS,
                                        parity=serial.PARITY_NONE,
                                        stopbits=serial.STOPBITS_ONE,
                                        timeout=1)
        return serial_connection

    def run_uart(self) :
        print("UART")
        z1serial = self.config_uart()
        
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
                            nameGroup = self.convertIDtoGroupLed(data_uart_dic["ID"])
                            print("Name Group UART " )
                            payload = self.pushUpdateConfigureToThingsboard(data_uart_dic["ID"] , data_uart_dic["ON"], data_uart_dic["DI"], data_uart_dic["TI"], data_uart_dic["SE"], nameGroup)
                            
                            self.client.publish(self.TELEMETRY, payload)

                        else :
                            print("Data Received Through UART Not Valid")              
                    except:
                        print("Data Received Through UART Not Valid except")  

                else :
                    time.sleep(1)
                    
        else:
            print ('z1serial not open')


    #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Hanlde Responce RPC To Thingsboard and Send Configure to Device
    def respond_message(self, z: str, y: dict, nameGroup: str, responce: str, client: mqtt_client):
        try: 
            if z.count(self.inf) != 0 and "TY" in z and "EX" in z and "ID" in z :
                check = self.checkTypeMessage(ID = y["params"]["ID"], TY = y["params"]["TY"], EX = y["params"]["EX"])
                if check == None :
                    self.default_notValid(responce, nameGroup,client)
                    return
                check = self.checkValidMessage(TY = y["params"]["TY"])
                if check == None :
                    self.default_notValid(responce, nameGroup, client)
                    return

                check = self.saveID(nameGroup, y["params"]["ID"])
                if check == None :
                    print("None")
                    self.default_notValid(responce, nameGroup,client) 
                    return  

                serial_uart = self.config_uart()
                payload = self.pushUpdateInformationToDevice(y["params"]["TY"], y["params"]["ID"], y["params"]["EX"], nameGroup)

                client.publish(self.TELEMETRY, payload)
                client.publish(responce, payload)

                print('Set information: ' + payload)

                payload = "{}"
                payload = self.add_json('TY', y["params"]["TY"], payload)
                payload = self.add_json('ID', y["params"]["ID"], payload)
                payload = self.add_json('EX', str(y["params"]["EX"]), payload)

                payload.replace(" ", "")
                print(payload)
                payload = payload.encode("utf-8")
                serial_uart.write(payload)
                for element in self.ID_Led :
                    print(element)


                
            #Dieu khien cac thong so cho Led
            elif z.count(self.conf) != 0 and "TY" in z and "ID" in z and "ON" in z and "DI" in z and "TI" in z: 
                TY = y["params"]["TY"]
                ID = y["params"]["ID"]
                ON = y["params"]["ON"]
                DI = y["params"]["DI"]
                TI = y["params"]["TI"]

                check = self.saveID(nameGroup, ID)
                if check == None :
                    self.default_notValid(responce, nameGroup, client)
                    return  

                check = self.checkTypeMessage(ID, TY, ON, DI, TI)
                if check == None :
                    self.default_notValid(responce, nameGroup, client)
                    return
                check = self.checkValidMessage(TY = TY, ON = ON, DI = DI, TI = TI)
                if check == None :
                    self.default_notValid(responce, nameGroup,client)
                    return

                serial_uart = self.config_uart()
                payload = self.pushUpdateConfigureToDevice(TY, ID, ON, DI, TI, nameGroup)
                
                self.client.publish(self.TELEMETRY, payload)
                self.client.publish(responce, payload)
                print('Set configuration: ' + payload)

                payload = "{}"
                payload = self.add_json('TY', y["params"]["TY"], payload)
                payload = self.add_json('ID', y["params"]["ID"], payload)
                payload = self.add_json('ON', y["params"]["ON"], payload)
                payload = self.add_json('DI', y["params"]["DI"], payload)
                payload = self.add_json('TI', y["params"]["TI"], payload)
                payload.replace(" ", "")
                print(payload)

                payload = payload.encode("utf8")
                serial_uart.write(payload)
                for element in self.ID_Led :
                    print(element)

                
            #Dieu khien tat bat led
            elif z.count(self.pin) != 0 and "enabled" in z :           
                serial_uart = self.config_uart()
                
                payload = self.initGroup(nameGroup)
                ID = self.convertGroupToID(nameGroup)

                payload = self.add_json(y["pin"], y["enabled"], payload)
                temp = self.convert_boolean(z)                   #convert true to "true"
                payload = self.add_json("enabled" + str(temp["pin"]), temp["enabled"], payload)
                payload = self.check_state(payload, "true")  
                print(payload)
                client.publish(responce, payload)
                client.publish(self.TELEMETRY, payload)

                y  = self.convert_boolean(z)  
                payload_uart = self.init_responce()
                ID = self.convertGroupToID(nameGroup)
                payload_uart = self.add_json('ID', ID, payload_uart)

                if str(y["enabled"]) == "true" :
                    payload_uart = self.add_json("ON", 1, payload_uart)
                    print('payload_uart control led: ' + payload_uart)
                    payload_uart = payload_uart.encode("utf8")
                    serial_uart.write(payload_uart)
                else :
                    payload_uart = self.add_json("ON", 0, payload_uart)
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
                        serial_uart = self.config_uart()
                        payload_responce_thingsboard = self.initGroup(nameGroup)
                        payload_responce_thingsboard = self.add_json("ID", numberDim, payload_responce_thingsboard)
                        payload_responce_thingsboard = self.add_json('DI', value_params, payload_responce_thingsboard)                    

                        client.publish(self.TELEMETRY, payload_responce_thingsboard)  
                        client.publish(responce, payload_responce_thingsboard)

                        payload_uart = self.init_responce()
                        payload_uart = self.add_json("ID", numberDim, payload_uart)
                        payload_uart = self.add_json('DI', value_params, payload_uart)
                        print('payload_uart control dim: ' + payload_uart)
                        payload = payload_uart.encode("utf-8")
                        serial_uart.write(payload) 
                    
                    else :
                        self.default_notValid(responce, nameGroup,client)
                
                except :
                    self.default_notValid(responce, nameGroup,client)
                            
            else :
                self.default_notValid(responce, nameGroup,client)
        
        except:
            self.default_notValid(responce, nameGroup,client)     


    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Connect Broker and Thingsboard
    def connect_group1(self) :
        payload = self.init_responce()
        payload = self.add_json("SerialNumber", self.Group_Led[0], payload)
        return payload

    def default_messase_Group1(self, nameGroup) : 
        payload = self.init_responce()
        payload = self.add_json(self.serialNumber, self.Group_Led[0], payload)
        payload = self.add_json(self.sensorTypeKey, self.sensorTypeValue, payload)
        return payload

    def connect_group2(self) :
        payload = self.init_responce()
        payload = self.add_json("SerialNumber", self.Group_Led[1], payload)
        return payload

    def default_messase_Group2(self) : 
        payload = self.init_responce()
        payload = self.add_json(self.serialNumber, self.Group_Led[1], payload)
        payload = self.add_json(self.sensorTypeKey, self.sensorTypeValue, payload)
        return payload
    
    def initGroup(self, nameGroup) :
        payload = self.init_responce()
        payload = self.add_json(self.serialNumber, nameGroup, payload)
        payload = self.add_json(self.sensorTypeKey, self.sensorTypeValue, payload)
        return payload

    def connect_mqtt(self) :
        self.client = mqtt_client.Client()  
        self.client_uart = mqtt_client.Client()  
        self.client.connect(self.broker, self.port)
        self.client_uart.connect(self.broker, self.port)

    def run(self) :
        self.client.loop_forever()

    def subscribe(self):
        def on_message(client, userdata, msg):
            print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic") 
            isJson = self.is_json(msg.payload.decode())
            repsonTopic = str(msg.topic)
            responce =  repsonTopic.replace("request", "response")
            elementNameTopics = responce.split("/")
            if isJson == True :   
                y = json.loads(msg.payload.decode())                         #convert sang json  
                z = json.dumps(y)                                            #convert to string                       
                
                self.respond_message(z, y, elementNameTopics[2],responce, client)
            else :
                self.default_notValid(client, responce, elementNameTopics[2])

        self.client.on_message = on_message
        self.client.subscribe(self.topic)
        self.client.publish(self.topic_connect, self.connect_group1())
        self.client.publish(self.topic_connect, self.connect_group2())
        self.client.publish(self.TELEMETRY, '{"serialNumber": "Group-Led-1", "sensorType": "default", "trash": "trash"}')
        self.client.publish(self.TELEMETRY, '{"serialNumber": "Group-Led-2", "sensorType": "default", "trash": "trash"}')

    def keepConnectThingsboard(self) :
        while True :
            time.sleep(10)
            self.client.publish(self.TELEMETRY, '{"serialNumber": "Group-Led-1", "sensorType": "default", "trash": "trash"}')
            self.client.publish(self.TELEMETRY, '{"serialNumber": "Group-Led-2, "sensorType": "default", "trash": "trash"}')
        
    def firstUartConnectToThingsboard(self) :
        self.client.publish(self.topic_connect, thingboardGateway.connect_group1())
        self.client.publish(self.TELEMETRY, '{"serialNumber": "Group-Led-1", "sensorType": "default", "trash": "trash"}')

    def excuteMultipleThread(self) :
        self.thread1 = threading.Thread(target=self.run, args=())
        self.thread2 = threading.Thread(target=self.run_uart, args=())
        self.thread3 = threading.Thread(target=self.keepConnectThingsboard, args=())
        self.thread1.start()
        self.thread2.start()
        self.thread3.start()


if __name__ == '__main__':
    thingboardGateway = ThingsboardGateway()
    thingboardGateway.connect_mqtt()
    thingboardGateway.subscribe()
    thingboardGateway.excuteMultipleThread()
    

