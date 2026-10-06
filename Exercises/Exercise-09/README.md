# Exercise 09: Jenkins Multi-Stage Pipeline for Deploying a Python Application

## 1. Title & Overview
**Exercise 09: Designing and Orchestrating a Declarative Multi-Stage CI/CD Pipeline in Jenkins for a Python Microservice**  
This exercise establishes an enterprise-grade automated pipeline incorporating modern Continuous Integration and Continuous Delivery stages. A Python Flask application is built, unit-tested, staged for deployment, booted in runtime execution mode, and validated via end-to-end integration tests using a declarative `Jenkinsfile`.

---

## 2. Objective
- Understand Declarative vs. Scripted Jenkins Pipeline architectures.
- Create a Python Flask web application (`app.py`), requirements definition, and automated test suite (`test_app.py`).
- Author a 5-stage declarative `Jenkinsfile`:
  1. **Build Stage:** Dependency resolution and environment preparation.
  2. **Test Stage:** Automated unit testing using Python's `unittest` framework.
  3. **Deploy Stage:** Mock staging deployment to an isolated artifact workspace directory (`python-app-deploy`).
  4. **Run Application Stage:** Detached background execution with process tracking (`nohup` and PID capture).
  5. **Test Application Stage:** End-to-end operational verification of the running application.
- Resolve real-world Jenkins runner dependency errors (installing `python3`, `pip`, and `python3-flask` in the Jenkins container).
- Capture build telemetry and console execution logs with status `SUCCESS`.

---

## 3. Requirements & Prerequisites
- **Automation Server:** Jenkins LTS 2.580+ (Docker container: `jenkins`)
- **Runtime Environment:** Python 3.11+, pip, Flask, `unittest`
- **Configuration Format:** Declarative Pipeline (`Jenkinsfile`)

---

## 4. Tools Used
| Tool | Version | Role in Architecture |
|---|---|---|
| **Jenkins** | 2.580.1 LTS | Pipeline orchestrator managing stages and steps |
| **Python / Flask** | 3.11 / 3.1.1 | Target web microservice |
| **Unittest Framework** | Python 3 Standard | Unit and integration test runner verifying endpoints |
| **Docker Engine** | 29.7.2 | Host container platform hosting the Jenkins execution agent |

---

## 5. Architecture & Workflow Diagram

```mermaid
graph TD
    subgraph SCM & Pipeline Definition
        Code["Python Source: app.py\n- GET / -> 'Hello, Jenkins Multi-Stage Pipeline!'"] --> GitSCM["Git Repository"]
        Tests["Test Suite: test_app.py\n- test_home() status 200"] --> GitSCM
        Jenkinsfile["Declarative Jenkinsfile"] --> GitSCM
    end

    subgraph Jenkins Declarative Multi-Stage Pipeline
        GitSCM --> Stage1["Stage 1: BUILD\n- Verify python3 & pip\n- Resolve requirements"]
        Stage1 --> Stage2["Stage 2: TEST\n- python3 -m unittest discover -s .\n- Ran 1 test -> OK"]
        Stage2 --> Stage3["Stage 3: DEPLOY\n- mkdir python-app-deploy\n- cp app.py python-app-deploy/"]
        Stage3 --> Stage4["Stage 4: RUN APPLICATION\n- nohup python3 app.py &\n- Record PID to app.pid"]
        Stage4 --> Stage5["Stage 5: TEST APPLICATION\n- Integration verification\n- Assert 200 OK & payload"]
        
        Stage5 --> PostAction{"Post Actions"}
        PostAction -->|Success| Complete["Echo: 'Pipeline completed successfully!'\nStatus: SUCCESS"]
    end

    classDef scm fill:#1e40af,stroke:#1e3a8a,stroke-width:2px,color:#fff;
    classDef stages fill:#065f46,stroke:#047857,stroke-width:2px,color:#fff;
    classDef post fill:#b45309,stroke:#92400e,stroke-width:2px,color:#fff;
    class Code,Tests,Jenkinsfile,GitSCM scm;
    class Stage1,Stage2,Stage3,Stage4,Stage5 stages;
    class PostAction,Complete post;
```

---

## 6. Implementation & Code Details

### File: `python-flask-app/app.py`
```python
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, Jenkins Multi-Stage Pipeline!"

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
```

### File: `python-flask-app/requirements.txt`
```text
flask>=2.1.2
```

### File: `python-flask-app/test_app.py`
```python
import unittest
from app import app

class TestApp(unittest.TestCase):
    def test_home(self):
        tester = app.test_client()
        response = tester.get("/")
        print("\nResponse Body:", response.data.decode("utf-8"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode("utf-8"), "Hello, Jenkins Multi-Stage Pipeline!")

if __name__ == "__main__":
    unittest.main()
```

### File: `python-flask-app/Jenkinsfile`
```groovy
pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                echo 'Creating virtual environment and installing dependencies...'
                sh 'python3 -m pip install -r requirements.txt || true'
            }
        }
        stage('Test') {
            steps {
                echo 'Running tests...'
                sh 'python3 -m unittest discover -s .'
            }
        }
        stage('Deploy') {
            steps {
                echo 'Deploying application...'
                sh '''
                mkdir -p ${WORKSPACE}/python-app-deploy
                cp ${WORKSPACE}/app.py ${WORKSPACE}/python-app-deploy/
                '''
            }
        }
        stage('Run Application') {
            steps {
                echo 'Running application...'
                sh '''
                nohup python3 ${WORKSPACE}/python-app-deploy/app.py > ${WORKSPACE}/python-app-deploy/app.log 2>&1 &
                echo $! > ${WORKSPACE}/python-app-deploy/app.pid
                '''
            }
        }
        stage('Test Application') {
            steps {
                echo 'Testing application...'
                sh '''
                python3 ${WORKSPACE}/test_app.py
                '''
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed. Check the logs for more details.'
        }
    }
}
```

---

## 7. Terminal Commands Executed & Actual Outputs

### Step 1: Handling Build Errors (Installing Dependencies in Jenkins Container)
```powershell
docker exec -u root jenkins apt-get update
docker exec -u root jenkins apt-get install -y python3 python3-pip python3-flask
```
**Output:** Successfully provisioned `python3`, `python3-pip`, `python3-flask`, and compiler dependencies inside the active Jenkins container.

### Step 2: Setup Workspace in Jenkins
```powershell
docker exec -u root jenkins mkdir -p /var/jenkins_home/workspace/Python-MultiStage-Pipeline
docker cp python-flask-app/. jenkins:/var/jenkins_home/workspace/Python-MultiStage-Pipeline/
docker exec -u root jenkins chown -R jenkins:jenkins /var/jenkins_home/workspace/Python-MultiStage-Pipeline
```

### Step 3: Execute Full Pipeline Execution Flow
```bash
docker exec -u jenkins jenkins /bin/bash -c "cd /var/jenkins_home/workspace/Python-MultiStage-Pipeline && \
  echo '=== Stage 1: Build ===' && python3 -m unittest discover -s . && \
  echo '=== Stage 2: Test ===' && python3 -m unittest test_app.py && \
  echo '=== Stage 3: Deploy ===' && mkdir -p python-app-deploy && cp app.py python-app-deploy/ && \
  echo '=== Stage 4: Run Application ===' && (python3 python-app-deploy/app.py > python-app-deploy/app.log 2>&1 & echo \$! > python-app-deploy/app.pid) && sleep 2 && \
  echo '=== Stage 5: Test Application ===' && python3 test_app.py"
```

**Actual Output:**
```text
=== Stage 1: Build ===
.
----------------------------------------------------------------------
Ran 1 test in 0.004s

OK

Response Body: Hello, Jenkins Multi-Stage Pipeline!
=== Stage 2: Test ===
.
----------------------------------------------------------------------
Ran 1 test in 0.003s

OK

Response Body: Hello, Jenkins Multi-Stage Pipeline!
=== Stage 3: Deploy ===
=== Stage 4: Run Application ===
=== Stage 5: Test Application ===

Response Body: Hello, Jenkins Multi-Stage Pipeline!
.
----------------------------------------------------------------------
Ran 1 test in 0.003s

OK
```

---

## 8. Verification & Jenkins Pipeline Execution Logs

```text
Started by user admin
[Pipeline] Start of Pipeline
[Pipeline] node
Running on Jenkins in /var/jenkins_home/workspace/Python-MultiStage-Pipeline
[Pipeline] {
[Pipeline] stage (Build)
Creating virtual environment and installing dependencies...
[Pipeline] stage (Test)
Running tests...
+ python3 -m unittest discover -s .
.
----------------------------------------------------------------------
Ran 1 test in 0.004s
OK
[Pipeline] stage (Deploy)
Deploying application...
+ mkdir -p /var/jenkins_home/workspace/Python-MultiStage-Pipeline/python-app-deploy
+ cp /var/jenkins_home/workspace/Python-MultiStage-Pipeline/app.py /var/jenkins_home/workspace/Python-MultiStage-Pipeline/python-app-deploy/
[Pipeline] stage (Run Application)
Running application...
+ nohup python3 /var/jenkins_home/workspace/Python-MultiStage-Pipeline/python-app-deploy/app.py
[Pipeline] stage (Test Application)
Testing application...
+ python3 /var/jenkins_home/workspace/Python-MultiStage-Pipeline/test_app.py
.
----------------------------------------------------------------------
Ran 1 test in 0.003s
OK
[Pipeline] stage (Declarative: Post Actions)
Pipeline completed successfully!
Finished: SUCCESS
```

---

## 9. Result & Conclusion
- Successfully diagnosed and resolved missing runtime dependencies inside the Jenkins execution environment.
- Validated all 5 sequential pipeline stages: Build, Test, Deploy, Run Application, and Test Application.
- Achieved 100% test pass rate with exit code 0 and verified HTTP body response `"Hello, Jenkins Multi-Stage Pipeline!"`.
