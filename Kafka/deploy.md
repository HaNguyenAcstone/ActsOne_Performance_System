# Command for use Kubectl
```bash

# Setup ENV for use Kubectl command
export CONTAINER_RUNTIME_ENDPOINT=unix:///run/k3s/containerd/containerd.sock
export CONTAINERD_ADDRESS=/run/k3s/containerd/containerd.sock
export PATH=/var/lib/rancher/rke2/bin:$PATH
export KUBECONFIG=/etc/rancher/rke2/rke2.yaml
alias k=kubectl

# Step 1: Set the tutorial home directory
export TUTORIAL_HOME="https://raw.githubusercontent.com/confluentinc/confluent-kubernetes-examples/master/quickstart-deploy/kraft-quickstart"

# Step 2: Create a namespace

kubectl create namespace confluent

# Set this namespace to default for your Kubernetes context:
kubectl config set-context --current --namespace confluent

# Step 3: Install Confluent for Kubernetes 

snap install helm --classic

helm repo add confluentinc https://packages.confluent.io/helm

helm repo update

# Install Confluent for Kubernetes:
helm upgrade --install confluent-operator confluentinc/confluent-for-kubernetes

# Check that the CFK pod comes up and is running: 
root@serverlocal:~# k get pod
NAME                                 READY   STATUS    RESTARTS   AGE
confluent-operator-57596c56f-sd54s   1/1     Running   0          28s
root@serverlocal:~#

# Step 4: Install Confluent Platform

# 4.1 Deploy the KRaft controller and the Kafka brokers:
kubectl apply -f $TUTORIAL_HOME/confluent-platform.yaml

# 4.2 Install the sample producer app and topic:
kubectl apply -f $TUTORIAL_HOME/producer-app-data.yaml

# Wait until all the Confluent Platform components are deployed and running:
```


https://raw.githubusercontent.com/confluentinc/confluent-kubernetes-examples/master/quickstart-deploy/kraft-quickstart/confluent-platform.yaml



https://raw.githubusercontent.com/confluentinc/confluent-kubernetes-examples/master/quickstart-deploy/kraft-quickstart/producer-app-data.yaml