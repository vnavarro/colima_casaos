#!/bin/bash

# Check if python3 is installed
check_python_installed() {
    if command -v python3 >/dev/null 2>&1; then
        echo "python3 is installed: $(python3 --version)"
        return 0
    else
        echo "python3 is not installed."
        return 1
    fi
}

# Install python3
install_python() {
    OS_TYPE="$1"
    echo "Installing python3..."
    if [ "$OS_TYPE" = "mac" ]; then
        if ! command -v brew >/dev/null 2>&1; then
            echo "Homebrew is not installed. Please install Homebrew first."
            exit 1
        fi
		echo "Mac detected. Installing python3 using Homebrew."
        brew install python3
    elif [ "$OS_TYPE" = "linux" ]; then
		echo "Linux detected. Trying installing python3 using apt-get."
        sudo apt-get update
        sudo apt-get install -y python3
    else
        echo "Unsupported OS type: $OS_TYPE"
        exit 1
    fi    
}

# Example usage:
# OS_TYPE="mac" # or "linux"
check_python_installed || install_python "$1"