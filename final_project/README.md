### 0 : create the local network with docker :

sudo usermod -aG docker $USER
newgrp docker
docker network create --subnet=172.18.0.0/16 ds_project


### 1 : Build docker images :

docker build -f ./multinode/node1/Dockerfile.node1 -t node1 .
docker build -f ./multinode/node2/Dockerfile.node2 -t node2 .

### 2 : run ntp (via chrony) and etcd servers :

sudo systemctl start chronyd
sudo systemctl enable chronyd

#### optional : to verify if all is good : sudo systemctl status chronyd

etcd --name node1 --data-dir /tmp/etcd-node1 --listen-client-urls http://0.0.0.0:2379 --advertise-client-urls http://172.18.0.2:2379 --listen-peer-urls http://0.0.0.0:2380 --initial-cluster node1=http://172.18.0.2:2380,node2=http://172.18.0.3:2380
etcd --name node1 \
  --data-dir /tmp/etcd-node1 \
  --listen-client-urls http://0.0.0.0:2379 \
  --advertise-client-urls http://127.0.0.1:2379 \
  --listen-peer-urls http://0.0.0.0:2380 \
  --initial-advertise-peer-urls http://10.10.17.188:2380 \
  --initial-cluster node1=http://10.10.17.188:2380

### 3 : Launch containers :

docker run --network ds_project --ip 172.18.0.2 -d --name node1 ds_project
docker run --network ds_project --ip 172.18.0.3 -d --name node2 ds_project
