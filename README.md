## Steam Data Solution

<img src="Picture/1.png" ><br>


### What is Steam Data  ?

Stream Data is a technique that allows processing data in real-time or near-real-time, where data is processed as a continuous stream rather than as fixed or static chunks. It enables handling of unbounded data, ensuring ordered data processing. Technologies like Redis Streams and Kafka Streams provide mechanisms to manage and process data in this streaming fashion, commonly used in data analytics, state monitoring, log processing, and various other real-time data processing scenarios.

----

### Table of contents

#### 1.Setup environment

# Mục Lục

1. [Giới Thiệu](#giới-thiệu)
2. [Cài Đặt](#cài-đặt)
3. [Sử Dụng](#sử-dụng)
4. [Hướng Dẫn](#hướng-dẫn)

## Giới Thiệu

Đây là phần giới thiệu.

## Cài Đặt

Đây là phần hướng dẫn cài đặt.

## Sử Dụng

Đây là phần hướng dẫn sử dụng.

## Hướng Dẫn

Đây là phần hướng dẫn chi tiết.


* [Setup Docker and K8S](#setup-docker-and-k8s)

* Setup Redis

* Setup Kafka

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

### Setup Docker and K8S {#setup-docker-and-k8s}

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





































### 1. Setup Node Exporter ( Plugin for get Metric in Node )
```bash
docker run -d --name=node-exporter -p 9100:9100 prom/node-exporter
```

----

### 2. Setup Container Exporte ( Plugin for get Metric in Docker's Container )
```bash
docker run -d -p 9104:9104 -v /var/run/docker.sock:/var/run/docker.sock --name=docker-exporter prom/container-exporter:latest
```

----

### 3. Setup Grafana ( Website for show Chart View )

```bash 
# Make the docker-compose.yml file with this content 
version: '3'
services:
  grafana:
    image: grafana/grafana:latest
    container_name: grafana
    ports:
      - "3000:3000"
    volumes:
      - /var/lib/grafana:/var/lib/grafana
    restart: always

# And then run this one 
docker-compose up -d

# Grafana will run in pod: 3000
root@serverlocal:~# docker ps
CONTAINER ID   IMAGE                               COMMAND                  CREATED          STATUS             PORTS                                       NAMES
4fcec7d72e72   grafana/grafana:latest              "/run.sh"                4 hours ago      Up About an hour   0.0.0.0:3000->3000/tcp, :::3000->3000/tcp   grafana

# Note is: Infor login default is: admin / admin 
```

----

### 4. Setup Redis ( Database No SQL )

```bash
version: '3'

services:
  redis:
    image: redis
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

volumes:
  redis_data:

# And then run this one, redis sẽ chạy trên pod 6379
docker-compose up -d

# Check again 
root@serverlocal:~# docker ps
CONTAINER ID   IMAGE                               COMMAND                  CREATED              STATUS              PORTS                                       NAMES
1fcd6b7e85b3   redis                               "docker-entrypoint.s…"   About a minute ago   Up About a minute   0.0.0.0:6379->6379/tcp

# Or Also can use this for fast Setup
docker run --name redis -d -p 6379:6379 redis

```
----

### 5. Setup Protheums ( Plugin for get all Metrics from Project want see the performace )

```bash
docker run -d -p 9090:9090 --name prometheus prom/prometheus
```

#### Check IP have connnect with ( targets service )
http://192.168.200.128:9090/targets?search=

#### Add more Target: Edit this file prometheus.yaml
```bash
# my global config
global:
  scrape_interval: 15s # Set the scrape interval to every 15 seconds. Default is every 1 minute.
  evaluation_interval: 15s # Evaluate rules every 15 seconds. The default is every 1 minute.
  # scrape_timeout is set to the global default (10s).

# Alertmanager configuration
alerting:
  alertmanagers:
    - static_configs:
        - targets:
          # - alertmanager:9093

# Load rules once and periodically evaluate them according to the global 'evaluation_interval'.
rule_files:
  # - "first_rules.yml"
  # - "second_rules.yml"

# A scrape configuration containing exactly one endpoint to scrape:
# Here it's Prometheus itself.
scrape_configs:

  # The job name is added as a label `job=<job_name>` to any timeseries scraped from this config.
  - job_name: "ActsOne Message"
    # metrics_path defaults to '/metrics'
    # scheme defaults to 'http'.
    static_configs:
      - targets: ["192.168.10.133:9100:5000"]

  # The job name is added as a label `job=<job_name>` to any timeseries scraped from this config.
  - job_name: "ActsOne Performance"
    # metrics_path defaults to '/metrics'
    # scheme defaults to 'http'.
    static_configs:
      # In here you can put more ip for check performance, in here I trust make example
      - targets: ["192.168.10.133:9100:9090"] 
```

----

### Command usual use 

```bash 

docker run -d -p 5000:5000 --name my_container linhtran2023/actsone_performance_system:v19

# Command help copy file from Container to Local ( VD: 601280c779bc = CONTAINER ID )
docker cp 601280c779bc:/etc/prometheus/prometheus.yml /etc/prometheus/prometheus.yml

# Command help copy file from local to Container ( VD: 601280c779bc = CONTAINER ID )
docker cp prometheus.yml 601280c779bc:/etc/prometheus/prometheus.yml

# Restart lại contaniner đó ( VD: 601280c779bc = CONTAINER ID )
docker restart 601280c779bc

# Command for join docker container 
docker exec -it 601280c779bc sh

# Command for get name of network layer --------------------------------------
docker inspect -f '{{.NetworkSettings.Networks}}' my_container_id

# EX for run 1 container with Network you want (--network=prometheus_default)
docker run -d --name=container-advisor -p 9300:9300 --network=prometheus_default prom/container-exporter

# Command for get ip inside Docker Container
docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' e11d293d6782

# Command for chance the network for container u want ( 7432faf616e8 is Container ID)
docker network connect prometheus_default 7432faf616e8

```