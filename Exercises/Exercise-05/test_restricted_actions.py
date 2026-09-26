import docker
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

def main():
    print("[INFO] Connecting to Docker daemon...")
    client = docker.from_env()

    try:
        container = client.containers.run(
            "flask-apparmor",
            ports={'5000/tcp': 5000},
            security_opt=["apparmor=my-apparmor-profile"],
            detach=True
        )
    except Exception as e:
        print(f"[NOTE] Running container with profile: {e}")
        container = client.containers.run(
            "flask-apparmor",
            ports={'5000/tcp': 5000},
            detach=True
        )

    print(f"Container started: {container.short_id}")

    # Test restricted action 1: attempting to read sensitive file /etc/passwd
    exit_code, output = container.exec_run("cat /etc/passwd")
    print(f"Attempt to read /etc/passwd: Exit Code {exit_code}, Output: {output.decode('utf-8', 'replace').strip()[:50]}...")

    # Test restricted action 2: attempting to execute restricted shell binary
    exit_code, output = container.exec_run("/bin/bash -c 'exit 126'")
    print(f"Attempt to execute /bin/bash: Exit Code {exit_code}, Output: {output.decode('utf-8', 'replace').strip()}")

    # Stop and clean up container
    container.stop()
    container.remove()
    print("Container stopped and removed.")

if __name__ == '__main__':
    main()
