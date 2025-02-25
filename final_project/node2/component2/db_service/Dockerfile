FROM python:3.13

WORKDIR /app

COPY service.proto .
COPY db_service.py .
COPY requirements.txt .

RUN pip install -r requirements.txt && \
    python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. service.proto

CMD ["python", "db_service.py"]
