#!/usr/bin/env python3
import grpc
from concurrent import futures
import requests
from urllib.parse import urlparse

import fetch_pb2, fetch_pb2_grpc

TIMEOUT = 3
ALLOWED_HOSTS = {"localhost", "127.0.0.1"}

class FetchService(fetch_pb2_grpc.FetchServiceServicer):
    def FetchURL(self, request, context):
        url = request.url.strip()
        method = request.method.upper() if request.method else "GET"
        body = request.body if request.body else None
        headers = dict(request.headers) if request.headers else {}

        parsed = urlparse(url)

        if parsed.scheme not in ("http", "https"):
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, "Only http(s) allowed Qwq")

        if parsed.hostname not in ALLOWED_HOSTS:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT,
                          f"Only localhost adallowed QwQ")

        try:
            resp = requests.request(method, url, data=body, headers=headers, timeout=TIMEOUT)
            resp.raise_for_status()
            return fetch_pb2.FetchResponse(content=resp.text[:4096])
        except Exception as e:
            context.abort(grpc.StatusCode.INTERNAL, f"Fetch failed: {e}")

def serve() -> None:
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
    fetch_pb2_grpc.add_FetchServiceServicer_to_server(FetchService(), server)
    server.add_insecure_port("[::]:6666")
    server.start()
    print("[gRPC] listening on :6666")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
