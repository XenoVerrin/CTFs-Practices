FROM python:3.11-slim
RUN apt-get update && \
    apt-get install -y gcc git && \
    pip install --no-cache-dir grpcio grpcio-tools

WORKDIR /app
COPY . /app

RUN python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. user.proto

CMD ["python", "server.py"]
