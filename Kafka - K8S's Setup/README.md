Research's Link: https://www.datumo.io/blog/setting-up-kafka-on-kubernetes

### Setup: zookeeper-deployment

* Node: Need setting about Storage when deploy in Production.

```bash
apiVersion: apps/v1
kind: Deployment
metadata:
  name: zookeeper-deployment
  labels:
    app: zookeeper
spec:
  replicas: 1
  selector:
    matchLabels:
      app: zookeeper
  template:
    metadata:
      labels:
        app: zookeeper
    spec:
      containers:
      - name: zookeeper
        image: confluentinc/cp-zookeeper:7.0.1
        ports:
        - containerPort: 2181
        env:
        - name: ZOOKEEPER_CLIENT_PORT
          value: "2181"
        - name: ZOOKEEPER_TICK_TIME
          value: "2000"
```

### Service: zookeeper-service

``` bash

apiVersion: v1
kind: Service
metadata:
  name: zookeeper-service
spec:
  selector:
    app: zookeeper
  ports:
    - protocol: TCP
      port: 2181
      targetPort: 2181

``` 

----

### Setup: kafka-deployment

#### Need pull images before deploy by K8S, Images is Large Size

```bash
docker pull confluentinc/cp-kafka:7.0.1
```

```bash
apiVersion: apps/v1
kind: Deployment
metadata:
  name: kafka-deployment
  labels:
    app: kafka
spec:
  replicas: 1
  selector:
    matchLabels:
      app: kafka
  template:
    metadata:
      labels:
        app: kafka
    spec:
      containers:
      - name: broker
        image: confluentinc/cp-kafka:7.0.1
        ports:
        - containerPort: 9092
        env:
        - name: KAFKA_BROKER_ID
          value: "1"
        - name: KAFKA_ZOOKEEPER_CONNECT
          value: 'zookeeper-service:2181'
        - name: KAFKA_LISTENER_SECURITY_PROTOCOL_MAP
          value: PLAINTEXT:PLAINTEXT,PLAINTEXT_INTERNAL:PLAINTEXT
        - name: KAFKA_ADVERTISED_LISTENERS
          value: PLAINTEXT://:29092,PLAINTEXT_INTERNAL://kafka-service:9092
        - name: KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR
          value: "1"
        - name: KAFKA_TRANSACTION_STATE_LOG_MIN_ISR
          value: "1"
        - name: KAFKA_TRANSACTION_STATE_LOG_REPLICATION_FACTOR
          value: "1"

```

### Service: zookeeper-service

```bash
apiVersion: v1
kind: Service
metadata:
  name: kafka-service
spec:
  selector:
    app: kafka
  ports:
    - protocol: TCP
      port: 9092
      targetPort: 9092

```

### Puplic Code 

```bash 

apiVersion: v1
kind: Service
metadata:
  name: kafka-service-public
spec:
  selector:
    app: kafka
  ports:
    - protocol: TCP
      port: 9092
      targetPort: 9092
  type: NodePort

```

---

### Note: 

IP Server's kafka-deployment, will be not public to connect with app in localtion call them, so we need make 1 service for connect to them like middleware.

#### Example:

```bash 

from confluent_kafka import Producer
import socket
import time

# Config for connect Producer Service
conf = {"bootstrap.servers": "kafka-service:9092", "client.id": socket.gethostname()}
producer = Producer(conf)


for i in range(15):
    
    time.sleep(2)
    producer.produce("minikube-topic", key="message", value="Linh 2")

```