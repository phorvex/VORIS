#!/bin/bash

echo "Setting up VORIS..."

# System dependencies
echo "Installing system dependencies..."
sudo apt install -y mpg123 python3-venv python3-pip portaudio19-dev python3-pyaudio libasound2-dev

# Virtual environment
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate and install Python packages
echo "Installing Python packages..."
source .venv/bin/activate

# Install pyaudio separately first using system headers
pip install --upgrade pip
pip install pyaudio

# Install remaining packages
pip install -r requirements.txt

# Install Ollama if not present
if ! command -v ollama &> /dev/null; then
    echo "Installing Ollama..."
    curl -fsSL https://ollama.com/install.sh | sh
    echo "Pulling VORIS coding model..."
    ollama serve > /dev/null 2>&1 &
    sleep 3
    ollama pull qwen2.5-coder:3b
else
    echo "Ollama already installed."
fi

echo ""
echo "Setup complete. Run VORIS with:"
echo "source .venv/bin/activate && ollama serve > /dev/null 2>&1 & python voris.py"