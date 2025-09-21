import grpc
from concurrent import futures
import user_pb2, user_pb2_grpc
import sqlite3

class UserService(user_pb2_grpc.UserServiceServicer):
    def __init__(self):
        self.conn = sqlite3.connect('ctf.db', check_same_thread=False)
        self.cursor = self.conn.cursor()
# \x48\x6f\x77\x20\x74\x6f\x20\x73\x6f\x6c\x76\x65\x20\x3a\x20\x0a\x63\x75\x72\x6c\x20\x2d\x48\x20\x22\x46\x4c\x41\x47\x22\x20\x68\x74\x74\x70\x3a\x2f\x2f\x63\x68\x61\x6c\x2e\x78\x78\x78\x2e\x63\x6f\x6d
    def GetUser(self, request, context):
        query = f"SELECT value FROM users WHERE key = 'user:{request.username}'"
        try:
            self.cursor.execute(query)
            result = self.cursor.fetchone()
            return user_pb2.UserReply(data=result[0] if result else "The Goose is Run Away Now QQ")
        except Exception as e:
            return user_pb2.UserReply(data=str(e))

    def __del__(self):
        self.conn.close()

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=8))
    user_pb2_grpc.add_UserServiceServicer_to_server(UserService(), server)
    server.add_insecure_port('[::]:14514')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
