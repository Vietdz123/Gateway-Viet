import json
from paho.mqtt import client as mqtt_client

import paho.mqtt.client as paho  		    #mqtt library
import os
import json
import time
from datetime import datetime
from threading import Thread
import threading


import json

data = {'pin': 1, 'enabled': True}

# Convert the dictionary to a JSON string
json_string = json.dumps(data)

# Split the string into a list of substrings
pairs = json_string.split(", ")

# Print the key-value pairs
for pair in pairs:
    (key, value) = pair
    print(key + ' ' + value)
