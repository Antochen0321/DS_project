from locust import HttpUser, task, between

class DistributedSystemUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def test_ping_node(self):
        self.client.get("http://node1:50051")

    @task
    def test_ping_other_node(self):
        self.client.get("http://node2:50051")
