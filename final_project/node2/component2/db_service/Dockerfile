FROM python:3.13

WORKDIR /app

RUN pip install --no-cache-dir \
    grpcio \
    grpcio-tools \
    kafka-python \
    pymongo

COPY service.proto .
COPY db_service.py .

RUN python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. service.proto

CMD ["python", "db_service.py"]
