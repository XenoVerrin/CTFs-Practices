FROM python:3.11-slim AS build

WORKDIR /app
COPY proto/ proto/
COPY server/ server/

RUN pip install --no-cache-dir -r server/requirements.txt \
 && python -m grpc_tools.protoc \
      -I proto \
      --python_out=server \
      --grpc_python_out=server \
      proto/fetch.proto


FROM python:3.11-slim
WORKDIR /app

COPY --from=build /app/server /app/server
RUN pip install --no-cache-dir -r server/requirements.txt
CMD ["sh", "-c", "python server/flag_server.py & python server/server.py"]
