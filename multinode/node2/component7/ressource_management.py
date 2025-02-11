import random
import time

### SCRIPT

class NodeResources:
    """Simulate the ressource management for every node"""
    def __init__(self, node_name):
        self.node_name = node_name
        self.cpu = 100  # % of cpu
        self.memory = 100  # % of memory
        self.gpu = 100  # % of GPU

    def allocate_resources(self):
        """Simulate ressource allocations"""
        cpu_allocation = random.randint(10, 30)
        memory_allocation = random.randint(10, 20)
        gpu_allocation = random.randint(0, 10)
        self.cpu -= cpu_allocation
        self.memory -= memory_allocation
        self.gpu -= gpu_allocation

        print(f"Allocated {cpu_allocation}% CPU, {memory_allocation}% Memory, {gpu_allocation}% GPU on {self.node_name}")
        print(f"Remaining resources on {self.node_name} -> CPU: {self.cpu}%, Memory: {self.memory}%, GPU: {self.gpu}%")

    def check_resources(self):
        print(f"Checking resources for {self.node_name}...")
        print(f"CPU: {self.cpu}%, Memory: {self.memory}%, GPU: {self.gpu}%")
        return self.cpu, self.memory, self.gpu

# Ressource allocations for nodes 1 and 2
node1_resources = NodeResources("node1")
node2_resources = NodeResources("node2")

# Execution of the script
for _ in range(5):
    node1_resources.allocate_resources()
    node2_resources.allocate_resources()
    time.sleep(3)
