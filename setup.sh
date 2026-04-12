#!/bin/bash

echo "Setting up VORIS..."

# System dependencies
echo "Installing system dependencies..."
sudo apt install -y mpg123 python3-venv python3-pip

# Virtual environment
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate and install Python packages
echo "Installing Python packages..."
source .venv/bin/activate
pip install -r requirements.txt

echo ""
echo "Setup complete. Run VORIS with:"
echo "source .venv/bin/activate && python voris.py"