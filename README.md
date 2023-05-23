# scc-local-server

## Equipment

### Required Software
- Docker: https://docs.docker.com/get-docker/
- Docker Compose:  https://docs.docker.com/compose/install/
>*Should be pre installed, might need to install manually*
>*Need to have Docker Desktop running if using a Windows machine*
- Ubuntu 22.10:  https://ubuntu.com/download/desktop
> *Used for testing, should work with other operating systems*

### Required Hardware
- Raspberry Pi 4 Model B Rev 1.2: https://www.raspberrypi.com/products/raspberry-pi-4-model-b/
> *Used for testing, should work with other hardware*

### Docker Containers:
- MQTT Broker: https://hub.docker.com/_/eclipse-mosquitto
- MQTT Subscriber: https://hub.docker.com/repository/docker/redfernj/scc-local-server-docker/general
>*When "client_sub.py" is modified it is automatically compiled and sent to Docker Hub.*

## Configuration

### Example compose.yml
```.yml
services:

############################################################ MQTT Broker

  mosquitto:
    image: eclipse-mosquitto
    container_name: mqtt
    ports:
      - 1883:1883
      - 9001:9001
    restart: unless-stopped
    volumes:
      - ./mosquitto/config:/mosquitto/config
      - ./mosquitto/data:/mosquitto/data
      - ./mosquitto/log:/mosquitto/log

############################################################ MQTT Subscriber

  python-app:
    image: redfernj/scc-local-server-docker
    container_name: python
    volumes:
      - ./python/data:/usr/src/app/python/data
    env_file: .env
```

### Example mosquitto.conf
```.conf
persistence true
persistence_location /mosquitto/data
log_dest file /mosquitto/log/mosquitto.log

listener ??? # Your ip address
listener 1883
allow_anonymous true
```

### Example .env
```.env
# Will the data revived from the MQTT server will be
# both - stored locally and uploaded to a web server
# remote - only uploaded to a web server
# local - only stored locally
UPLOAD=both

# IP address the machine the MQTT server will run on
IP=??? # Your ip address

# URL for where to send the data via PUT request
# - By default: https://osuscc-testing.azurewebsites.net
URL=https://osuscc.azurewebsites.net


# Authentication token to upload data to the server
TOKEN=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2NDQwOTg5MjBiZGIzYjYwYjdkZWNhOGYiLCJpYXQiOjE2ODE5NTUxNTMsImV4cCI6MTcxMzQ5MTE1M30.gILdaaKY6PX7mEdeSkSRGHbnwZzlZG0xWz8678hvZf0
```

### Example File Structure
```
./mosquitto/config/mosquitto.conf
./mosquitto/data
./mosquitto/log
./python/data
./.env
./compose.yml
```
## Run

### Start
```
docker compose up --build -d
```

### Stop
```
docker compose down
```

<img src="./scc-local-server-diagram.svg">
