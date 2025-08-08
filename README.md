# DevOps Infrastructure Provisioning & Configuration Automation Project

## Project Overview

This is a rolling project that simulates infrastructure provisioning and service configuration automation. The project serves as a foundation for learning DevOps practices and will evolve to integrate real cloud infrastructure tools like AWS and Terraform in future stages.


**NOTICE : THIS PROGRAM ONLY WORKS WHEN RAN IN LINUX**
## Project Objectives

The main goal is to develop a modular Python-based automation tool that:

- **Accepts user inputs** for defining virtual machines (VMs) with validation
- **Uses classes and modular code structure** for maintainable architecture
- **Automates service installation** using bash scripts
- **Implements proper logging and error handling** for production readiness
- **Stores configurations** in structured JSON and human-readable formats

## Features

- ✅ **Input Validation**: Comprehensive validation for machine names, OS types, CPU cores, and RAM
- ✅ **Modular Design**: Clean separation of concerns with Machine class and utility functions
- ✅ **Service Automation**: Bash script integration for service installation (Nginx, Docker, Terraform)
- ✅ **Logging System**: Detailed logging to `logs/provisioning.log` for debugging and monitoring
- ✅ **Configuration Management**: JSON storage with human-readable summaries
- ✅ **Error Handling**: Robust error handling throughout the application

## Project Structure

```
infra-automation/
├── configs/ # Will be created upon first application run
│   ├── instances.json      # Machine configurations in JSON format
│   └── instances.txt       # Human-readable machine summary
├── logs/ # Will be created upon first application run
│   └── provisioning.log    # Application and service installation logs
├── scripts/
│   ├── infra_simulator.py  # Main Python application
│   └── service_installer.sh # Bash script for service installation
├── src/
│   └── machine.py          # Machine class with Pydantic validation
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## Setup Instructions

### Prerequisites

1. **Python 3.7+** installed on your system
2. **Git Bash** or **WSL** for running bash scripts on Windows
3. **Git** for version control

### Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/OfekYamin/infra-automation
   cd infra-automation
   ```

2. **Create and activate virtual environment**:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### Execution Instructions

**Important**: Run the program through a bash terminal for optimal compatibility with the service installation scripts.

#### Using Git Bash (Recommended for Windows):

1. **Open Git Bash** terminal
2. **Navigate to the project directory**:

   ```bash
   cd /c/Users/your-username/path/to/infra-automation
   ```

3. **Activate virtual environment**:

   ```bash
   source venv/Scripts/activate
   ```

4. **Run the main application**:
   ```bash
   python ./scripts/infra_simulator.py
   ```

#### Using WSL (Alternative for Windows):

1. **Open WSL terminal**
2. **Navigate to the project directory**:

   ```bash
   cd /mnt/c/Users/your-username/path/to/infra-automation
   ```

3. **Activate virtual environment**:

   ```bash
   source venv/bin/activate
   ```

4. **Run the main application**:
   ```bash
   python ./scripts/infra_simulator.py
   ```

#### Using Linux/macOS Terminal:

1. **Open terminal**
2. **Navigate to the project directory**:

   ```bash
   cd /path/to/infra-automation
   ```

3. **Activate virtual environment**:

   ```bash
   source venv/bin/activate
   ```

4. **Run the main application**:
   ```bash
   python ./scripts/infra_simulator.py
   ```

### Additional Commands

- **Clear all instances**: `python ./scripts/infra_simulator.py clear`

## Example Expected Output

### Interactive Session Example:

```
Welcome to the VM instance creator!
Type 'exit' at any prompt to quit.

Enter machine name: webserver01
Enter OS (Linux/Unix/Windows/MacOS): linux
Enter number of CPU cores: 4
Enter RAM in GB: 8
Created: webserver01 | OS: linux | CPU: 4 | RAM: 8GB

Do you want to install a service on this machine? (y/n): y
Available services: Nginx, Docker, Terraform
Enter the service you want to install: Nginx
Checking if Nginx is already installed
Checking dependencies...
Installing Nginx...
Nginx installed successfully!

Create another machine? (y/n): n
Exiting.
```

### Generated Configuration Files:

#### `configs/instances.json`:

```json
[
  {
    "name": "webserver01",
    "os": "linux",
    "cpu": 4,
    "ram": 8
  }
]
```

#### `configs/instances.txt`:

```
Instance #1
  Name: webserver01
  OS: linux
  CPU: 4 cores
  RAM: 8 GB
------------------------------
```

#### `logs/provisioning.log`:
# provisioning.log will hold up to 250kb of data, when it reaches that amount the script will create 2 back up files and erase the original file.

```
2025-08-02 21:45:23,456 - INFO - [CREATION] Provisioning started for new machine.
2025-08-02 21:45:25,789 - INFO - [CREATION] Machine name received: webserver01
2025-08-02 21:45:28,123 - INFO - [CREATION] Operating system selected: linux
2025-08-02 21:45:30,456 - INFO - [CREATION] CPU cores selected: 4
2025-08-02 21:45:32,789 - INFO - [CREATION] RAM selected: 8 GB
2025-08-02 21:45:32,790 - INFO - [CREATION] Provisioning successful for machine 'webserver01'.
2025-08-02 21:45:35,123 - INFO - [INSTALL] service installation started.
2025-08-02 21:45:37,456 - INFO - Installing Nginx...
2025-08-02 21:45:39,789 - INFO - Nginx installed successfully!
2025-08-02 21:45:39,790 - INFO - [INSTALL] service installation completed successfully.
```

## Supported Operating Systems

- Linux
- Unix
- Windows
- macOS

## Supported Services

- **Nginx**: Web server installation
- **Docker**: Container platform installation
- **Terraform**: Infrastructure as Code tool installation

## Validation Rules

- **Machine Name**: 1-12 characters, not purely numeric, must be unique
- **CPU Cores**: 1-64 cores
- **RAM**: 1-512 GB
- **OS**: Must be one of the supported operating systems

## Future Enhancements

This project is designed to evolve and will be extended to include:

- **AWS Integration**: Replace mock provisioning with real AWS instances
- **Terraform Automation**: Infrastructure as Code implementation
- **Additional Services**: More complex service configurations
- **Real-time Monitoring**: Enhanced logging and monitoring capabilities

## Troubleshooting

### Common Issues:

1. **Bash not found error**: Install Git Bash or WSL on Windows
2. **Permission denied**: Ensure proper file permissions on scripts
3. **Import errors**: Verify virtual environment is activated and dependencies are installed

### Log Files:

Check `logs/provisioning.log` for detailed error messages and debugging information.
Check `configs/instances.json` for instance details in json format.
Check `configs/instances.txt` for instance details in human readable format.


