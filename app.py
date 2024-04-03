from confluent_kafka import Producer
import socket
import time

conf = {"bootstrap.servers": "kafka-service:9092", "client.id": socket.gethostname()}
producer = Producer(conf)


for i in range(15):
    
    time.sleep(2)
    producer.produce("minikube-topic", key="message", value="Linh 2" + i)