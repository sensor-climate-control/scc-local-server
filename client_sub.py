import paho.mqtt.client as mqtt
import time

def on_connect(client, userdata, flags, rc):
   global flag_connected
   flag_connected = 1
   client_subscriptions(client)
   print("Connected to MQTT server")

def on_disconnect(client, userdata, rc):
   global flag_connected
   flag_connected = 0
   print("Disconnected from MQTT server")

# a callback functions
def callback_sensor(client, userdata, msg):
    print(msg.topic,": ",msg.payload.decode("utf-8"))

def client_subscriptions(client):
    client.subscribe("home/+/hmit")
    client.subscribe("home/+/temp")

client = mqtt.Client("sensors") #this should be a unique name
flag_connected = 0

client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.message_callback_add("home/+/hmit", callback_sensor)
client.message_callback_add("home/+/temp", callback_sensor)
client.connect("127.0.0.1",1883)
# start a new thread
client.loop_start()
client_subscriptions(client)
print("......client setup complete............")


while True:
    time.sleep(4)
    if (flag_connected != 1):
        print("trying to connect MQTT server..")
