### 1. Setup Loki 

* So have Note: Loki will save all logs from Promtail, so this one with use many storage, so we need control and clear log in some time.

```bash
# So my loki-config.yaml stay in thí url /root/loki )

docker run --name loki -d -v /root/loki:/mnt/config -p 3100:3100 grafana/loki:2.9.1

nano loki-config.yaml
```

* Use this content 

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

### 2. Setup Promtail for get all logs in every node with ( Daemonset )

Link Docs Detail: https://grafana.com/docs/loki/latest/send-data/promtail/installation/

* Create value file 

```bash
helm repo update

helm repo add grafana https://grafana.github.io/helm-charts

helm repo update
```

##### Create the configuration file values.yaml with this conntent

```bash
config:
  # publish data to loki
  clients:
    - url: http://loki-gateway/loki/api/v1/push
      tenant_id: 1
```

#### The default helm configuration deploys promtail as a daemonSet (recommended)
```bash 
helm upgrade --values values.yaml --install promtail grafana/promtail
```