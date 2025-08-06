
---

# Student Coding Environments

This project provides an automated solution to set up isolated, web-based coding environments for students using [code-server](https://github.com/coder/code-server), a browser-based Visual Studio Code. Each student gets a dedicated Docker container with pre-installed programming languages (Python, Java, C/C++, Go, C#) and essential VS Code extensions, accessible via unique URLs and passwords. Perfect for classrooms, coding bootcamps, or educational workshops.

## ✨ Features
- **Isolated Workspaces**: Individual `code-server` instances for each student, ensuring privacy and independence.
- **Pre-installed Runtimes**: Supports Python, Java, C, C++, Go, and C# out of the box.
- **VS Code Extensions**: Includes Code Runner, Python, C/C++, Java, Go, C#, ESLint, Prettier, and Live Server for a ready-to-code experience.
- **Dynamic Port Management**: Automatically assigns available ports to avoid conflicts.
- **CSV Output**: Generates a `student_links.csv` with student IDs, access URLs, and passwords for easy distribution.
- **Persistent Workspaces**: Student projects are saved in local directories for continuity.

## 📋 Prerequisites
- **Docker**: Install [Docker Desktop](https://www.docker.com/products/docker-desktop/) and ensure it’s running.
- **Python 3**: Required for the primary setup script (`setup_student_envs_no_nginx.py`).
- **Windows**: The batch script (`start_student_envs.bat`) is Windows-specific. For other OS, use the Python script.
- **Git**: For cloning and managing the repository.

## 🚀 Installation
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/student-coding-environments.git
   cd student-coding-environments
   ```

2. **Build the Docker Image**:
   The `Dockerfile` creates a custom `code-server` image with required runtimes and extensions.
   ```bash
   docker build -t mycode-server:latest .
   ```

3. **Set Up Workspace Directory**:
   Ensure the base directory (default: `E:\student_workspaces`) exists and is writable. Modify `BASE_DIR` in the scripts if needed.

## 🛠️ Usage
### Option 1: Python Script (Recommended)
The `setup_student_envs_no_nginx.py` script automates environment setup with port conflict handling and CSV generation.

1. Run the script with the number of students:
   ```bash
   python setup_student_envs_no_nginx.py <number_of_students>
   ```
   Example:
   ```bash
   python setup_student_envs_no_nginx.py 5
   ```

2. **What Happens**:
   - Verifies Docker is running.
   - Creates a workspace directory for each student (e.g., `E:\student_workspaces\student_1`).
   - Launches a `code-server` container per student on unique ports (starting from 8081).
   - Saves access details (Student ID, URL, Password) to `E:\student_workspaces\student_links.csv`.

3. **Access Environments**:
   - Open `student_links.csv` to find each student’s URL (e.g., `http://192.168.56.1:8081`) and password (e.g., `student1_pass`).
   - Share the respective URL and password with each student to access their coding environment.

### Option 2: Batch Script (Windows Only)
The `start_student_envs.bat` script is a simpler alternative for Windows but lacks port conflict checks.

1. Run the script:
   ```bash
   start_student_envs.bat <number_of_students>
   ```
   Example:
   ```bash
   start_student_envs.bat 5
   ```

2. **What Happens**:
   - Creates workspace directories and starts containers.
   - Displays URLs (e.g., `http://<COMPUTERNAME>:8081`) and passwords (`student1_pass`, etc.).

3. **Note**: Manually note down the URLs and passwords, as no CSV is generated.

## 📂 Repository Structure
- **`Dockerfile`**: Defines the custom `code-server` image with runtimes and a startup script.
- **`startup.sh`**: Installs VS Code extensions and launches `code-server`.
- **`setup_student_envs_no_nginx.py`**: Python script for automated setup with port management and CSV output.
- **`start_student_envs.bat`**: Windows batch script for basic setup.
- **`.gitignore`**: Excludes student workspaces, CSV files, Python cache, Docker artifacts, and OS-specific files.
- **`student_links.csv`**: Generated file with student access details (not committed to Git).

## ⚙️ Customization
- **Workspace Directory**: Update `BASE_DIR` in scripts (default: `E:\student_workspaces`).
- **Port Range**: Change `BASE_PORT` (default: 8080) in scripts to use different ports.
- **Extensions**: Modify `startup.sh` to add or remove VS Code extensions.
- **Runtimes**: Edit the `Dockerfile` to include additional programming languages or tools.

## 🔒 Security Notes
- **Sensitive Data**: The `student_links.csv` file contains URLs and passwords. Do not share it publicly or commit it to Git (it’s excluded via `.gitignore`).
- **Firewall**: Ensure your firewall allows traffic on the used ports (e.g., 8081–8085).
- **Access Control**: Distribute URLs and passwords securely to students.

## 🛡️ Troubleshooting
- **Docker Not Running**: Start Docker Desktop before running scripts.
- **Port Conflicts**: Use `netstat -ano | findstr :<port>` to check for occupied ports. The Python script auto-resolves conflicts by selecting the next available port.
- **URL Not Working**: Verify your machine’s IP address (`ipconfig`) matches the URLs in `student_links.csv`. Adjust firewall settings if needed.
- **Container Errors**: Check Docker logs with `docker logs code_server_<number>` for specific issues.

## 🤝 Contributing
We welcome contributions! Please fork the repository, make changes, and submit a pull request. Report bugs or suggest features via GitHub Issues.

## 📜 License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

