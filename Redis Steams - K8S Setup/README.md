### Command for use Kubectl

```bash
export CONTAINER_RUNTIME_ENDPOINT=unix:///run/k3s/containerd/containerd.sock
export CONTAINERD_ADDRESS=/run/k3s/containerd/containerd.sock
export PATH=/var/lib/rancher/rke2/bin:$PATH
export KUBECONFIG=/etc/rancher/rke2/rke2.yaml
alias k=kubectl
```
### File yaml for setup Redis Steams in K8S

```bash
# Deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-redis-streams
  namespace: default
spec:
  replicas: 10
  revisionHistoryLimit: 1
  selector:
    matchLabels:
      app: api-redis-streams
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 0
  template:
    metadata:
      labels:
        app: api-redis-streams
    spec:
      containers:
      - name: api-redis-streams
        image: linhtran2023/actsone_performance_system:v17
         # Cấu hình sử dụng thời gian của máy chủ
        env:
        - name: TZ
          value: "Asia/Ho_Chi_Minh"  # Thay đổi "Asia/Ho_Chi_Minh" bằng múi giờ của bạn
        resources:
          limits:
            cpu: "2"  # Giới hạn CPU tối đa là 2 core
            memory: "2Gi"  # Giới hạn bộ nhớ tối đa là 2GB
          requests:
            cpu: 200m      # Yêu cầu tối thiểu CPU là 0.2 core
            memory: 200m   # Yêu cầu tối thiểu bộ nhớ là 200MB
      restartPolicy: Always

---

# Service
apiVersion: v1
kind: Service
metadata:
  name: api-redis-streams
  namespace: default
spec:
  selector:
    app: api-redis-streams
  ports:
  - nodePort: 30000
    port: 5000
    protocol: TCP
    targetPort: 5000
  type: NodePort

```

### File yaml for setup API Test in K8S
```bash 
# Deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-producer-redis
  namespace: default
spec:
  replicas: 10
  revisionHistoryLimit: 1
  selector:
    matchLabels:
      app: api-producer-redis
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 0
  template:
    metadata:
      labels:
        app: api-producer-redis
    spec:
      containers:
      - name: api-producer-redis
        # Put your images to here
        image: linhtran2023/actsone_performance_system:v18
        # Settings the time same your location
        env:
        - name: TZ
          value: "Asia/Ho_Chi_Minh"  # "Asia/Ho_Chi_Minh"
      restartPolicy: Always

---

# Service
apiVersion: v1
kind: Service
metadata:
  name: api-producer-redis
  namespace: default
spec:
  selector:
    app: api-producer-redis
  ports:
  - nodePort: 30000
    port: 5000
    protocol: TCP
    targetPort: 5000
  type: NodePort
```

-----

## Tips

### Command for restart pod
```bash
kubectl rollout restart deployment actsone-message
```