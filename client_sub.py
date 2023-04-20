import paho.mqtt.client as mqtt
import time
import requests
from decouple import config

def on_connect(client, userdata, flags, rc):
    # If there is a successful connection to the MQTT server:
    # - Subscribe to all sensor MQTT topics
    # - Inform the user 

   client.subscribe("/api/homes/+/sensors/+/readings")
   print("Connected to MQTT server")

def on_disconnect(client, userdata, rc):
    # If there is an interruption with the connection to the MQTT server:
    # - Inform the user

   print("Disconnected from MQTT server")
   print("Trying to connect to MQTT server...")

# Callback Function
def callback_sensor(client, userdata, msg):
    # If a message is received from the server
    upload = config("UPLOAD")
    data = msg.payload.decode("utf-8")
    data = data.split(",")
    tempF = data[0]
    tempC = data[2]
    hum = float(data[1])
    print(msg.topic,": tempF = ",tempF, " tempC = ", tempC, " hum = ", hum)

    # - Send data to server
    if upload == "remote" or upload == "both":
        url = config("URL") + msg.topic

        myobj = [
                    {
                        "temp_f": tempF,
                        "temp_c": tempC,
                        "humidity": str(hum),
                        "date_time": str(time.time())
                    }
                ]
        headers = {
            "Authorization": f"Bearer {config('TOKEN')}" 
        }
        x = requests.put(url, json=myobj, headers=headers)
        print(x.status_code)

    # - Send data to file
    if upload == "local" or upload == "both":
        data = open("./python/data/sensor_data.csv", "a")
        send = "{},{}\n".format(msg.topic, msg.payload.decode("utf-8"))
        data.write(send)
        data.close()

def connect(client, flag_connected, ip, port):
    # What to do when there is a connection/disconnection with the MQTT server
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect

    # What to do when data is revived from the topic for the MQTT server
    client.message_callback_add("/api/homes/+/sensors/+/readings", callback_sensor)

    # Create a Thread
    client.loop_start()
    print("............client setup complete............")

    # Attempt to connect to the MQTT server
    print("Trying to connect to MQTT server...")

    while(flag_connected == False):
        try:
            client.connect(ip, port, 120)
        except Exception as e:
            print("Re-trying...")
        else:
            # Loop Forever
            flag_connected = True
            while True:
                time.sleep(4)
            


def main():
    # Create starter variables
    client = mqtt.Client("sensors") #this should be a unique name
    flag_connected = 0
    ip = config("IP")
    print("IP: ", ip)
    port = 1883

    connect(client, flag_connected, ip, port)
    
if __name__ == '__main__':
    main()
