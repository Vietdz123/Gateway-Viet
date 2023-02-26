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

class Wrapper :
    # Sự khác nhau của bản tin gửi xuống Device và bản tin gui lên Thingsboard là: bản tin gửi lên Thingsboard thì cần thêm 2 trường là tên của Thiết bị và kiểu thiết bị 
    # Các function nào có parameter là nameGroup thì 99% bản tin đó sẽ được gửi lên Thingssboard

    # nhận bản tin từ Device, sau đó đóng gói bản tin gồm các parameters , bản tin sau đó được gửi lên Thingsboard Cloud
    def pushUpdateConfigureToThingsboard(self, ID, ON, DI, TI, SE, nameGroup) :
        print("Function")

    # đóng gói bản tin gồm các parameters, bản tin sau đó gửi xuống Device
    def pushUpdateConfigureToDevice(self, TY, ID, ON, DI, TI, SE) :
        print("Function")

    # nhận bản tin RPC từ Thingsboard, sau đó đóng gói thành bản tin gồm các parameters, bản tin sau đó được gửi len Thingsboard
    def respondUpdateConfigureToDevice(self, TY, ID, ON, DI, TI, SE, nameGroup) :
        print("Function")
        
    # nhận bản tin RPC từ Thingsboard, sau đó đóng gói thành bản tin gồm các parameters, bản tin sau đó được gửi len Thingsboard
    def respondUpdateInformationToDevice(self, TY, ID, EX, nameGroup) : 
        print("Function")

    # nhận bản tin RPC từ Thingsboard, sau đó đóng gói thành bản tin gồm các parameters, bản tin sau đó được gửi xuong Device
    def pushUpdateInformationToDevice(self, TY, ID, EX) :
        print("Function")

    # Function này sẽ check ON là 0 hay 1, nếu là 0 thì sẽ đính trường "STATE": "OFF" vao payload và ngược lại
    def check_state(self, payload: str, isTrue: any) : 
        print("Function")

    # check bản tin có phải bản tin Json hay ko
    def is_json(self, message) :
        print("Function")

    # check xem bản tin có phải kieu định dạng mong muốn hay ko, VD: TY phải là int, DIM có thể là float hoặc Int  
    def checkValidMessage(self, TY = 0, ON = 1, DI = 50.5, TI = 15, SE = 100) : 
        print("Function")

    # check xem giá trị của các parameter có hợp lệ hay ko, VD ID phải > 0, DI phải < 100 và > 0
    def checkTypeMessage(self, ID = 0, TY = 5, ON = 1, DI = 30.8, TI = 10, EX = "0x12", SE = 20) :     
        print("Function")

    # Lưu ID vào hệ thống, check ID xem đã tồn tại hay chưa, bla bla
    def saveID(self, nameGroup: str, ID: int) :    
        print("Function")

    # Từ ID nhận được sẽ chuyển có được tên GroupLed, tên GroupLed được sửa dụng để đính kèm vào bản tin để gửi lên Thingsboard (Nói bên trên rồi đấy)
    def convertIDtoGroupLed(self, ID) : 
        print("Function")
        
    # Từ tên thiết bị truyền được, ta sẽ lấy được ID tương ứng của thiết bị ấy, cái này được sử dụng ở chỗ m dùng cái gpio chẳng hạn, bản tin gửi xuống ko có ID, chỉ có trường enabled
    def convertGroupToID(self, nameGroup) : 
        print("Function")

    # Init 1 bản tin rỗng để response 
    def init_responce(self) :
        print("Function")

    #  Add bản tin có key, value vào trong responce  
    def add_json(self, key , value, responce: str):
        print("Function")

    # Init bản tin chứa tên thiết bị 
    def initGroup(self, nameGroup) :
        print("Function")

    # Bản tin nhận được là True, t sẽ convert là true, vì cái gpio nó nhận true sẽ kéo cần ra, True thì ko kéo
    def convert_boolean(self, json_string) : 
        print("Function")

    # Khởi tạo Serial để truyền nhận bản tin 
    def config_uart(self) :
        print("Function")

    #  Function này có nhiệm vụ nhận, gửi bản tin tới thiết bị thông qua UART, chạy 1 thread khác
    def run_uart(self) :
        print("Function")
        
    # Xử lý mọi bản tin từ RPC từ Thingsboard gửi xuống, sau đó response và gửi xuống device
    def respond_message(self, z: str, y: dict, nameGroup: str, responce: str, client: mqtt_client):
        print("Function")

    # Connect to broker    
    def connect_mqtt(self) :
        print("Function")
        
    # Khởi tạo bản tin chứa tên thiết bị ở Cloud và kiểu của thiết bị, hinh nhu cai nay t ko dung nua
    def default_messase_Group1(self, nameGroup) : 
        print("Function")
    def default_messase_Group2(self) : 
        print("Function")

    # Khởi tạo một bản tin kết nối tới Group1 va 2 để truyền và nhận rpc  
    def connect_group2(self) :
        print("Function")
    def connect_group1(self) :
        print("Function")
    # Subcribe topic RPC    

    def subscribe(self):
        print("Function")

    # Nếu trong 1p or hơn mà ko gửi và nhận RPC nữa thì Gateway sẽ ngắt kết nối nhận RPC nữa, nên Function này để giữ kết nối RPC, cái này được chạy ở 1 thread khác
    def keepConnectThingsboard(self) :
        print("Function")

    # Thi Run, chay o Thread Main :)))    
    def run(self) :
        print("Function")
        
    # Thực thi nhiều Thread cùng lúc    
    def excuteMultipleThread(self) :
        print("Function")

#Newest
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
    params = "params"

    Group_Led = ["Group-Led-1", "Group-Led-2"]
    ID_Led = [200, 100]

    sensorTypeValue = "default"
    serialNumber = "serialNumber"
    sensorTypeKey = "sensorType"

    z1baudrate = 38400
    z1port = '/dev/pts/6'

    client: mqtt_client

    #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Convert Data
    def pushUpdateConfigureToThingsboard(self, ID, ON, DI,  TI, SE, nameGroup) :
        payload = self.initGroup(nameGroup)
        if ID != None:
            payload = self.add_json('ID', ID, payload)
        if ON != None:
            payload = self.add_json('ON', ON, payload)
        if DI != None:
            payload = self.add_json('DI', DI, payload)
        if TI != None:
            payload = self.add_json('TI', TI, payload)
        if SE != None:
            payload = self.add_json('SE', SE, payload)         
        return payload 

    def pushUpdateConfigureToDevice(self, TY, ID, ON, DI, TI, SE) :
        payload = self.init_responce()
        if ID != None:
            payload = self.add_json('ID', ID, payload)
        if ON != None:
            payload = self.add_json('ON', ON, payload)
        if DI != None:
            payload = self.add_json('DI', DI, payload)
        if TI != None:
            payload = self.add_json('TI', TI, payload)
        if TY != None:
            payload = self.add_json('TY', TY, payload)
        if SE != None:
            payload = self.add_json('SE', SE, payload)            
        payload = payload.replace(" ", "")
        return payload 

    def respondUpdateConfigureToDevice(self, TY, ID, ON, DI, TI, SE, nameGroup) :
        payload = self.initGroup(nameGroup)
        if ID != None:
            payload = self.add_json('ID', ID, payload)
        if ON != None:
            payload = self.add_json('ON', ON, payload)
        if DI != None:
            payload = self.add_json('DI', DI, payload)
        if TI != None:
            payload = self.add_json('TI', TI, payload)
        if TY != None:
            payload = self.add_json('TY', TY, payload)
        if SE != None:
            payload = self.add_json('SE', SE, payload)            
        return payload       

    def respondUpdateInformationToDevice(self, TY, ID, EX, nameGroup) :
        payload = self.initGroup(nameGroup)
        if ID != None:
            payload = self.add_json('ID', ID, payload)
        if TY != None:
            payload = self.add_json('TY', TY, payload)
        if EX != None:
            payload = self.add_json('EX', EX, payload)
        return payload

    def pushUpdateInformationToDevice(self, TY, ID, EX) :
        payload = self.init_responce()
        if ID != None:
            payload = self.add_json('ID', ID, payload)
        if TY != None:
            payload = self.add_json('TY', TY, payload)
        if EX != None:
            payload = self.add_json('EX', str(EX), payload)
        payload = payload.replace(" ", "")
        print(payload)
        return payload    

    #>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Responce Not Valid Message
    def defaultJsonnotValid(self, responce, nameGroup, client: mqtt_client) :
        payload = self.initGroup(nameGroup)
        payload = self.add_json(self.serialNumber, nameGroup, payload)
        payload = self.add_json(self.sensorTypeKey, self.sensorTypeValue, payload)
        payload = self.add_json("Key", "Json", payload)
        payload = self.add_json("Valid", "Not", payload)

        client.publish(responce, payload) 

    def respondMessageNotValid(self, responce, nameGroup, message,client: mqtt_client) :
        payload = self.initGroup(nameGroup)
        payload = self.add_json(self.serialNumber, nameGroup, payload)
        payload = self.add_json(self.sensorTypeKey, self.sensorTypeValue, payload)
        payload = json.loads(payload)
        payload.update(message)
        payload = json.dumps(payload)

        client.publish(responce, payload) 

    #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Check Valid Format Message
    def check_state(self, payload: str, isTrue: any) : 
        if isTrue != None: 
            if isTrue == "True" or isTrue == 1:
                fullstring = self.add_json("STATE", "ON", payload)
                return fullstring
            else:
                fullstring = self.add_json("STATE", "OFF", payload)
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

    def checkTypeMessage(self, ID = 0, TY = 5, ON = 1, DI = 30.8, TI = 10, EX = "0x12", SE = 20) : 
        if EX != None:
            EX = int(EX, 16)
            EX = hex(EX)                 
        if ID != None:    
            if isinstance(ID, int) != True  :
                return None
        if TY != None: 
            if isinstance(TY, int) != True :
                return None
        if ON != None: 
            if isinstance(ON, int) != True :
                return None
        if DI != None: 
            if isinstance(DI, (int, float)) != True :
                return None
        if TI != None: 
            if isinstance(TI, int) != True :
                return None 
        if SE != None: 
            if isinstance(TI, int) != True :
                return None             
        return True               

    def checkValidMessage(self, TY = 0, ON = 1, DI = 50.5, TI = 15, SE = 100) : 
        if TY != None:
            if TY != 0 and TY != 1 :
                return None
        if ON != None:
            if ON != 0 and ON != 1 :
                return None
        if DI != None:
            if DI < 0 or DI > 100:
                return None
        if TI != None:
            if TI < 1 :
                return None
        if SE != None: 
            if SE < 0:
                return None
        return True
        
    #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Save Id, Convert ID To NameGroup, Convert NameGroup To ID
    def saveID(self, nameGroup: str, ID: int) :
        for i in range(len(self.Group_Led)):
            if self.Group_Led[i] == nameGroup :
                for k in range(len(self.Group_Led)) : 
                    if k != i and self.ID_Led[k] == ID :    
                        print("Cannot Save...Exist ID")
                        return None
                print("Save success")
                self.ID_Led[i] = ID
                return True

    def convertIDtoGroupLed(self, ID) :
        for i in range(len(self.ID_Led)):
            if self.ID_Led[i] == ID:
                return self.Group_Led[i]  
        print("ID not Exist")    
    
    def convertGroupToID(self, nameGroup) : 
        for i in range(len(self.Group_Led)):
            if self.Group_Led[i] == nameGroup:
                return self.ID_Led[i]      

    #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Helpers
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

    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> UART
    def config_uart(self) :
        serial_connection = serial.Serial(port=self.z1port,
                                        baudrate = self.z1baudrate,
                                        bytesize=serial.EIGHTBITS,
                                        parity=serial.PARITY_NONE,
                                        stopbits=serial.STOPBITS_ONE,
                                        timeout=None)
        return serial_connection

    def run_uart(self) :
        z1serial = self.config_uart()
        
        if z1serial.is_open:
            while True:
                # size = z1serial.inWaiting()
                # if size:
                try:
                    data_uart = z1serial.readline()
                    data_uart = data_uart.decode()
                    print("Received data: " + data_uart + "\n")
                    data_uart_dic = json.loads(data_uart)
                    
                    ID = data_uart_dic.get("ID")
                    ON = data_uart_dic.get("ON")
                    DI = data_uart_dic.get("DI")
                    TI = data_uart_dic.get("TI")
                    SE = data_uart_dic.get("SE")

                    if data_uart.count('ID') != 0:
                        nameGroup = self.convertIDtoGroupLed(ID)
                        payload = self.pushUpdateConfigureToThingsboard(ID, ON, DI, TI, SE, nameGroup)
                        payload = self.check_state(payload = payload, isTrue = ON)
                        print(payload)
                        self.client.publish(self.TELEMETRY, payload)

                    else :
                        print("Data Received Through UART Not Valid")              
                except:
                    print("Data Received Through UART Not Valid except")  

                # else :
                #     time.sleep(0.5)
                    
        else:
            print ('z1serial not open')


    #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Handle Responce RPC To Thingsboard and Send Configure to Device
    def respond_message(self, z: str, y: dict, nameGroup: str, responce: str, client: mqtt_client):
        try: 
            if z.count(self.inf) != 0 and "ID" in z and "EX" in z:
                TY = y.get(self.params).get("TY")
                ID = y.get(self.params).get("ID")
                EX = y.get(self.params).get("EX")

                check = self.checkTypeMessage(ID = ID, TY = TY, EX = EX)
                if check == None :
                    self.defaultJsonnotValid(responce, nameGroup, client)
                    return
                check = self.checkValidMessage(TY = TY)
                if check == None :
                    self.defaultJsonnotValid(responce, nameGroup, client)
                    return

                check = self.saveID(nameGroup, ID)
                if check == None :
                    self.defaultJsonnotValid(responce, nameGroup, client) 
                    return  

                serial_uart = self.config_uart()
                payload = self.respondUpdateInformationToDevice(TY, ID, EX, nameGroup)

                client.publish(responce, payload)
                print('Set information: ' + payload)

                payload = self.pushUpdateInformationToDevice(TY, ID, EX)
                payload = payload.encode("utf-8")
                serial_uart.write(payload)
                for element in self.ID_Led :
                    print("ID after save " + str(element))

            #Dieu khien cac thong so cho Led
            elif z.count(self.conf) != 0 and "ID" in z:       
                TY = y.get(self.params).get("TY")
                ID = y.get(self.params).get("ID")
                ON = y.get(self.params).get("ON")
                DI = y.get(self.params).get("DI")
                TI = y.get(self.params).get("TI")
                SE = y.get(self.params).get("SE")

                check = self.checkTypeMessage(ID, TY, ON, DI, TI, SE=SE)
                if check == None :
                    self.defaultJsonnotValid(responce, nameGroup, client)
                    return
                check = self.checkValidMessage(TY = TY, ON = ON, DI = DI, TI = TI, SE = SE)
                if check == None :
                    self.defaultJsonnotValid(responce, nameGroup, client)
                    return
                check = self.saveID(nameGroup, ID)
                if check == None :
                    self.defaultJsonnotValid(responce, nameGroup, client)
                    return  

                serial_uart = self.config_uart()
                payload = self.respondUpdateConfigureToDevice(TY, ID, ON, DI, TI, SE, nameGroup)
                payload = self.check_state(payload, ON)
                self.client.publish(self.TELEMETRY, payload)
                print('Set configuration: ' + payload)

                payload = self.pushUpdateConfigureToDevice(TY, ID, ON, DI, TI, SE)
                payload = payload.encode("utf8")
                serial_uart.write(payload)
                for element in self.ID_Led :
                    print("ID after save " + str(element))
                
            #Dieu khien tat bat led
            elif z.count(self.pin) != 0 and "enabled" in z :           
                serial_uart = self.config_uart()
                
                payload = self.initGroup(nameGroup)
                ID = self.convertGroupToID(nameGroup)

                payload = self.add_json(y["pin"], y["enabled"], payload)
                temp = self.convert_boolean(z)                   #convert true to "true"
                payload = self.add_json("enabled" + str(temp["pin"]), temp["enabled"], payload)
                payload = self.check_state(payload, str(y["enabled"]))  
                print(payload)
                client.publish(responce, payload)

                y  = self.convert_boolean(z)  
                payload_uart = self.init_responce()
                ID = self.convertGroupToID(nameGroup)
                payload_uart = self.add_json('ID', ID, payload_uart)
                payload_uart = self.add_json("TY", 1, payload_uart)

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
                            
            else :
                self.defaultJsonnotValid(responce, nameGroup,client)
        
        except:
            self.defaultJsonnotValid(responce, nameGroup,client)     


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
            rpcMessage = msg.payload.decode()
            rpcMessage = rpcMessage.replace("\\", "")

            if rpcMessage.startswith('"') and rpcMessage.endswith('"'):
                rpcMessage = rpcMessage[1:-1]
                
            print(rpcMessage + '\n')

            # print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic") 
            isJson = self.is_json(rpcMessage)
            repsonTopic = str(msg.topic)
            responce =  repsonTopic.replace("request", "response")
            elementNameTopics = responce.split("/")
            if isJson == True :   
                y = json.loads(rpcMessage)                         #convert sang json  
                z = json.dumps(y)                                            #convert to string                       

                self.respond_message(z, y, elementNameTopics[2],responce, client)
            else :
                self.defaultJsonnotValid(responce, elementNameTopics[2], client)

        self.client.on_message = on_message
        self.client.subscribe(self.topic)
        self.client.publish(self.topic_connect, self.connect_group1())
        self.client.publish(self.topic_connect, self.connect_group2())
        self.client.publish(self.TELEMETRY, '{"serialNumber": "Group-Led-1", "sensorType": "default", "trash": "5"}')
        self.client.publish(self.TELEMETRY, '{"serialNumber": "Group-Led-2", "sensorType": "default", "trash": "5"}')

    def keepConnectThingsboard(self) :
        while True :
            time.sleep(20)
            self.client.publish(self.topic_connect, self.connect_group1())
            self.client.publish(self.topic_connect, self.connect_group2())
            self.client.publish(self.TELEMETRY, '{"serialNumber": "Group-Led-1", "sensorType": "default", "trash": "6"}')
            self.client.publish(self.TELEMETRY, '{"serialNumber": "Group-Led-2", "sensorType": "default", "trash": "5"}')
        


    def excuteMultipleThread(self) :
        self.thread1 = threading.Thread(target=self.run, args=())
        self.thread2 = threading.Thread(target=self.run_uart, args=())
        self.thread3 = threading.Thread(target=self.keepConnectThingsboard, args=())
        self.thread1.start()
        self.thread2.start()
        self.thread3.start()


#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Main
if __name__ == '__main__':
    thingboardGateway = ThingsboardGateway()
    thingboardGateway.connect_mqtt()
    thingboardGateway.subscribe()
    thingboardGateway.excuteMultipleThread()
    
