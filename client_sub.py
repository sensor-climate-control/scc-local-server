import paho.mqtt.client as mqtt
import time
import requests
import sys

def on_connect(client, userdata, flags, rc):
   flag_connected = 1
   client_subscriptions(client)
   print("Connected to MQTT server")

def on_disconnect(client, userdata, rc):
   global flag_connected
   flag_connected = 0
   print("Disconnected from MQTT server")

# a callback functions
def callback_sensor(client, userdata, msg):
    upload = str(sys.argv[1])
    
    # send data to server
    if upload == "remote" or upload == "both":
        data = msg.payload.decode("utf-8")
        data = data.split(",")
        tempF = data[0]
        tempC = data[2]
        hum = float(data[1])
        print(msg.topic,": tempF = ",tempF, " tempC = ", tempC, " hum = ", hum)
        url = "https://osuscc-testing.azurewebsites.net" + msg.topic
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
    if upload == "local" or upload == "both":
        data = open("./python/data/test_sensor_data.csv", "a")
        send = "{},{}\n".format(msg.topic, msg.payload.decode("utf-8"))
        data.write(send)
        data.close()

def client_subscriptions(client):
    client.subscribe("/api/homes/+/sensors/+/readings")

def connect(client, flag_connected, ip, port):
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.message_callback_add("/api/homes/+/sensors/+/readings", callback_sensor)

    client.connect(ip, port)
            
    # start a new thread
    client.loop_start()
    client_subscriptions(client)
    print("......client setup complete............")
    print("Trying to connect to MQTT server ...")

    while True:
        time.sleep(4)

def main():
    client = mqtt.Client("sensors") #this should be a unique name
    flag_connected = 0
    ip = "10.0.0.182"
    port = 1883

    connect(client, flag_connected, ip, port)
    
if __name__ == '__main__':
    main()
