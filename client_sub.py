import paho.mqtt.client as mqtt
import time
import requests

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

    data = msg.payload.decode("utf-8")
    data = data.split(",")
    tempF = data[0]
    tempC = data[2]
    hum = data[1]
    print(msg.topic,": tempF = ",tempF, " tempC = ", tempC, " hum = ", hum)
    topic = msg.topic
    url = "https://osuscc-testing.azurewebsites.net/api/homes/63c8a874922df840d1d7ec0f/" + topic
    myobj = [
                {
                    "temp_f": tempF,
                    "temp_c": tempC,
                    "humidity": str(hum),
                    "date_time": str(time.time())
                }
            ]
    myobj2 = {"testkey": "testvalue"}
    x = requests.put(url, json=myobj)
    print(x.status_code)

    # Send data to file
    data = open("test_sensor_data.csv", "a")
    send = "{},{}\n".format(msg.topic, msg.payload.decode("utf-8"))
    data.write(send)
    data.close()

def client_subscriptions(client):
    #client.subscribe("home/+/hmit")
    client.subscribe("sensors/+/readings")

client = mqtt.Client("sensors") #this should be a unique name
flag_connected = 0

client.on_connect = on_connect
client.on_disconnect = on_disconnect
#client.message_callback_add("home/+/hmit", callback_sensor)
client.message_callback_add("sensors/+/readings", callback_sensor)
client.connect("127.0.0.1",1883)
# start a new thread
client.loop_start()
client_subscriptions(client)
print("......client setup complete............")


while True:
    time.sleep(4)
    if (flag_connected != 1):
        print("trying to connect MQTT server..")
