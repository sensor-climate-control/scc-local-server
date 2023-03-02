# scc-local-server

### Required Software
- Docker: https://docs.docker.com/get-docker/
- Docker Compose:  https://docs.docker.com/compose/install/
>*Should be pre installed, might need to install manually*
- Ubuntu 22.10:  https://ubuntu.com/download/desktop
> *Used for testing, should work with other operating systems*

### Required Hardware
- Raspberry Pi 4 Model B Rev 1.2: https://www.raspberrypi.com/products/raspberry-pi-4-model-b/
> *Used for testing, should work with other hardware*

### Docker Containers:
- MQTT Broker: https://hub.docker.com/_/eclipse-mosquitto
- MQTT Subscriber: https://hub.docker.com/repository/docker/redfernj/scc-local-server-docker/general
>*When "client_sub.py" is modified it is automatically compiled and sent to Docker Hub.*

### Example .yml file

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

### Example File Structure:
```
./mosquitto/config
./mosquitto/data
./mosquitto/log
./python/data
./.env
./compose.yml
```

<img src="./scc-local-server-diagram.svg">
