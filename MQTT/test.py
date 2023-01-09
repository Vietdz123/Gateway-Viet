import json
from paho.mqtt import client as mqtt_client
import paho.mqtt.client as mqtt
import paho.mqtt.client as paho  		    #mqtt library

import json
import time
from datetime import datetime
from threading import Thread
import threading
import re

message = '{"method":"ControlLed","params":{"pin":2,"enabled": false}}'
message = json.loads(message)
message = json.dumps(message)
print(message)