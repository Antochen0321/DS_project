from concurrent import futures
import grpc
import pymongo
import service_pb2
import service_pb2_grpc

class DatabaseService(service_pb2_grpc.DatabaseServiceServicer):
    def __init__(self, db_url="mongodb://mongodb:27017", db_name="mydb"):
        self.client = pymongo.MongoClient(db_url)
        self.db = self.client[db_name]
        self.collection = self.db["entries"]

    def CreateEntry(self, request, context):
        entry = {"_id": request.id, "data": request.data}
        self.collection.insert_one(entry)
        return service_pb2.Response(success=True)

    def ReadEntry(self, request, context):
        entry = self.collection.find_one({"_id": request.id})
        if entry:
            return service_pb2.Entry(id=entry["_id"], data=entry["data"])
        return service_pb2.Entry(id="", data="")

    def UpdateEntry(self, request, context):
        updated = self.collection.update_one({"_id": request.id}, {"$set": {"data": request.data}})
        return service_pb2.Response(success=updated.modified_count > 0)

    def DeleteEntry(self, request, context):
        deleted = self.collection.delete_one({"_id": request.id})
        return service_pb2.Response(success=deleted.deleted_count > 0)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    service_pb2_grpc.add_DatabaseServiceServicer_to_server(DatabaseService(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
