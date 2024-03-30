### 1. Setup Loki 

```bash
# So my loki-config.yaml stay in thí url /root/loki )

docker run --name loki -d -v /root/loki:/mnt/config -p 3100:3100 grafana/loki:2.9.1

nano loki-config.yaml
```

```bash
auth_enabled: false

server:
  http_listen_port: 3100

ingester:
  lifecycler:
    address: 127.0.0.1
    ring:
      kvstore:
        store: inmemory
      replication_factor: 1

schema_config:
  configs:
    - from: 2020-01-01
      store: boltdb
      object_store: filesystem
      schema: v11
      index:
        prefix: index_
        period: 24h

storage_config:
  boltdb:
    directory: /tmp/loki/index

  filesystem:
    directory: /tmp/loki/chunks

limits_config:
  enforce_metric_name: false
  reject_old_samples: true
  reject_old_samples_max_age: 168h

chunk_store_config:
  max_look_back_period: 0s

table_manager:
  retention_deletes_enabled: false
  retention_period: 0

```
-----

### 2. Setup promtail 

* DaemonSet

```bash 
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: promtail-daemonset
spec:
  selector:
    matchLabels:
      app: promtail
  template:
    metadata:
      labels:
        app: promtail
    spec:
      containers:
      - name: promtail
        image: grafana/promtail:latest  # Thay đổi tag image tùy theo phiên bản mong muốn
        args:
        - -config.file=/etc/promtail/promtail-config.yaml
        volumeMounts:
        - name: promtail-config
          mountPath: /etc/promtail
      schedulerName: default-scheduler
      securityContext: {}
      terminationGracePeriodSeconds: 30
      volumes:
      - name: promtail-config
        configMap:
          name: promtail-configmap

```

* ConfigMap

```bash
apiVersion: v1
kind: ConfigMap
metadata:
  name: promtail-configmap
data:
  promtail-config.yaml: |-
    server:
      http_listen_port: 9080
    positions:
      filename: /tmp/positions.yaml
    clients:
      - url: http://192.168.10.133:3100/loki/api/v1/push  # Cập nhật địa chỉ Loki của bạn
    scrape_configs:
      - job_name: kubernetes-pods
        static_configs:
        - targets:
            - localhost
          labels:
            job: varlogs
            __path__: /var/log/*/*.log
```
