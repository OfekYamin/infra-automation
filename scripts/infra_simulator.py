# Main script for rolling project.
import json
import sys
from pathlib import Path
import logging
import subprocess

# Storing the project root directory as a variable for future use
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# Path Variables
Configs_Path = project_root / "configs"
Logs_Path = project_root / "logs"
JSON_Path = Configs_Path / "instances.json"
TXT_Path = Configs_Path / "instances.txt"
Provisioning_Log_File = Logs_Path / "provisioning.log"
script_path = project_root / "scripts" / "service_installer.sh"

# Directory setup
Configs_Path.mkdir(parents=True, exist_ok=True)
Logs_Path.mkdir(parents=True, exist_ok=True)

# Named logger setup
infra_logger = logging.getLogger("infra_simulator")

def setup_logging(log_file_path):
    infra_logger.setLevel(logging.INFO)
    infra_logger.propagate = False

    if not infra_logger.handlers:
        file_handler = logging.FileHandler(log_file_path)
        file_handler.setLevel(logging.INFO)

        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)

        infra_logger.addHandler(file_handler)

setup_logging(Provisioning_Log_File)


from src.machine import Machine



# Load VM instances
def load_instances():
    if not JSON_Path.exists():
        infra_logger.info("[LOAD] instances.json file does not exist, creating empty list")
        return []
    try:
        with open(JSON_Path, "r") as f:
            data = json.load(f)
            infra_logger.info(f"[LOAD] Successfully loaded {len(data)} instances from JSON file")
            return data if isinstance(data, list) else []
    except json.JSONDecodeError as e:
        infra_logger.error(f"[LOAD] JSON decode error in instances.json: {e}")
        return []
    except FileNotFoundError as e:
        infra_logger.error(f"[LOAD] File not found error: {e}")
        return []
    except Exception as e:
        infra_logger.error(f"[LOAD] Unexpected error loading instances: {e}")
        return []



# Save VM instance
def save_instance(instance_data):
    try:
        data = load_instances()
        data.append(instance_data)
        with open(JSON_Path, "w") as f:
            json.dump(data, f, indent=4)
        infra_logger.info(f"[SAVE] Successfully saved instance '{instance_data.get('name', 'unknown')}' to JSON file")
        write_human_readable_summary(data)
    except PermissionError as e:
        infra_logger.error(f"[SAVE] Permission denied when saving to JSON file: {e}", exc_info=True)
        raise
    except Exception as e:
        infra_logger.error(f"[SAVE] Unexpected error saving instance: {e}", exc_info=True)
        raise



# Human-readable summary
def write_human_readable_summary(instances):
    try:
        with open(TXT_Path, "w") as f:
            if not instances:
                f.write("No VM instances available.\n")
                infra_logger.info("[SUMMARY] Wrote empty instances summary to text file")
                return
            for idx, vm in enumerate(instances, 1):
                f.write(f"Instance #{idx}\n")
                f.write(f"  Name: {vm['name']}\n")
                f.write(f"  OS: {vm['os']}\n")
                f.write(f"  CPU: {vm['cpu']} cores\n")
                f.write(f"  RAM: {vm['ram']} GB\n")
                f.write("-" * 30 + "\n")
        infra_logger.info(f"[SUMMARY] Successfully wrote summary for {len(instances)} instances to text file")
    except PermissionError as e:
        infra_logger.error(f"[SUMMARY] Permission denied when writing to text file: {e}", exc_info=True)
        raise
    except Exception as e:
        infra_logger.error(f"[SUMMARY] Unexpected error writing summary: {e}", exc_info=True)
        raise



# Input handler
def get_input(prompt, validator):
    while True:
        try:
            value = input(prompt).strip()
            if value.lower() == "exit":
                print("Exiting.")
                infra_logger.info("[EXIT] User exited input prompt.")
                exit()
            if not value:
                infra_logger.warning("[INPUT] Empty input received, prompting again")
                print("Error: Input cannot be empty.")
                continue
            return validator(value)
        except ValueError as e:
            print(f"Error: {e}")
            infra_logger.warning(f"[INPUT] Validation error: {e}")
        except KeyboardInterrupt:
            infra_logger.info("[EXIT] User interrupted with Ctrl+C")
            print("\nExiting.")
            exit()
        except EOFError:
            infra_logger.info("[EXIT] User triggered EOF (Ctrl+D)")
            print("\nExiting.")
            exit()
        except Exception as e:
            infra_logger.error(f"[INPUT] Unexpected error during input: {e}", exc_info=True)
            print(f"Unexpected error: {e}")



# Name input validators
def get_machine_name(existing_names):
    def validate(name):
        if not (1 <= len(name) <= 12):
            raise ValueError("Name must be 1–12 characters.")
        if name.isdigit():
            raise ValueError("Name cannot be purely numeric.")
        if name in existing_names:
            raise ValueError("Name already exists.")
        return name
    return get_input("Enter machine name: ", validate)



# Get operating system input
def get_os():
    def validate(os_name):
        os_name = os_name.lower()
        if os_name not in Machine.supported_os:
            raise ValueError(f"Unsupported OS. Choose from: Linux/Unix/MacOS/Windows")
        return os_name
    return get_input("Enter OS (Linux/Unix/Windows/MacOS): ", validate)


# Get CPU input
def get_cpu():
    def validate_cpu(val):
        try:
            val = int(val)
            if not (1 <= val <= 64):
                raise ValueError("CPU must be between 1 and 64 cores.")
            return val
        except:
            raise ValueError("CPU must be between 1 and 64 cores.")
    return get_input("Enter number of CPU cores: ", validate_cpu)


# Get RAM input
def get_ram():
    def validate_ram(val):
        try:
            val = int(val)
            if not (1 <= val <= 512):
                raise ValueError("RAM must be between 1 and 512 GB.")
            return val
        except:
            raise ValueError("RAM must be between 1 and 512 GB.")
    return get_input("Enter RAM in GB: ", validate_ram)


# Create machine
def create_machine():
    infra_logger.info("[CREATION] Provisioning started for new machine.")

    try:
        existing_data = load_instances()
        existing_names = {item["name"] for item in existing_data}
        infra_logger.info(f"[CREATION] Found {len(existing_names)} existing machine names")

        # Name Logging
        infra_logger.info("[CREATION] Prompting user for machine name.")
        name = get_machine_name(existing_names)
        infra_logger.info(f"[CREATION] Machine name received: {name}")

        # OS Logging
        infra_logger.info("[CREATION] Prompting user for operating system.")
        os = get_os()
        infra_logger.info(f"[CREATION] Operating system selected: {os}")

        # CPU Logging
        infra_logger.info("[CREATION] Prompting user for number of CPU cores.")
        cpu = get_cpu()
        infra_logger.info(f"[CREATION] CPU cores selected: {cpu}")

        # RAM Logging
        infra_logger.info("[CREATION] Prompting user for RAM amount.")
        ram = get_ram()
        infra_logger.info(f"[CREATION] RAM selected: {ram} GB")

        # Machine creation
        infra_logger.info(f"[CREATION] Creating Machine object with: name={name}, os={os}, cpu={cpu}, ram={ram}")
        machine = Machine(name=name, os=os, cpu=cpu, ram=ram)
        print("Created:", machine)
        
        # Save to files
        infra_logger.info("[CREATION] Saving machine instance to files")
        save_instance(machine.as_dict)
        infra_logger.info(f"[CREATION] Provisioning successful for machine '{name}'.")
        return machine
        
    except Exception as e:
        infra_logger.error(f"[CREATION] Provisioning failed: {e}", exc_info=True)
        print("Failed to create machine:", e)
        return None
    


# Clear log files function
def clear_instances():
    try:
        infra_logger.info("[CLEAR] Starting to clear all VM instances")
        with open(JSON_Path, "w") as f:
            json.dump([], f, indent=4)
        infra_logger.info("[CLEAR] Successfully cleared JSON file")
        
        write_human_readable_summary([])
        infra_logger.info("[CLEAR] Successfully cleared text summary file")
        
        infra_logger.info("[CLEAR] All VM instances cleared successfully")
        print("All VM instances cleared.")
    except PermissionError as e:
        infra_logger.error(f"[CLEAR] Permission denied when clearing files: {e}", exc_info=True)
        print("Error: Permission denied when clearing files.")
        raise
    except Exception as e:
        infra_logger.error(f"[CLEAR] Unexpected error clearing instances: {e}", exc_info=True)
        print("Error: Failed to clear instances.")
        raise



# Install service
def service_installer():
    try:
        infra_logger.info("[INSTALL] Service installation started")
        infra_logger.info(f"[INSTALL] Executing bash script: {script_path}")
        
        if not script_path.exists():
            infra_logger.error(f"[INSTALL] Bash script not found: {script_path}", exc_info=True)
            print(f"Error: Service installer script not found at {script_path}")
            return None
            
        # Run the bash script interactively (not capturing output to allow user input)
        result = subprocess.run(["bash", str(script_path)], check=True)
        infra_logger.info("[INSTALL] Service installation completed successfully")
        
        return "Service installation completed"
        
    except subprocess.CalledProcessError as e:
        if e.returncode == 99:
            infra_logger.info("[EXIT] Service installation exited by user")
            print("Exiting program.")
            exit()
        infra_logger.error(f"[INSTALL] Service installation failed with return code {e.returncode}", exc_info=True)
        print(f"Error: Service installation failed (return code: {e.returncode})")
        return None
    except FileNotFoundError:
        infra_logger.error("[INSTALL] Bash command not found - bash not installed or not in PATH", exc_info=True)
        print("Error: Bash not found. Please install Git Bash or WSL on Windows.")
        return None
    except Exception as e:
        infra_logger.error(f"[INSTALL] Unexpected error during service installation: {e}", exc_info=True)
        print(f"Error: Unexpected error during service installation: {e}")
        return None



# Main execution block
if __name__ == "__main__":
    try:
        infra_logger.info("====================================== Infrastructure Simulator Started ======================================")
        
        if len(sys.argv) > 1 and sys.argv[1].lower() == "clear":
            infra_logger.info("[MAIN] Clear command detected")
            clear_instances()
        else:
            print("Welcome to the VM instance creator!\nType 'exit' at any prompt to quit.")
            infra_logger.info("[MAIN] Starting interactive VM creation session")
            
            while True:
                try:
                    machine = create_machine()
                    if not machine:
                        infra_logger.warning("[MAIN] Machine creation failed, continuing to next iteration")
                        continue

                    install = input("Do you want to install a service on this machine? (y/n): ").strip().lower()
                    if install in ("y", "yes"):
                        infra_logger.info("[MAIN] User requested service installation")
                        result = service_installer()
                        if result:
                            infra_logger.info("[MAIN] Service installation completed successfully")
                        else:
                            infra_logger.warning("[MAIN] Service installation failed or was cancelled")
                    else:
                        infra_logger.info("[MAIN] User declined service installation")

                    again = input("Create another machine? (y/n): ").strip().lower()
                    if again not in ("y", "yes"):
                        infra_logger.info("[MAIN] User chose to exit")
                        print("Exiting.")
                        break
                        
                except KeyboardInterrupt:
                    infra_logger.info("[MAIN] User interrupted the process with Ctrl+C")
                    print("\nProcess interrupted by user.")
                    break
                except Exception as e:
                    infra_logger.error(f"[MAIN] Unexpected error in main loop: {e}", exc_info=True)
                    print(f"An error occurred: {e}")
                    continue
                    
    except Exception as e:
        infra_logger.error(f"[MAIN] Critical error in main execution: {e}", exc_info=True)
        print(f"Critical error: {e}")
    finally:
        infra_logger.info("====================================== Infrastructure Simulator Ended ========================================")
    
   
