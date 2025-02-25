import time
import random

### SCRIPT

def simulate_latency():
    """Simulate latency between nodes"""
    return random.uniform(0.1, 1.0) 

def simulate_cpu_usage():
    """Simulate cpu usage for nodes"""
    return random.uniform(0, 100)

def simulate_memory_usage():
    """Simulate memory usage"""
    return random.uniform(0, 16)

def log_metrics():
    """Print log metrics"""
    latency = simulate_latency()
    cpu_usage = simulate_cpu_usage()
    memory_usage = simulate_memory_usage()
    
    print(f"Latence: {latency:.2f} ms")
    print(f"CPU Usage: {cpu_usage:.2f} %")
    print(f"Memory Usage: {memory_usage:.2f} GB")

### EXECUTION PART (MAIN)

if __name__ == "__main__":
    while True:
        log_metrics()
        time.sleep(5)
