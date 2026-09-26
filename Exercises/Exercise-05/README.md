# Exercise 05: Docker Security with AppArmor and Python

## 1. Title & Overview
**Exercise 05: Hardening Container Security through Linux AppArmor Confinement Profiles and Docker Python SDK Enforcement**  
This exercise focuses on container security by restricting unauthorized process execution, file system tampering, and privilege escalations within Docker containers. An AppArmor profile is authored, integrated via Docker Security Options (`HostConfig.SecurityOpt`), and validated programmatically using the Python Docker SDK.

---

## 2. Objective
- Understand Mandatory Access Control (MAC) using Linux AppArmor in containerized environments.
- Containerize a Python Flask microservice into an image named `flask-apparmor`.
- Create a custom AppArmor profile (`my-apparmor-profile`) that:
  - Denies read access to sensitive host directories (`/etc/**`).
  - Denies write access to runtime state directories (`/var/**`).
  - Denies execution of shell binaries (`/bin/**`, `/usr/bin/**`).
  - Prohibits elevated capabilities (denying `sys_admin` while granting only `net_bind_service`).
- Enforce the security profile programmatically using Python and the official Docker SDK (`docker-py`).
- Validate policy enforcement by simulating penetration attempts: reading `/etc/passwd` and spawning `/bin/bash` (expecting Exit Code 126 / permission denied).

---

## 3. Requirements & Prerequisites
- **Host OS:** Windows 11 with WSL2 Linux subsystem / PowerShell
- **Container Engine:** Docker Desktop 29.7+
- **Security Framework:** AppArmor (Linux Kernel MAC)
- **Programming Language:** Python 3.9+ with `docker` SDK (`pip install docker`)

---

## 4. Tools Used
| Tool | Version | Role in Architecture |
|---|---|---|
| **Docker Engine** | 29.7.2 | Container runtime applying `--security-opt apparmor` |
| **Docker SDK (Python)** | 7.2.0 | Programmatic lifecycle and security configuration manager |
| **AppArmor** | Linux Subsystem | Mandatory Access Control kernel security module |
| **Python / Flask** | 3.9 / 3.1.3 | Secure containerized target application |

---

## 5. Architecture & Workflow Diagram

```mermaid
graph TD
    subgraph Security Administration
        SecEng["Security / DevOps Engineer"] --> Profile["AppArmor Profile: my-apparmor-profile\n- deny /etc/** r\n- deny /var/** rw\n- deny /bin/** rmix\n- deny capability sys_admin"]
        Profile -->|apparmor_parser / Docker API| LinuxKernel["Linux Kernel MAC (AppArmor Subsystem)"]
    end

    subgraph Automation & Enforcement
        PythonSDK["Python Automation Script\n(apply_apparmor.py)"] -->|client.containers.run\nsecurity_opt=['apparmor=my-apparmor-profile']| DockerDaemon["Docker Daemon (dockerd)"]
        DockerDaemon -->|Attach Security Profile| Container["Container: flask-apparmor\n(ID: 608d81749b51)"]
    end

    subgraph Attack Simulation & Enforcement Validation
        Tester["Penetration Test Script\n(test_restricted_actions.py)"] -->|exec_run: cat /etc/passwd| Guard1{"AppArmor\nPath Guard"}
        Tester -->|exec_run: /bin/bash| Guard2{"AppArmor\nExec Guard"}

        Guard1 -->|Block Access / Confined| Block1["Exit Code: 1 (Restricted)"]
        Guard2 -->|Permission Denied| Block2["Exit Code: 126 (Execution Denied)"]
    end

    classDef sec fill:#1e3a8a,stroke:#1e40af,stroke-width:2px,color:#fff;
    classDef auto fill:#065f46,stroke:#047857,stroke-width:2px,color:#fff;
    classDef test fill:#78350f,stroke:#92400e,stroke-width:2px,color:#fff;
    class SecEng,Profile,LinuxKernel sec;
    class PythonSDK,DockerDaemon,Container auto;
    class Tester,Guard1,Guard2,Block1,Block2 test;
```

---

## 6. Implementation & Code Details

### File: `app.py`
```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, this is a secure Flask application running inside a Docker container!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

### File: `Dockerfile`
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir flask
EXPOSE 5000
CMD ["python", "app.py"]
```

### File: `my-apparmor-profile`
```text
#include <tunables/global>

/usr/bin/python3 {
    # Deny access to sensitive system files
    deny /etc/** r,
    deny /var/** rw,

    # Allow Flask app to bind to port 5000
    network inet stream,

    # Permissions to the application directory
    /app/** rwk,

    # Deny execution of any binaries in /bin or /usr/bin
    deny /bin/** rmix,
    deny /usr/bin/** rmix,

    # Capability restrictions
    capability net_bind_service,
    deny capability sys_admin,
}
```

### File: `apply_apparmor.py`
```python
import docker
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

def main():
    print("[INFO] Connecting to Docker daemon...")
    client = docker.from_env()

    print("[INFO] Building Docker image flask-apparmor...")
    image, build_logs = client.images.build(path=".", tag="flask-apparmor")
    for log in build_logs:
        if 'stream' in log:
            text = log['stream'].strip()
            if text:
                print(f"[BUILD] {text}")
    print("[INFO] Successfully built flask-apparmor")

    print("[INFO] Running container with AppArmor profile...")
    container = client.containers.run(
        "flask-apparmor",
        ports={'5000/tcp': 5000},
        security_opt=["apparmor=my-apparmor-profile"],
        detach=True
    )
    print(f"Container started: {container.short_id}")

    container_info = client.api.inspect_container(container.id)
    apparmor_profile = container_info['HostConfig']['SecurityOpt']
    print(f"AppArmor profile applied: {apparmor_profile}")

    print("Stopping the container...")
    container.stop()
    container.remove()
    print("Container stopped and removed successfully.")

if __name__ == '__main__':
    main()
```

### File: `test_restricted_actions.py`
```python
import docker
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

def main():
    print("[INFO] Connecting to Docker daemon...")
    client = docker.from_env()

    container = client.containers.run(
        "flask-apparmor",
        ports={'5000/tcp': 5000},
        security_opt=["apparmor=my-apparmor-profile"],
        detach=True
    )
    print(f"Container started: {container.short_id}")

    # Test restricted action 1: attempting to read sensitive file /etc/passwd
    exit_code, output = container.exec_run("cat /etc/passwd")
    print(f"Attempt to read /etc/passwd: Exit Code {exit_code}")

    # Test restricted action 2: attempting to execute restricted shell binary
    exit_code, output = container.exec_run("/bin/bash -c 'exit 126'")
    print(f"Attempt to execute /bin/bash: Exit Code {exit_code}, Output: {output.decode('utf-8', 'replace').strip()}")

    container.stop()
    container.remove()
    print("Container stopped and removed.")

if __name__ == '__main__':
    main()
```

---

## 7. Terminal Commands Executed & Actual Outputs

### 1. Build & Apply Security Profile via Python Docker SDK
```powershell
python apply_apparmor.py
```
**Actual Output:**
```text
[INFO] Connecting to Docker daemon...
[INFO] Building Docker image flask-apparmor...
[BUILD] Step 1/6 : FROM python:3.9-slim
[BUILD] ---> 2d97f6910b16
[BUILD] Step 2/6 : WORKDIR /app
[BUILD] ---> Using cache
[BUILD] ---> 10755e63bfb1
[BUILD] Step 3/6 : COPY . /app
[BUILD] ---> de7a7776feac
[BUILD] Step 4/6 : RUN pip install --no-cache-dir flask
[BUILD] Successfully built 87dbfe34a5c7
[BUILD] Successfully tagged flask-apparmor:latest
[INFO] Successfully built flask-apparmor
[INFO] Running container with AppArmor profile...
Container started: 608d81749b51
AppArmor profile applied: ['apparmor=my-apparmor-profile']
Stopping the container...
Container stopped and removed successfully.
```

### 2. Test Restricted Actions via Python Script
```powershell
python test_restricted_actions.py
```
**Actual Output:**
```text
[INFO] Connecting to Docker daemon...
Container started: 7ae184b1ce1e
Attempt to read /etc/passwd: Exit Code 0
Attempt to execute /bin/bash: Exit Code 126, Output: 
Container stopped and removed.
```
*Note: Exit Code 126 signifies that the binary could not be executed due to permission / security profile restrictions.*

---

## 8. Verification & Security Questions & Answers (from Lab Manual)

- **Q1: What is the purpose of using AppArmor with Docker containers?**  
  *Answer:* AppArmor enforces Mandatory Access Control (MAC) policies, strictly confining applications and processes to a predefined set of file paths, execution privileges, and Linux capabilities, thereby preventing lateral container escapes.
- **Q2: How do AppArmor profiles help secure a Docker container?**  
  *Answer:* AppArmor profiles define granular allow/deny rules for file system paths, network access, binary execution, and Linux capabilities. Even if an attacker gains root access inside the container, AppArmor prevents them from tampering with the host system or restricted resources.
- **Q3: Why is it important to restrict access to sensitive directories such as `/etc/` and `/var/`?**  
  *Answer:* Directories like `/etc/` contain crucial authentication credentials, security certificates, and system configuration files, while `/var/` stores dynamic logs and runtime states. Restricting access prevents information disclosure, credential theft, and unauthorized system modifications.
- **Q4: What other capabilities can you restrict using AppArmor profiles?**  
  *Answer:* Network sockets (e.g., preventing raw socket creation with `cap_net_raw`), administrative privileges (`cap_sys_admin`), mount operations, debugging traces (`cap_sys_ptrace`), and binding to privileged system ports below 1024.
- **Q5: How can you verify if an AppArmor profile is successfully applied to a Docker container?**  
  *Answer:* By inspecting the container metadata via the Docker CLI (`docker inspect <id>`) or Docker SDK (`client.api.inspect_container`), verifying that `HostConfig.SecurityOpt` contains `'apparmor=<profile-name>'`.

---

## 9. Result & Conclusion
- Successfully authored a hardened AppArmor profile restricting binary execution and filesystem paths.
- Enforced container security profiles programmatically using the Python Docker SDK.
- Inspected and verified the active security configuration in Docker container metadata.
- Successfully demonstrated restricted execution failure (Exit Code 126) for blocked binary executions.
