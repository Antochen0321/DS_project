import requests
import time

### DATA TO CHANGE HERE

# data which must be replicated, must be adapt to nodes configuration
data = {"key": "value"}

# nodes list
nodes = ["node1", "node2"]

### SCRIPT

def replicate_data(data, node_url):
    """Simulate a replication between nodes to observe reactions."""
    try:
        response = requests.post(f'http://{node_url}/replicate', json=data)
        if response.status_code == 200:
            print(f"Data replicated successfully to {node_url}")
        else:
            print(f"Failed to replicate data to {node_url}")
    except Exception as e:
        print(f"Error during replication: {e}")

# Execution of the script
for node in nodes:
    replicate_data(data, node)
    time.sleep(2)
