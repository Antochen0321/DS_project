import etcd3
import time
import sys
import os
import grpc
from concurrent import futures
import node_pb2
import node_pb2_grpc

# this script need to be executed for every node, it's made to register every nodes informations and to elect the leader node

### INSTRUCTIONS : to launch the etcd server, to be executed in shell : 

# for one local node (test), change by the real node code implementation :

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
ETCD_HOST = '127.0.0.1' #  Customoizable
ETCD_PORT = 2379  # Customoizable

# SCRIPT

class NodeService(node_pb2_grpc.NodeServiceServicer):
    # Communication via gRPC
    def SendTask(self, request, context):
        print(f"Task received: {request.task}")
        # Traiter la tâche ici
        return node_pb2.TaskResponse(message="Task completed")

def start_grpc_server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    node_pb2_grpc.add_NodeServiceServicer_to_server(NodeService(), server)
    server.add_insecure_port('[::]:50051')
    print(f"gRPC server started on port 50051")
    server.start()
    server.wait_for_termination()

def connect_etcd():
    """Connect to etcd local server"""
    try:
        etcd = etcd3.client(host=ETCD_HOST, port=ETCD_PORT)
        print(f"Connexion à {ETCD_HOST}:{ETCD_PORT}")
        return etcd
    except Exception as e:
        print(f"Erreur : {e}")
        sys.exit(1)

def register_node(etcd, node_id, ip):
    """Register a node on the local server."""
    print(f"Registration of {node_id} with this ip : {ip}")
    etcd.put(f"/nodes/{node_id}", ip)

def get_registered_nodes(etcd):
    """Get registered nodes from the local server."""
    nodes = {}
    for value, metadata in etcd.get_prefix("/nodes/"):
        key = metadata.key.decode("utf-8").split("/")[-1]
        nodes[key] = value.decode("utf-8")
    return nodes

def main():
    etcd = connect_etcd()

    register_node(etcd, NODE_ID, NODE_IP)
    time.sleep(1)

    print("\nNœuds enregistrés :")
    nodes = get_registered_nodes(etcd)
    for node, ip in nodes.items():
        print(f"{node} : {ip}")
    
    # Start the grpc server to do the inter node communication
    start_grpc_server()

# Execution of main function
if __name__ == "__main__":
    main()



