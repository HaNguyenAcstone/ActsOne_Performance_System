
### Another Tips

----

### Setup Telegraf have same network with prometheus

#### Telegraf is ?

Telegraf is an open-source tool designed for collecting, processing, and sending metrics and data from various sources within a system for monitoring and analysis purposes. It supports gathering data from diverse inputs such as logs, services, system resources, and external sources like SNMP and Docker. Telegraf can then send this collected data to storage systems like InfluxDB or other monitoring systems using protocols such as Prometheus and Graphite. It's highly flexible and extensible, allowing users to customize data collection and processing according to their specific needs.
 

### File Docker Compose Setup prometheus + telegraf

```bash 

# Lưu ý ở đây telegraf sẽ phải cùng lớp mạng với prometheus, vì telegraf hoạt động ở nội mạng với Docker

version: '3'
services:
  prometheus:
    image: prom/prometheus:latest
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
    ports:
      - "9090:9090"

  telegraf:
    image: telegraf:latest
    volumes:
      - ./telegraf.conf:/etc/telegraf/telegraf.conf:ro
    depends_on:
      - prometheus  # Telegraf phụ thuộc vào Prometheus

```