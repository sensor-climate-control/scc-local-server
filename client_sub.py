import paho.mqtt.client as mqtt
import time
import requests
import sys

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
    upload = str(sys.argv[1])

    # send data to server
    if upload == "remote" or upload == "both":
        data = msg.payload.decode("utf-8")
        data = data.split(",")
        tempF = data[0]
        tempC = data[2]
        hum = float(data[1])
        print(msg.topic,": tempF = ",tempF, " tempC = ", tempC, " hum = ", hum)
        url = "https://osuscc-testing.azurewebsites.net/api/" + msg.topic
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
        data = open("test_sensor_data.csv", "a")
        send = "{},{}\n".format(msg.topic, msg.payload.decode("utf-8"))
        data.write(send)
        data.close()

def client_subscriptions(client):
    client.subscribe("homes/+/sensors/+/readings")

def main():
    client = mqtt.Client("sensors") #this should be a unique name
    flag_connected = 0
    ip = 10.0.0.182
    port = 1883

    while flag_connected == 0:
        print("Trying to connect to MQTT server...")
        client.on_connect = on_connect
        client.on_disconnect = on_disconnect
        client.message_callback_add("homes/+/sensors/+/readings", callback_sensor)

        connect.connect_timeout = 120
        try:
            client.connect(ip, port)
        except :
            print("Error connecting to server:\n ip:",ip," port:",port)
            time.sleep(4)
            
    # start a new thread
    client.loop_start()
    client_subscriptions(client)
    print("......client setup complete............")

if __name__ == '__main__':
    main()
