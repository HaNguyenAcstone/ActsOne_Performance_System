# So in here  we just need setup 1 master 

#### Setup time for server
```bash
apt-get install chrony  
systemctl restart chronyd

# And then check time
watch -n 1 cmd

# Turn off the fire wall
sudo systemctl status ufw
sudo systemctl stop ufw
sudo ufw disable
```
-----

# Begin Setup

```bash
vi /etc/hosts

# In here put your Ip server
192.168.2.39 master master.demo.local

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