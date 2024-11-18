import process_order as PO
import paho.mqtt.client as mqtt


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
    else:
        print(f"Failed to connect, return code {rc}")


client = mqtt.Client()
client.on_message = on_connect
client.connect("127.0.0.1", 1883, 60)   # Connect to localhost MQTT broker

topic = "myStore/order/size" 
message = PO.Size

print(f"Publishing to topic '{topic}': {message}")
client.publish("myStore/orders", message)  # Publish the message