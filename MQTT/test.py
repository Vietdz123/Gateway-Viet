
import paho.mqtt.client as mqtt

# Create the first client
client1 = mqtt.Client()

# Connect the first client to the first Kafka broker
client1.connect("localhost", 9092)

# Create the second client
client2 = mqtt.Client()

# Connect the second client to the second Kafka broker
client2.connect("localhost", 9093)

# Set the on_message callback for the first client
def on_message(client, userdata, message):
  # Print the received message
  print(f"Received message: {message.payload}")

client1.on_message = on_message

# Subscribe the first client to the "test" topic
client1.subscribe("test")

# Publish a message to the "test" topic using the second client
client2.publish("test", "Hello, world!")

# Run the first client's event loop to process the received message
client1.loop_forever()