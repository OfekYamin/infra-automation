#!/bin/bash

BASE_DIR="$(dirname "$(dirname "$(realpath "$0")")")"
LOGS_PATH="$BASE_DIR/logs"
PROVISIONING_LOG="$LOGS_PATH/provisioning.log"


# Simple logging function
log_message() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - INFO - $1" >> "$PROVISIONING_LOG"
    echo "$1"
}

# Define available services
declare -A services
services["nginx"]="true"
services["docker"]="true"
services["terraform"]="true"

# Service installation loop
while true; do
    # Read user input
    if ! read -p "Enter the service you want to install (Nginx, Docker, Terraform): " service; then
        log_message "ERROR: Failed to read user input"
        echo "Error: Failed to read input. Please try again."
        continue
    fi

    # Convert input to lowercase
    service="${service,,}"

    # Exit check
    if [[ "$service" == "exit" ]]; then
        log_message "INFO: User requested exit"
        echo "Exiting service installer."
        exit 99
    fi

    # Check for empty input
    if [[ -z "$service" ]]; then
        log_message "ERROR: Empty input received"
        echo "Error: Input cannot be empty. Please enter one of: ${!services[@]}"
        continue
    fi

    # Check if service is valid
    if [[ ! -v services["$service"] ]]; then
        log_message "ERROR: Invalid service requested: $service"
        echo "Error: '$service' is not a recognized service. Please choose from: ${!services[@]}"
        continue
    fi

    # Log selected service
    log_message "Selected service: $service"

    # Simulated installation
    case "$service" in
        "nginx")
            echo "Checking if Nginx is already installed..."
            sleep 2
            echo "Installing Nginx..."
            sleep 2
            echo "Checking dependencies..."
            sleep 2
            ;;
        "docker")
            echo "Checking if Docker is already installed..."
            sleep 2
            echo "Installing Docker..."
            sleep 2
            echo "Checking dependencies..."
            sleep 2
            ;;
        "terraform")
            echo "Checking if Terraform is already installed..."
            sleep 2
            echo "Installing Terraform..."
            sleep 2
            echo "Checking dependencies..."
            sleep 2
            ;;
    esac

    # Log success
    log_message "$service installation completed successfully."
    break
done


