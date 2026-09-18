# Exercise 03: Scaling Flask App on Single Node using ReplicaSets

## 1. Title & Overview
**Exercise 03: Implementing High Availability and Dynamic Pod Autoscaling with Kubernetes ReplicaSets (E-commerce Flash Sale Scenario)**  
This exercise simulates an e-commerce flash sale scenario (e.g., Big Billion Days / Prime Day) where sudden request spikes require dynamic application scaling from 3 to 5 pods, resilient self-healing upon pod deletion, and distributed request processing.

---

## 2. Objective
- Understand Kubernetes ReplicaSets, Pod controllers, and pod lifecycle management.
- Containerize a high-throughput Flask ordering application running on Gunicorn WSGI.
- Define a declarative `ReplicaSet` manifest with liveness probes, readiness probes, and CPU/memory resource limits.
- Scale the ReplicaSet horizontally using `kubectl scale rs --replicas=5`.
- Validate automated self-healing by terminating a pod and verifying instantaneous replacement by the controller.
- Observe load distribution across distinct pods via the `/buy` and `/health` endpoints.

---

## 3. Requirements & Prerequisites
- **Local Cluster:** Minikube v1.38+ (Docker driver)
- **Container Runtime:** Docker Desktop 29.7+
- **Kubernetes CLI:** `kubectl` v1.36+
- **Application Stack:** Python 3.11, Flask, Gunicorn

---

## 4. Tools Used
| Tool | Version | Role in Architecture |
|---|---|---|
| **Python / Flask** | 3.11 / 3.1.3 | Flash sale order placement microservice |
| **Gunicorn** | 26.2.0 | Production-grade WSGI HTTP server |
| **Docker** | 29.7.2 | Container build engine creating `flashsale:1.0` |
| **Kubernetes ReplicaSet** | apps/v1 | Controller maintaining the exact desired replica count |
| **Kubectl** | v1.36.4 | Scaling, inspection, and cluster management CLI |

---

## 5. Architecture & Workflow Diagram

```mermaid
graph TD
    subgraph Client Traffic & Ingress
        Client["Simulated Shoppers / Flash Sale Traffic"] -->|Checkout Requests /buy| Service["ClusterIP Service: flashsale-svc\nPort: 80 -> TargetPort: 5000"]
    end

    subgraph Kubernetes Node ["Minikube Single Node Cluster"]
        RSController["K8s ReplicaSet Controller\n(Desired: 5 | Current: 5 | Ready: 5)"] -->|Watches & Reconciles State| RS["ReplicaSet: flashsale-rs"]
        
        RS -->|Replica 1| Pod1["Pod: flashsale-rs-k5rh8\nIP: 10.244.0.6"]
        RS -->|Replica 2| Pod2["Pod: flashsale-rs-rqfqg\nIP: 10.244.0.9"]
        RS -->|Replica 3| Pod3["Pod: flashsale-rs-tdqs4\nIP: 10.244.0.8"]
        RS -->|Replica 4 (Self-Healed)| Pod4["Pod: flashsale-rs-x7cfn\nIP: 10.244.0.10"]
        RS -->|Replica 5| Pod5["Pod: flashsale-rs-zdn2p\nIP: 10.244.0.7"]

        Service -->|Round Robin Load Balancing| Pod1
        Service -->|Round Robin Load Balancing| Pod2
        Service -->|Round Robin Load Balancing| Pod3
        Service -->|Round Robin Load Balancing| Pod4
        Service -->|Round Robin Load Balancing| Pod5

        subgraph Self Healing Trigger
            DeletedPod["Pod: flashsale-rs-gh62s (Terminated)"] -.->|State Discrepancy Detected| RSController
            RSController -.->|Spawns Replacement Pod| Pod4
        end
    end

    classDef traffic fill:#1e40af,stroke:#1e3a8a,stroke-width:2px,color:#fff;
    classDef control fill:#065f46,stroke:#047857,stroke-width:2px,color:#fff;
    classDef pod fill:#d97706,stroke:#b45309,stroke-width:2px,color:#fff;
    classDef alert fill:#b91c1c,stroke:#991b1b,stroke-width:2px,color:#fff;
    class Client,Service traffic;
    class RSController,RS control;
    class Pod1,Pod2,Pod3,Pod4,Pod5 pod;
    class DeletedPod alert;
```

---

## 6. Implementation & Configuration Files

### File: `app.py`
```python
from flask import Flask, request
import socket, time, random

app = Flask(__name__)

@app.get("/")
def homepage():
    return {
        "message": "Welcome to Big Sale!",
        "pod": socket.gethostname(),
        "ts": time.time()
    }

@app.get("/buy")
def buy():
    item = random.choice(["Smartphone", "Shoes", "Headphones", "Laptop"])
    user = request.args.get("user", f"user{random.randint(1,1000)}")
    return {
        "status": "success",
        "item": item,
        "user": user,
        "served_by_pod": socket.gethostname(),
        "time": time.strftime("%H:%M:%S")
    }

@app.get("/health")
def health():
    return {"status": "healthy", "pod": socket.gethostname()}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
```

### File: `Dockerfile`
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY app.py .
RUN pip install --no-cache-dir flask gunicorn
EXPOSE 5000
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app", "--workers", "1", "--threads", "2"]
```

### File: `flashsale-replicaset.yaml`
```yaml
apiVersion: apps/v1
kind: ReplicaSet
metadata:
  name: flashsale-rs
  labels:
    app: flashsale
spec:
  replicas: 3
  selector:
    matchLabels:
      app: flashsale
  template:
    metadata:
      labels:
        app: flashsale
    spec:
      containers:
      - name: flashsale-container
        image: flashsale:1.0
        imagePullPolicy: Never
        ports:
        - containerPort: 5000
        readinessProbe:
          httpGet:
            path: /health
            port: 5000
          initialDelaySeconds: 2
          periodSeconds: 5
        livenessProbe:
          httpGet:
            path: /health
            port: 5000
          initialDelaySeconds: 10
          periodSeconds: 10
        resources:
          requests:
            cpu: "100m"
            memory: "128Mi"
          limits:
            cpu: "500m"
            memory: "256Mi"
---
apiVersion: v1
kind: Service
metadata:
  name: flashsale-svc
spec:
  selector:
    app: flashsale
  ports:
  - name: http
    port: 80
    targetPort: 5000
  type: ClusterIP
```

---

## 7. Terminal Commands Executed & Actual Outputs

### 1. Build and Load Image
```powershell
docker build -t flashsale:1.0 .
minikube image load flashsale:1.0
```
**Output:** Image built and cached into Minikube VM with exit code 0.

### 2. Apply ReplicaSet Manifest
```powershell
kubectl apply -f flashsale-replicaset.yaml
```
**Output:**
```text
replicaset.apps/flashsale-rs created
service/flashsale-svc created
```

### 3. Verify Initial 3 Replicas
```powershell
kubectl get rs
kubectl get pods -l app=flashsale -o wide
```
**Output:**
```text
NAME           DESIRED   CURRENT   READY   AGE
flashsale-rs   3         3         3       42s

NAME                 READY   STATUS    RESTARTS   AGE   IP           NODE       NOMINATED NODE   READINESS GATES
flashsale-rs-gh62s   1/1     Running   0          42s   10.244.0.5   minikube   <none>           <none>
flashsale-rs-k5rh8   1/1     Running   0          42s   10.244.0.6   minikube   <none>           <none>
flashsale-rs-zdn2p   1/1     Running   0          42s   10.244.0.7   minikube   <none>           <none>
```

### 4. Scale Out to 5 Replicas
```powershell
kubectl scale rs flashsale-rs --replicas=5
```
**Output:**
```text
replicaset.apps/flashsale-rs scaled
```

### 5. Verify Scaled Replicas
```powershell
kubectl get rs flashsale-rs
kubectl get pods -l app=flashsale -o wide
```
**Output:**
```text
NAME           DESIRED   CURRENT   READY   AGE
flashsale-rs   5         5         5       104s

NAME                 READY   STATUS    RESTARTS   AGE    IP           NODE       NOMINATED NODE   READINESS GATES
flashsale-rs-gh62s   1/1     Running   0          104s   10.244.0.5   minikube   <none>           <none>
flashsale-rs-k5rh8   1/1     Running   0          104s   10.244.0.6   minikube   <none>           <none>
flashsale-rs-rqfqg   1/1     Running   0          7s     10.244.0.9   minikube   <none>           <none>
flashsale-rs-tdqs4   1/1     Running   0          7s     10.244.0.8   minikube   <none>           <none>
flashsale-rs-zdn2p   1/1     Running   0          104s   10.244.0.7   minikube   <none>           <none>
```

### 6. Test Self-Healing (Delete Pod `flashsale-rs-gh62s`)
```powershell
kubectl delete pod flashsale-rs-gh62s
```
**Output:**
```text
pod "flashsale-rs-gh62s" deleted from default namespace
```

### 7. Verify Automatic Pod Replacement
```powershell
kubectl get pods -l app=flashsale -o wide
```
**Output:**
```text
NAME                 READY   STATUS    RESTARTS   AGE     IP            NODE       NOMINATED NODE   READINESS GATES
flashsale-rs-k5rh8   1/1     Running   0          4m33s   10.244.0.6    minikube   <none>           <none>
flashsale-rs-rqfqg   1/1     Running   0          2m56s   10.244.0.9    minikube   <none>           <none>
flashsale-rs-tdqs4   1/1     Running   0          2m56s   10.244.0.8    minikube   <none>           <none>
flashsale-rs-x7cfn   1/1     Running   0          2m13s   10.244.0.10   minikube   <none>           <none>
flashsale-rs-zdn2p   1/1     Running   0          4m33s   10.244.0.7    minikube   <none>           <none>
```
*Note: Controller immediately provisioned replacement pod `flashsale-rs-x7cfn` (IP 10.244.0.10) to maintain desired count of 5.*

---

## 8. Verification & Testing Evidence

### Microservice Endpoint Testing across Replicas:
```bash
minikube ssh "curl -s http://10.244.0.6:5000/buy; echo ''; curl -s http://10.244.0.8:5000/buy; echo ''; curl -s http://10.244.0.10:5000/health"
```
**Output:**
```json
{"item":"Smartphone","served_by_pod":"flashsale-rs-k5rh8","status":"success","time":"12:07:22","user":"user327"}
{"item":"Laptop","served_by_pod":"flashsale-rs-tdqs4","status":"success","time":"12:07:22","user":"user255"}
{"pod":"flashsale-rs-x7cfn","status":"healthy"}
```

---

## 9. Conceptual Questions & Answers (from Lab Manual)

- **Q1: What is the initial number of replicas in the ReplicaSet?**  
  *Answer:* 3 replicas.
- **Q2: How many pods are running after applying the ReplicaSet configuration?**  
  *Answer:* Exactly 3 pods (`flashsale-rs-gh62s`, `flashsale-rs-k5rh8`, `flashsale-rs-zdn2p`).
- **Q3: What happens when you scale the ReplicaSet to 5 replicas?**  
  *Answer:* The Kubernetes ReplicaSet controller detects the discrepancy between desired state (5) and current state (3) and immediately provisions 2 additional pods (`flashsale-rs-rqfqg` and `flashsale-rs-tdqs4`).
- **Q4: What happens when you delete one pod?**  
  *Answer:* Kubernetes automatically initiates self-healing by detecting the reduction in active pods and scheduling a brand new replacement pod (`flashsale-rs-x7cfn`) to restore the desired count of 5.
- **Q5: How does Kubernetes maintain the desired number of replicas?**  
  *Answer:* Through the continuous reconciliation loop running inside `kube-controller-manager`, which compares the live cluster state against the manifest's desired state.
- **Q6: How many nodes are running?**  
  *Answer:* 1 single control-plane node (`minikube`).
- **Q7: Where are the pods running with respect to nodes?**  
  *Answer:* All 5 pods are colocated and distributed across the single `minikube` node.

---

## 10. Result & Conclusion
- Successfully deployed a scalable, multi-threaded Gunicorn Flask microservice.
- Verified horizontal pod autoscaling from 3 to 5 replicas on-demand.
- Proved Kubernetes fault tolerance and automated self-healing mechanisms upon pod deletion.
- Validated individual pod load distribution and health probes with zero failures.
