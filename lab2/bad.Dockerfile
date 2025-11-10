FROM ubuntu:latest

RUN apt-get update
RUN apt-get install -y python3 python3-pip
RUN pip3 install flask

COPY . /app
WORKDIR /app

ENV SECRET_KEY=my_super_secret_key_12345

CMD["python3", "app.py"]
