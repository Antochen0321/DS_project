import etcd3
import time
import sys
import os

# this script need to be executed for every node, it's made to register every nodes informations and to elect the leader node

### INSTRUCTIONS : to launch the etcd server, to be executed in shell : 

# for one local node (test) :

"""etcd --name node1 --data-dir /tmp/etcd-node1 --listen-client-urls http://0.0.0.0:2379 --advertise-client-urls http://127.0.0.1:2379 --listen-peer-urls http://0.0.0.0:2380 --initial-cluster node1=http://127.0.0.1:2380
"""

"""export NODE_ID=node1
export NODE_IP=127.0.0.1
python etcd_cluster.py
"""

# CONFIGURATION

NODE_ID = os.getenv('NODE_ID', 'node1') 
NODE_IP = os.getenv('NODE_IP', '127.0.0.1')

# Configuration of ETCD local server
ETCD_HOST = os.getenv('ETCD_HOST', 'host.docker.internal') #  Customoizable
ETCD_PORT = 2379  # Customoizable

# SCRIPT

def connect_etcd():
    """Used to connect to the local etcd server"""
    try:
        etcd = etcd3.client(host=ETCD_HOST, port=ETCD_PORT)
        print(f"Connexion to {ETCD_HOST}:{ETCD_PORT}")
        return etcd
    except Exception as e:
        print(f"Error : {e}")
        sys.exit(1)

def register_node(etcd, node_id, ip):
    """Register a node inside the etcd server."""
    print(f"Registration of the node {node_id} with this ip : {ip}")
    etcd.put(f"/nodes/{node_id}", ip)

def get_registered_nodes(etcd):
    """Get registered nodes from the server."""
    nodes = {}
    for value, metadata in etcd.get_prefix("/nodes/"):
        key = metadata.key.decode("utf-8").split("/")[-1]
        nodes[key] = value.decode("utf-8")
    return nodes

def leader_election(etcd):
    """Leader election"""
    lease = etcd.lease(10)
    if leader:
        print(f"Leader already elected: {leader[0].decode('utf-8')}")
        return False
    if etcd.put_if_not_exists("/leader", NODE_ID, lease):
        print(f"Node {NODE_ID} as been elected leader.")
        return True
    print(f"Node {NODE_ID} is not the leader")
    return False

def main():
    etcd = connect_etcd()

    # Register the node
    register_node(etcd, NODE_ID, NODE_IP)
    time.sleep(1)

    # Print all registered nodes
    print("\nRegistered Node:")
    nodes = get_registered_nodes(etcd)
    for node, ip in nodes.items():
        print(f"{node} : {ip}")
    
    # Elect the leader
    leader_election(etcd)

# Execution of main function
if __name__ == "__main__":
    main()