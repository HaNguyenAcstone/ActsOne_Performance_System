### Logic for check Performance of System 

-----

### In ActsOne now run applicaction in Docker, we will use the way for docker

Docker => ( Setup Metric in project ) => Prometheus => Grafana

* Metric is ?

Metric is plugin for get all specifications of 1 container, node, or system run.

* Prometheus is ?

Prometheus is opensource for get all information for Metric and then send that to Grafana for show with user view.

-----

### Step 1: Setup Grafana

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
```

### Step 2: Setup Telegraf
*** Telegraf is ?


Telegraf is an open-source tool designed for collecting, processing, and sending metrics and data from various sources within a system for monitoring and analysis purposes. It supports gathering data from diverse inputs such as logs, services, system resources, and external sources like SNMP and Docker. Telegraf can then send this collected data to storage systems like InfluxDB or other monitoring systems using protocols such as Prometheus and Graphite. It's highly flexible and extensible, allowing users to customize data collection and processing according to their specific needs.