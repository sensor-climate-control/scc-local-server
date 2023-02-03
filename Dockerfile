#FROM ubuntu:latest

#RUN apt update
#RUN apt-get update && apt-get install -y \
#	python3\
#	python3-pip
#RUN pip3 install paho

#WORKDIR /usr/app/src

#COPY client_sub.py ./

FROM python:3

WORKDIR /usr/app/src
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY client_sub.py ./

RUN python client_sub.py

#COPY . .
#CMD [ "python", "./client_sub.py" ]
