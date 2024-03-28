## List All Step For Setup Base For Test Stream DATA

----

### 1. Setup Node Exporter ( Plugin for get Metric in Node )
```bash
docker run -d --name=node-exporter -p 9100:9100 prom/node-exporter
```

----

### 2. Setup Container Advisor ( Plugin for get Metric in Docker's Container )
```bash
docker run -d --name=container-advisor -p 9300:9300 prom/container-exporter
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

```

----

### 5. Setup Protheums ( Plugin for get all Metrics from Project want see the performace )

```bash
docker run -d -p 9090:9090 --name prometheus prom/prometheus
```

#### Check IP have connnect with ( targets service )
http://192.168.200.128:9090/targets?search=

#### Add more Target: Edit this file Prometheus.yaml
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
  - job_name: "prometheus"

    # metrics_path defaults to '/metrics'
    # scheme defaults to 'http'.

    static_configs:
      - targets: ["localhost:9090"]

  # The job name is added as a label `job=<job_name>` to any timeseries scraped from this config.
  - job_name: "ActsOne Performance"

    # metrics_path defaults to '/metrics'
    # scheme defaults to 'http'.

    static_configs:
      # In here you can put more ip for check performance, in here I trust make example
      - targets: ["localhost:9090", "1.22.3.4:9100"] 

```


----

#### 6. Setup App for run Test Redis Stream 

```bash 
docker run -d -p 5000:5000 --name add_task_redis linhtran2023/add_task_redis:v11
```

----

#### And then use this command 

```bash 
# Lệnh lấy file từ Docker Container ra ngoài ( VD: 601280c779bc = CONTAINER ID )
docker cp 601280c779bc:/etc/prometheus/prometheus.yml /etc/prometheus/prometheus.yml

# Tương tự copy ngược vào lại Container ( VD: 601280c779bc = CONTAINER ID )
docker cp prometheus.yml 601280c779bc:/etc/prometheus/prometheus.yml

# Restart lại contaniner đó ( VD: 601280c779bc = CONTAINER ID )
docker restart 601280c779bc
```


----


----

### Note for fix 

```bash

# Cái Container này cho chạy chung lớp mạng với prometheus
prom/container-exporter

```