## Steam Data Solution

<img src="Picture/1.png" ><br>


### What is Steam Data  ?

Stream Data is a technique that allows processing data in real-time or near-real-time, where data is processed as a continuous stream rather than as fixed or static chunks. It enables handling of unbounded data, ensuring ordered data processing. Technologies like Redis Streams and Kafka Streams provide mechanisms to manage and process data in this streaming fashion, commonly used in data analytics, state monitoring, log processing, and various other real-time data processing scenarios.

----

### Table of contents

#### 1.Setup environment

* [Setup Docker and K8S](#setup-docker-and-k8s)

* [Setup Redis](#setup-redis)

* [Setup Kafka](#setup-Kafka)

#### 2.Setup Monitor System

* Setup Grafana

* Setup Loki

* Setup Node Exporter 

#### 3. API For Test Server's Performance

* API - DdOS

* API - Kafka's

* API - Request Redis Streams

----

## 1.Setup environment

-----

### Setup Docker and K8S

#### . Setup Docker

```bash

sudo -i # Change to root
apt update
apt install docker
apt install docker-compose

```

#### . Setup K8S - Version RKE2

```bash
# Setup time for server ----------------
apt-get install chrony  
systemctl restart chronyd

# And then check time
watch -n 1 cmd

# Turn off the fire wall
sudo systemctl status ufw
sudo systemctl stop ufw
sudo ufw disable

# Begin Setup -------------------------
vi /etc/hosts

# In here put your Ip server
192.168.200.130  master master.demo.local

# Create rke2
mkdir -p /etc/rancher/rke2/

# Create tls-san for kubernetes
cat > /etc/rancher/rke2/config.yaml << HERE
tls-san:
- master1
- master1.demo.local
HERE

# Setup environment
export CONTAINER_RUNTIME_ENDPOINT=unix:///run/k3s/containerd/containerd.sock
export CONTAINERD_ADDRESS=/run/k3s/containerd/containerd.sock
export PATH=/var/lib/rancher/rke2/bin:$PATH
export KUBECONFIG=/etc/rancher/rke2/rke2.yaml
alias k=kubectl

# Download rke2
curl -sfL https://get.rke2.io | sh -

# Use this command if no have proxy
cat > /etc/default/rke2-server << HERE
CONTAINERD_NO_PROXY=localhost,127.0.0.0/8,10.0.0.0/8,172.16.0.0/12,192.168.0.0/16,.svc,.local
NO_PROXY=localhost,127.0.0.0/8,10.0.0.0/8,172.16.0.0/12,192.168.0.0/16,.svc,.local
HERE

# And then turn on for run
systemctl enable rke2-server
systemctl start rke2-server 

```

---

### Setup Redis

. Setup by Docker

```bash
docker run -d --name my-redis-container -p 6379:6379 redis
```

---

## Setup Kafka

### . Setup by K8S

Research's Link: https://www.datumo.io/blog/setting-up-kafka-on-kubernetes

#### zookeeper-deployment

<strong>Node</strong>: Need setting about Storage when deploy in Production.

```bash
# Deployment
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

---

# Service
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

#### kafka-deployment

<strong>Note</strong>: Need pull images before deploy by K8S, Images is Large Size.

```bash
docker pull confluentinc/cp-kafka:7.0.1
```

```bash
# Deployment
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

---

# Service
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

#### Note: 

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

---