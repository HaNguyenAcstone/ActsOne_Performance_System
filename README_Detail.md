### Logic for check Performance of System 

### In ActsOne now run applicaction in Docker, we will use the way for docker

Docker => ( Setup Metric in project ) => Prometheus => Grafana

* Metric is ?

Metric is plugin for get all specifications of 1 container, node, or system run.

* Prometheus is ?

Prometheus is opensource for get all information for Metric and then send that to Grafana for show with user view.

----

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