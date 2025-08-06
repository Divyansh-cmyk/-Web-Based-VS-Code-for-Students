import subprocess
import csv
import socket
import sys
import os
import json

def check_docker():
    """Check if Docker is running."""
    try:
        subprocess.run(["docker", "--version"], check=True, capture_output=True)
        print("Docker is running.")
    except subprocess.CalledProcessError:
        print("Error: Docker is not installed or not running. Please start Docker Desktop.")
        sys.exit(1)

def check_port(port):
    """Check if a port is available."""
    result = subprocess.run(["netstat", "-ano", "|", "findstr", f":{port}"], shell=True, capture_output=True, text=True)
    return not result.stdout

def create_settings_json(workspace_dir):
    """Create VS Code settings.json with enabled extensions and configurations."""
    settings = {
        "extensions.autoUpdate": True,
        "extensions.autoCheckUpdates": True,
        "extensions.ignoreRecommendations": False,
        # Code Runner settings for immediate use with installed runtimes
        "code-runner.runInTerminal": True,
        "code-runner.saveFileBeforeRun": True,
        "code-runner.executorMap": {
            "python": "python",
            "javascript": "node",
            "java": "javac $fileName && java $fileNameWithoutExt",
            "cpp": "g++ $fileName -o $fileNameWithoutExt && $fileNameWithoutExt",
            "c": "gcc $fileName -o $fileNameWithoutExt && $fileNameWithoutExt",
            "go": "go run",
            "csharp": "mcs $fileName && mono $fileNameWithoutExt.exe"
        }
    }
    settings_path = os.path.join(workspace_dir, ".vscode")
    os.makedirs(settings_path, exist_ok=True)
    with open(os.path.join(settings_path, "settings.json"), "w") as f:
        json.dump(settings, f, indent=4)

def setup_student_envs(num_students, base_port=8080, base_dir="E:\\student_workspaces"):
    """Set up Docker containers for students with pre-installed languages and extensions."""
    check_docker()
    ip = socket.gethostbyname(socket.gethostname())
    links = []

    # Stop and remove existing containers to avoid conflicts
    for i in range(1, num_students + 1):
        container_name = f"code_server_{i}"
        subprocess.run(["docker", "stop", container_name], capture_output=True, text=True)
        subprocess.run(["docker", "rm", container_name], capture_output=True, text=True)

    for i in range(1, num_students + 1):
        port = base_port + i
        # Find a free port
        while not check_port(port):
            print(f"Port {port} is in use, trying next port...")
            port += 1

        student_id = f"student_{i}"
        workspace = os.path.join(base_dir, student_id)
        password = f"student{i}_pass"

        # Create workspace directory and settings.json
        os.makedirs(workspace, exist_ok=True)
        create_settings_json(workspace)

        # Start Docker container with custom image
        container_name = f"code_server_{i}"
        print(f"Starting container for {student_id} on port {port}...")
        try:
            subprocess.run([
                "docker", "run", "-d", "--name", container_name,
                "-p", f"{port}:8080",
                "-v", f"{workspace}:/home/coder/project",
                "-v", f"{workspace}/.local/share/code-server:/home/coder/.local/share/code-server",
                "-e", f"PASSWORD={password}",
                "mycode-server:latest",
                "--auth", "password"
            ], check=True, capture_output=True)
        except subprocess.CalledProcessError as e:
            print(f"Error starting container for {student_id}: {e}")
            continue

        # Generate direct port link
        link = f"http://{ip}:{port}"
        links.append({"Student_ID": student_id, "Link": link, "Password": password})

    # Save to CSV
    csv_path = os.path.join(base_dir, "student_links.csv")
    with open(csv_path, "w", newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["Student_ID", "Link", "Password"])
        writer.writeheader()
        writer.writerows(links)
    print(f"CSV saved to {csv_path}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python setup_student_envs_no_nginx.py <number_of_students>")
        sys.exit(1)
    
    try:
        num_students = int(sys.argv[1])
        if num_students < 1:
            raise ValueError("Number of students must be positive.")
        print("🎉 Setting up student environments with pre-installed languages and extensions! 🎉")
        setup_student_envs(num_students)
    except ValueError:
        print("Error: Please provide a valid number of students.")
        sys.exit(1)