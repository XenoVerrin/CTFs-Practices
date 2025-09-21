#!/usr/bin/env python3
from flask import Flask, request, jsonify
import hashlib
import time
import secrets

app = Flask(__name__)

FLAG = "NHNC{YuMMyeeeE_GOOOd_ChAL_rIGHT}"
PORT = 80

SECRET_KEY = secrets.token_hex(32)


TOKEN_VALIDITY = 5

def generate_token():
    current_time = int(time.time())
    token_data = f"{current_time}:{SECRET_KEY}"
    token = hashlib.sha256(token_data.encode()).hexdigest()
    return token, current_time

def verify_token(token):
    current_time = int(time.time())
    

    for i in range(TOKEN_VALIDITY + 1):
        check_time = current_time - i
        token_data = f"{check_time}:{SECRET_KEY}"
        valid_token = hashlib.sha256(token_data.encode()).hexdigest()
        
        if token == valid_token:
            return True
    
    return False

@app.route("/token", methods=["GET"])
def get_token():
    token, timestamp = generate_token()
    return token

@app.route("/flag", methods=["POST"])
def get_flag():
    token = request.form.get('token')
    
    if not token:
        return "Token required", 401
    
    if not verify_token(token):
        return "Invalid token", 401
    
    return FLAG

@app.route("/", methods=["GET"])
def index():

    return "Meow"

@app.errorhandler(404)
def not_found(error):
    return "Not Found", 404

if __name__ == "__main__":
    print(f"[flag_server] listening on 0.0.0.0:{PORT}")
    app.run(host="0.0.0.0", port=PORT, debug=False)
