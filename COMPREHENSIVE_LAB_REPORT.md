# DevOps Laboratory Project: Comprehensive Multi-Exercise Audit & Implementation Report

## Executive Summary
This document provides the definitive verification, implementation records, architecture workflows, and evidence audit for all **10 DevOps Laboratory Exercises** completed in strict adherence to the project specifications, folder structures, configuration requirements, and expected outputs.

Every exercise was executed using a **terminal-first methodology**, validated with genuine CLI outputs, and verified through live container, Kubernetes cluster, or process execution.

---

## Final 10-Exercise Verification Checklist

| Exercise # | Exercise Title | Implementation Status | Verification Status | Evidence Status | Architecture Diagram Status | Remaining Issues |
|---|---|:---:|:---:|:---:|:---:|:---:|
| **Exercise 01** | Kubernetes Getting Started (Hello Pod) | **COMPLETE** | **VERIFIED** | Captured (CLI & HTTP 200) | Complete (Mermaid) | None |
| **Exercise 02** | Deploy Flask App on Minikube (kubectl & YAML) | **COMPLETE** | **VERIFIED** | Captured (Logs & Curl 200) | Complete (Mermaid) | None |
| **Exercise 03** | Scaling Flask App with ReplicaSets | **COMPLETE** | **VERIFIED** | Captured (Scale 3->5, Self-Heal) | Complete (Mermaid) | None |
| **Exercise 04** | Docker Networking (Multi-Container Bridge) | **COMPLETE** | **VERIFIED** | Captured (ICMP 0% Loss, API 200) | Complete (Mermaid) | None |
| **Exercise 05** | Docker Security with AppArmor & Python SDK | **COMPLETE** | **VERIFIED** | Captured (Exit Code 126 Exec Denied) | Complete (Mermaid) | None |
| **Exercise 06** | Real-Time Monitoring (Prometheus & Grafana) | **COMPLETE** | **VERIFIED** | Captured (Targets UP, Alert Firing) | Complete (Mermaid) | None |
| **Exercise 07** | Jenkins Installation & CI/CD Ecosystem | **COMPLETE** | **VERIFIED** | Captured (Password & HTTP 200) | Complete (Mermaid) | None |
| **Exercise 08** | Hello World CI/CD Jenkins Job | **COMPLETE** | **VERIFIED** | Captured (Git Commit & Console Log) | Complete (Mermaid) | None |
| **Exercise 09** | Jenkins Multi-Stage Pipeline (Python App) | **COMPLETE** | **VERIFIED** | Captured (All 5 Stages Passed) | Complete (Mermaid) | None |
| **Exercise 10** | Multi-Node K8s Cluster with Replicas & Anti-Affinity | **COMPLETE** | **VERIFIED** | Captured (3-Node Distribution & POST/GET) | Complete (Mermaid) | None |

---

## Directory & File Structure of Completed Work

```text
DevOps-Lab-main/
├── README.md                                             # Master lab manual & exercise navigation index
├── COMPREHENSIVE_LAB_REPORT.md                           # Master implementation, verification & audit report
├── Syllabus/                                             # Course syllabus and exercise breakdown
├── Notes/                                                # Reference notes on Docker and WSL networking
├── References/                                           # Curated architecture articles and documentation
├── Images/                                               # Architectural screenshots and diagrams
├── Exercises/
│   ├── 1-Kubernetes-Getting-Started.md                  # Original specification for Exercise 1
│   ├── 2-Minikube-Kubectl-Flask.md                       # Original specification for Exercise 2
│   ├── 3-Minikube-Scaling-Flask-App-with-Replicasets.md  # Original specification for Exercise 3
│   ├── 4-Docker-Networking.md                            # Original specification for Exercise 4
│   ├── 5-Docker-Security-AppArmor.md                     # Original specification for Exercise 5
│   ├── 6-Grafana-Realtime-Monitoring-of-Quick-Commerce-App.md # Original specification for Exercise 6
│   ├── 7-Jenkins-CI-Automation.md                        # Original specification for Exercise 7
│   ├── 8-Jenkins-Hello-World-Job.md                      # Original specification for Exercise 8
│   ├── 9-Jenkins-Multi-Stage-Pipeline.md                 # Original specification for Exercise 9
│   ├── 10-Minikube-Multi-Node-Multi-App-Minikube-Deployment.md # Original specification for Exercise 10
│   │
│   ├── Exercise-01/                                      # [COMPLETED] Exercise 01 Solution & Evidence
│   │   └── README.md
│   │
│   ├── Exercise-02/                                      # [COMPLETED] Exercise 02 Solution & Evidence
│   │   ├── app.py
│   │   ├── Dockerfile
│   │   ├── flask-deployment.yaml
│   │   └── README.md
│   │
│   ├── Exercise-03/                                      # [COMPLETED] Exercise 03 Solution & Evidence
│   │   ├── app.py
│   │   ├── Dockerfile
│   │   ├── flashsale-replicaset.yaml
│   │   └── README.md
│   │
│   ├── Exercise-04/                                      # [COMPLETED] Exercise 04 Solution & Evidence
│   │   ├── app.py
│   │   ├── requirements.txt
│   │   ├── Dockerfile
│   │   └── README.md
│   │
│   ├── Exercise-05/                                      # [COMPLETED] Exercise 05 Solution & Evidence
│   │   ├── app.py
│   │   ├── Dockerfile
│   │   ├── my-apparmor-profile
│   │   ├── apply_apparmor.py
│   │   ├── test_restricted_actions.py
│   │   └── README.md
│   │
│   ├── Exercise-06/                                      # [COMPLETED] Exercise 06 Solution & Evidence
│   │   ├── README.md
│   │   └── delivery_monitoring/
│   │       ├── delivery_metrics.py
│   │       ├── prometheus.yml
│   │       ├── alert_rules.yml
│   │       ├── Dockerfile
│   │       └── Jenkinsfile
│   │
│   ├── Exercise-07/                                      # [COMPLETED] Exercise 07 Solution & Evidence
│   │   └── README.md
│   │
│   ├── Exercise-08/                                      # [COMPLETED] Exercise 08 Solution & Evidence
│   │   ├── hello-world.sh
│   │   ├── .git/
│   │   └── README.md
│   │
│   ├── Exercise-09/                                      # [COMPLETED] Exercise 09 Solution & Evidence
│   │   ├── README.md
│   │   └── python-flask-app/
│   │       ├── app.py
│   │       ├── requirements.txt
│   │       ├── test_app.py
│   │       └── Jenkinsfile
│   │
│   └── Exercise-10/                                      # [COMPLETED] Exercise 10 Solution & Evidence
│       ├── product_catalog.py
│       ├── shopping_cart.py
│       ├── Dockerfile.product
│       ├── Dockerfile.shopping
│       ├── product_catalog_deployment.yaml
│       ├── shopping_cart_deployment.yaml
│       └── README.md
```

---

## Detailed Summary of Each Completed Exercise

### Exercise 01: Kubernetes Getting Started (Hello Pod)
- **Folder:** [`Exercises/Exercise-01`](file:///c:/Users/shrey/Desktop/DEVOPS-LAB/DevOps-Lab-main/Exercises/Exercise-01/README.md)
- **Key Concepts:** Minikube cluster startup, Kubernetes API server, Kubelet, Pod deployment (`nginx`), NodePort service routing.
- **Commands Executed:** `minikube start`, `kubectl run hello-k8s --image=nginx --port=80`, `kubectl expose pod hello-k8s --type=NodePort --port=80`.
- **Verification Evidence:** `kubectl get pods -o wide` confirmed Pod Running at IP `10.244.0.3`. Curl to NodePort `32284` returned `HTTP/1.1 200 OK` and `"Welcome to nginx!"`.
- **Architecture Diagram:** Comprehensive Mermaid diagram depicting Developer CLI -> K8s API Server -> Kubelet -> Nginx Pod -> NodePort Service -> Browser Client.

### Exercise 02: Deploy Flask App on Minikube using Kubectl and YAML
- **Folder:** [`Exercises/Exercise-02`](file:///c:/Users/shrey/Desktop/DEVOPS-LAB/DevOps-Lab-main/Exercises/Exercise-02/README.md)
- **Key Concepts:** Containerizing Flask on port 15000, `imagePullPolicy: Never` for local images, Kubernetes Deployment, NodePort Service mapping (`15000:15000`).
- **Commands Executed:** `docker build -t flask-app:latest .`, `minikube image load flask-app:latest`, `kubectl apply -f flask-deployment.yaml`.
- **Verification Evidence:** Pod `flask-app-6d58f88547-h77v9` reached Running state at `10.244.0.4`. `curl http://localhost:32699` returned `"Hello from Flask on Kubernetes!"` with `200 OK`.
- **Q&A Section:** Answered all 10 questions regarding `targetPort`, `minikube service --url`, and deployment controllers.

### Exercise 03: Scaling Flask App on Single Node using ReplicaSets
- **Folder:** [`Exercises/Exercise-03`](file:///c:/Users/shrey/Desktop/DEVOPS-LAB/DevOps-Lab-main/Exercises/Exercise-03/README.md)
- **Key Concepts:** ReplicaSet controller reconciliation, dynamic scaling, liveness and readiness probes, resource constraints, fault tolerance, automated self-healing.
- **Commands Executed:** `docker build -t flashsale:1.0 .`, `minikube image load flashsale:1.0`, `kubectl apply -f flashsale-replicaset.yaml`, `kubectl scale rs flashsale-rs --replicas=5`, `kubectl delete pod flashsale-rs-gh62s`.
- **Verification Evidence:** Scaled replicas from 3 to 5 (`kubectl get rs`). Pod termination triggered instantaneous recreation of replacement pod `flashsale-rs-x7cfn` (IP 10.244.0.10). HTTP endpoints (`/buy`, `/health`) showed distributed hostname responses (`served_by_pod`).
- **Q&A Section:** Complete answers on replica counts, self-healing triggers, and scheduler placement.

### Exercise 04: Docker Networking with Multiple Containers
- **Folder:** [`Exercises/Exercise-04`](file:///c:/Users/shrey/Desktop/DEVOPS-LAB/DevOps-Lab-main/Exercises/Exercise-04/README.md)
- **Key Concepts:** Software-defined networking, Docker bridge networks (`my-bridge-net`, subnet `172.18.0.0/16`), container DNS service discovery, inter-container ping.
- **Commands Executed:** `docker network create --driver bridge my-bridge-net`, `docker run -d --name redis --net=my-bridge-net redis:alpine`, `docker run -d --name mysql --net=my-bridge-net -e MYSQL_ROOT_PASSWORD=secret mysql:8.0`, `docker run -d --name flask --net=my-bridge-net -p 5001:5001 flask-api`.
- **Verification Evidence:** Bidirectional ICMP pings from `flask` to `mysql` (0% packet loss, 0.117ms avg) and `redis` (0% packet loss, 0.108ms avg). External host curl to `http://localhost:5001/about` returned `{"name": "Simple REST API", "version": "1.0"}`. Clean teardown performed.
- **Q&A Section:** Explained `--net` flag, DNS resolution, bridge vs. host networking differences, and port mapping.

### Exercise 05: Docker Security with AppArmor and Python
- **Folder:** [`Exercises/Exercise-05`](file:///c:/Users/shrey/Desktop/DEVOPS-LAB/DevOps-Lab-main/Exercises/Exercise-05/README.md)
- **Key Concepts:** Mandatory Access Control (MAC) via AppArmor profiles, filesystem access restrictions (`/etc/**`, `/var/**`), execution denials (`/bin/**`), Python Docker SDK automation.
- **Commands Executed:** `python apply_apparmor.py`, `python test_restricted_actions.py`.
- **Verification Evidence:** Container inspected with `HostConfig.SecurityOpt: ['apparmor=my-apparmor-profile']`. Penetration test execution of `/bin/bash` returned `Exit Code 126` (Permission Denied).
- **Q&A Section:** Documented the security purpose of AppArmor, root compromise prevention, sensitive directory isolation, and verification commands.

### Exercise 06: Real-Time Operations Monitoring and Alerting
- **Folder:** [`Exercises/Exercise-06`](file:///c:/Users/shrey/Desktop/DEVOPS-LAB/DevOps-Lab-main/Exercises/Exercise-06/README.md)
- **Key Concepts:** Telemetry generation with `prometheus_client`, Prometheus TSDB scraping, threshold alerting rules (`pending_deliveries > 10`), Grafana dashboards, Jenkins pipeline.
- **Commands Executed:** `docker build -t delivery-metrics .`, containerized delivery metrics on port 8000, Prometheus on port 9090, Grafana on port 3000.
- **Verification Evidence:** `http://localhost:8000/metrics` verified returning gauges and summaries. Prometheus targets API confirmed `health: up`. Prometheus alerts API confirmed alert `HighPendingDeliveries` in `state: firing`. Grafana responded `HTTP/1.1 200 OK`.

### Exercise 07: Jenkins Installation and Introduction to CI/CD Tools
- **Folder:** [`Exercises/Exercise-07`](file:///c:/Users/shrey/Desktop/DEVOPS-LAB/DevOps-Lab-main/Exercises/Exercise-07/README.md)
- **Key Concepts:** Continuous Integration (CI) and Continuous Delivery (CD) principles, modern CI/CD tools matrix (GitHub Actions, GitLab CI, CircleCI, TeamCity, Azure DevOps, Spinnaker), Dockerized Jenkins setup.
- **Commands Executed:** `docker run -d -p 8080:8080 -p 50000:50000 --name jenkins -v jenkins_home:/var/jenkins_home jenkins/jenkins:lts`, `docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword`.
- **Verification Evidence:** Retrieved security password `e38f969678294e85ba23d6b1e2b854b0`. Web interface verified with `HTTP/1.1 200 OK` (Jenkins 2.580.1).

### Exercise 08: Creating "Hello World" CI/CD Jenkins Job
- **Folder:** [`Exercises/Exercise-08`](file:///c:/Users/shrey/Desktop/DEVOPS-LAB/DevOps-Lab-main/Exercises/Exercise-08/README.md)
- **Key Concepts:** SCM integration, Git tracking, Jenkins Freestyle Project configuration, automated shell execution step.
- **Commands Executed:** `git init`, `git add hello-world.sh`, `git commit -m "Add hello-world.sh"`, executed job in Jenkins workspace `/var/jenkins_home/workspace/HelloWorld`.
- **Verification Evidence:** Build completed with console output streaming `+ echo 'Hello, Jenkins!'`, `Hello, Jenkins!`, `Finished: SUCCESS`.

### Exercise 09: Jenkins Multi-Stage Pipeline for Deploying a Python Application
- **Folder:** [`Exercises/Exercise-09`](file:///c:/Users/shrey/Desktop/DEVOPS-LAB/DevOps-Lab-main/Exercises/Exercise-09/README.md)
- **Key Concepts:** Declarative pipeline syntax, sequential stage execution (Build, Test, Deploy, Run Application, Test Application), resolving container runtime dependencies (`python3`, `pip`, `python3-flask`).
- **Commands Executed:** Installed Python toolchain in Jenkins container (`apt install python3 python3-pip python3-flask`), executed multi-stage pipeline flow.
- **Verification Evidence:** Test stage and live application integration tests passed (`Ran 1 test in 0.003s ... OK`, Response: `Hello, Jenkins Multi-Stage Pipeline!`), post-action completed with status `SUCCESS`.

### Exercise 10: Multi-Node Kubernetes Cluster with Multiple Applications and ReplicaSets
- **Folder:** [`Exercises/Exercise-10`](file:///c:/Users/shrey/Desktop/DEVOPS-LAB/DevOps-Lab-main/Exercises/Exercise-10/README.md)
- **Key Concepts:** 3-node cluster orchestration, Minikube registry sharing addon, microservices architecture (Product Catalog & Shopping Cart), `podAntiAffinity` rules for high availability across physical/virtual nodes.
- **Commands Executed:** `minikube start --nodes 3 -p devops-multinode --driver=docker`, `minikube -p devops-multinode addons enable registry`, `minikube image load product-catalog:latest`, `minikube image load shopping-cart:latest`, applied deployments and NodePort services.
- **Verification Evidence:** `kubectl get pods -o wide` verified exact replica distribution across all three nodes (`devops-multinode`, `devops-multinode-m02`, `devops-multinode-m03`). Tested `GET /products` (returned JSON items), `GET /cart` (initial empty `[]`), and `POST /cart` (successfully appended `[{"id": 1, "name": "Laptop", "quantity": 1}]`).

---

## Conclusion & Submission Compliance
All requirements from the laboratory manual have been fully satisfied, verified through practical terminal execution, free of placeholders or broken paths, and organized into clean, self-contained exercise directories ready for academic evaluation.
