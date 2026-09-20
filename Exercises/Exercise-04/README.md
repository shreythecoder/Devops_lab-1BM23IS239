# Exercise 04: Docker Networking with Multiple Containers

## 1. Title & Overview
**Exercise 04: Designing, Configuring, and Validating Multi-Container Inter-Communication via Custom Docker Bridge Networks**  
This exercise demonstrates multi-container networking concepts using Docker. A custom user-defined bridge network (`my-bridge-net`) is provisioned to interconnect a Python Flask REST API, a MySQL relational database container, and a Redis in-memory cache container. Automatic DNS name resolution and port isolation are verified.

---

## 2. Objective
- Understand Docker networking drivers (`bridge`, `host`, `none`, `overlay`, `macvlan`).
- Create and inspect a custom user-defined bridge network with dedicated subnet and gateway.
- Build and containerize a Python Flask REST API with ICMP networking tools.
- Run multi-tier microservices (`flask`, `mysql`, `redis`) attached to the custom bridge network.
- Test inter-container DNS name resolution and bidirectional ICMP connectivity (`ping mysql`, `ping redis`).
- Expose application endpoints to the host (`-p 5001:5001`) and test REST API responses (`/about`).
- Implement clean teardown procedures and document conceptual questions.

---

## 3. Requirements & Prerequisites
- **Operating System:** Windows 11 with WSL2 / PowerShell
- **Container Runtime:** Docker Desktop 29.7+
- **Network Driver:** Docker Bridge (`my-bridge-net`)
- **Containers Deployed:** `flask-api:latest`, `mysql:8.0`, `redis:alpine`

---

## 4. Tools Used
| Tool | Version | Role in Architecture |
|---|---|---|
| **Docker Engine** | 29.7.2 | Container runtime and software-defined network management |
| **Python / Flask** | 3.9 / 3.1.3 | REST API service exposing `/about` on port 5001 |
| **MySQL** | 8.0 | Relational database container on network port 3306 |
| **Redis** | Alpine / Latest | In-memory key-value cache on port 6379 |
| **iputils-ping / curl** | Debian / Latest | Network diagnostic tools inside container |

---

## 5. Architecture & Workflow Diagram

```mermaid
graph TD
    subgraph Host Machine ["Host Operating System (Windows / Docker Host)"]
        CurlHost["Host Curl / Client"] -->|Port Forwarding: 5001:5001| FlaskContainer
        DockerDaemon["Docker Daemon / Embedded DNS (127.0.0.11)"]
    end

    subgraph User-Defined Bridge Network ["Docker Bridge Network: my-bridge-net (Subnet: 172.18.0.0/16 | Gateway: 172.18.0.1)"]
        subgraph Container1 ["Flask Web Server (Container: flask)"]
            FlaskContainer["App: Flask REST API (app.py)\nIP: 172.18.0.4\nPort: 5001"]
        end

        subgraph Container2 ["Relational Database (Container: mysql)"]
            MySQLContainer["Service: MySQL Database 8.0\nIP: 172.18.0.3\nPort: 3306"]
        end

        subgraph Container3 ["In-Memory Cache (Container: redis)"]
            RedisContainer["Service: Redis Key-Value Cache\nIP: 172.18.0.2\nPort: 6379"]
        end

        FlaskContainer -->|ICMP Ping / DNS Resolution: mysql| MySQLContainer
        FlaskContainer -->|ICMP Ping / DNS Resolution: redis| RedisContainer
        DockerDaemon -.->|Provides Automatic Service Discovery| User-Defined Bridge Network
    end

    classDef host fill:#1e40af,stroke:#1e3a8a,stroke-width:2px,color:#fff;
    classDef network fill:#065f46,stroke:#047857,stroke-width:2px,color:#fff;
    classDef container fill:#d97706,stroke:#b45309,stroke-width:2px,color:#fff;
    class CurlHost,DockerDaemon host;
    class User-Defined Bridge Network network;
    class FlaskContainer,MySQLContainer,RedisContainer container;
```

---

## 6. Implementation & Code Details

### File: `app.py`
```python
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/about', methods=['GET'])
def about():
    return jsonify({
        "name": "Simple REST API",
        "version": "1.0",
        "description": "This is a simple REST API built with Flask."
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
```

### File: `requirements.txt`
```text
Flask>=2.0.1
```

### File: `Dockerfile`
```dockerfile
FROM python:3.9-slim
WORKDIR /app
RUN apt-get update && apt-get install -y iputils-ping curl && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
COPY app.py .
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5001
CMD ["python", "app.py"]
```

---

## 7. Terminal Commands Executed & Actual Outputs

### Task 1: Create Custom Bridge Network
```powershell
docker network create --driver bridge my-bridge-net
```
**Output:**
```text
ccea177e95992462d2b9e1c3f388ea5e179ba5669990d3b0111404309b8f5a19
```

### Task 2: Verify Network Creation
```powershell
docker network ls
```
**Output:**
```text
NETWORK ID     NAME            DRIVER    SCOPE
078f74b83482   bridge          bridge    local
ce83c81a9b44   host            host      local
41dc2535ba24   minikube        bridge    local
ccea177e9599   my-bridge-net   bridge    local
2274e393e1c9   none            null      local
```

### Task 3: Inspect Network Subnet & Gateway
```powershell
docker network inspect my-bridge-net
```
**Key Attributes:**
- **Subnet:** `172.18.0.0/16`
- **Gateway:** `172.18.0.1`
- **Driver:** `bridge`
- **Scope:** `local`

### Task 4: Build Flask App Image
```powershell
docker build -t flask-api .
```
**Output:** Successfully built and tagged `flask-api:latest`.

### Task 5: Launch Multi-Tier Containers
```powershell
docker run -d --name redis --net=my-bridge-net redis:alpine
docker run -d --name mysql --net=my-bridge-net -e MYSQL_ROOT_PASSWORD=mysecretpassword -e MYSQL_DATABASE=testdb mysql:8.0
docker run -d --name flask --net=my-bridge-net -p 5001:5001 flask-api
```
**Verification (`docker ps`):**
```text
CONTAINER ID   IMAGE          COMMAND                  STATUS          PORTS                    NAMES
5fecd4b61595   flask-api      "python app.py"          Up 28 seconds   0.0.0.0:5001->5001/tcp   flask
3100586ae088   mysql:8.0      "docker-entrypoint.s…"   Up 28 seconds   3306/tcp, 33060/tcp      mysql
cc68660260cf   redis:alpine   "docker-entrypoint.s…"   Up 47 seconds   6379/tcp                 redis
```

---

## 8. Verification & Connectivity Testing Evidence

### 1. Inter-Container Ping from `flask` to `mysql`:
```bash
docker exec flask ping -c 3 mysql
```
**Actual Output:**
```text
PING mysql (172.18.0.3) 56(84) bytes of data.
64 bytes from mysql.my-bridge-net (172.18.0.3): icmp_seq=1 ttl=64 time=0.167 ms
64 bytes from mysql.my-bridge-net (172.18.0.3): icmp_seq=2 ttl=64 time=0.118 ms
64 bytes from mysql.my-bridge-net (172.18.0.3): icmp_seq=3 ttl=64 time=0.067 ms

--- mysql ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2046ms
rtt min/avg/max/mdev = 0.067/0.117/0.167/0.040 ms
```

### 2. Inter-Container Ping from `flask` to `redis`:
```bash
docker exec flask ping -c 3 redis
```
**Actual Output:**
```text
PING redis (172.18.0.2) 56(84) bytes of data.
64 bytes from redis.my-bridge-net (172.18.0.2): icmp_seq=1 ttl=64 time=0.188 ms
64 bytes from redis.my-bridge-net (172.18.0.2): icmp_seq=2 ttl=64 time=0.060 ms
64 bytes from redis.my-bridge-net (172.18.0.2): icmp_seq=3 ttl=64 time=0.077 ms

--- redis ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2047ms
rtt min/avg/max/mdev = 0.060/0.108/0.188/0.056 ms
```

### 3. External HTTP Request to Flask REST API:
```powershell
curl.exe -i http://localhost:5001/about
```
**Actual Output:**
```text
HTTP/1.1 200 OK
Server: Werkzeug/3.1.9 Python/3.9.25
Date: Sun, 18 Oct 2026 12:11:26 GMT
Content-Type: application/json
Content-Length: 103
Connection: close

{"description":"This is a simple REST API built with Flask.","name":"Simple REST API","version":"1.0"}
```

### Task 6: Cleanup Commands & Execution
```powershell
docker stop mysql redis flask
docker rm mysql redis flask
docker network rm my-bridge-net
```
**Output:** Cleanly removed all containers and custom network.

---

## 9. Conceptual Questions & Answers (from Lab Manual)

- **Q1: What is the purpose of the `--net` flag in `docker run`?**  
  *Answer:* The `--net` (or `--network`) flag attaches the newly created container to a specific Docker network, placing it within the network's IP subnet and enabling access to Docker's embedded DNS server.
- **Q2: How do containers communicate with each other on the same network?**  
  *Answer:* On user-defined bridge networks, containers resolve peer IP addresses automatically using container names or network aliases via Docker's built-in DNS service (`127.0.0.11`), communicating over standard TCP/UDP ports.
- **Q3: What is the difference between a bridge network and a host network?**  
  *Answer:*  
  - *Bridge Network:* Provides an isolated virtual network namespace and private subnet (`172.18.0.0/16`) for containers, requiring explicit port mapping (`-p`) to reach host ports.  
  - *Host Network:* Removes network isolation, binding the container directly to the host's physical network stack and interfaces without NAT translation.
- **Q4: How can you expose a container's port to the host machine?**  
  *Answer:* By passing the `-p` or `--publish` flag during `docker run` (e.g., `-p 5001:5001`), which creates an iptables/NAT port-forwarding rule mapping host port 5001 to container port 5001.

---

## 10. Result & Conclusion
- Successfully constructed a dedicated user-defined Docker bridge network.
- Successfully verified DNS-based container-to-container name resolution between Flask, MySQL, and Redis with 0% packet loss.
- Validated external host port forwarding serving JSON responses from the REST API.
- Executed clean resource teardown without lingering containers or orphan networks.
