import grpc
import service_pb2
import service_pb2_grpc

def run():
    channel = grpc.insecure_channel("db_service_node1:50051")  # Changer en db_service_node2 pour node2
    stub = service_pb2_grpc.DatabaseServiceStub(channel)

    # Create an entry
    response = stub.CreateEntry(service_pb2.Entry(id="1", data="Sample Data"))
    print(f"Create Success: {response.success}")

    # Read the entry
    entry = stub.ReadEntry(service_pb2.Query(id="1"))
    print(f"Read Entry: {entry.id}, {entry.data}")

    # Update the entry
    response = stub.UpdateEntry(service_pb2.Entry(id="1", data="Updated Data"))
    print(f"Update Success: {response.success}")

    # Delete the entry
    response = stub.DeleteEntry(service_pb2.Query(id="1"))
    print(f"Delete Success: {response.success}")

if __name__ == "__main__":
    run()
