import etcd3
import time

# this script need to be executed for every node, it's made to register every nodes informations and to elect the leader node

### INSTRUCTIONS : to launch the etcd server, to be executed in shell : 

# for one local node (test) :

"""etcd --name localnode --data-dir /tmp/etcd-data --listen-client-urls http://127.0.0.1:2379 --advertise-client-urls http://127.0.0.1:2379"""

# for a server (if local, ip needs to be changed) :

"""etcd --name node1 --data-dir /tmp/etcd-data \
     --listen-client-urls http://0.0.0.0:2379 \
     --advertise-client-urls http://192.168.1.101:2379 \
     --listen-peer-urls http://0.0.0.0:2380 \
     --initial-advertise-peer-urls http://192.168.1.101:2380 \
     --initial-cluster node1=http://192.168.1.101:2380,node2=http://192.168.1.102:2380,node3=http://192.168.1.103:2380 \
     --initial-cluster-state new --initial-cluster-token etcd-cluster-1"""

# to verify if nodes are registered :

"""ETCDCTL_API=3 etcdctl get --prefix /
/nodes/test_node"""

# to clean registered node

"""rm -rf /tmp/etcd-data"""

### CONFIGURATION, MODIFY THE CODE HERE

NODE_ID = "test_node"  # node information, node1 or node2 etcd
NODE_IP = "127.0.0.1"  # put the ip adress of the current node
ETCD_HOST = "127.0.0.1"  # put the adress used to launch the server, if the command above is used, do not modify
ETCD_PORT = 2379  # etcd server port, if the command above is used, do not modify
LEASE_TTL = 10  # Time duration used to elect the node leader

### END OF CONFIGURATION, DO NOT MODIFY

### SCRIPT :

# Connexion to the cluster
etcd = etcd3.client(host=ETCD_HOST, port=2379)  

def register_node(node_id, ip):
    """Register the node in etcd server"""
    etcd.put(f"/nodes/{node_id}", ip)
    print(f"Node {node_id} registered with this ip : {ip}")

def get_registered_nodes():
    """Take every registered node."""
    nodes = {}
    for value, metadata in etcd.get_prefix("/nodes/"):
        key = metadata.key.decode("utf-8").split("/")[-1]
        nodes[key] = value.decode("utf-8")
    return nodes

def leader_election():
    """Elect the good leader, the choice is based on etcd data."""
    lease = etcd.lease(10)
    if etcd.put_if_not_exists("/leader", "node1", lease):
        print("This node is the new leader")
        return True
    print("Error: this node is not the leader, select the good node.")
    return False


### MAIN SCRIPT PART

if __name__ == "__main__":
    print(f"\n--- {NODE_ID} launch ---")
    
    register_node(NODE_ID, NODE_IP)
    time.sleep(2)

    nodes = get_registered_nodes()
    print("\n Registered nodes:", nodes)

    leader_election()
