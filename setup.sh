#!/bin/bash

echo "Setting up VORIS..."

# System dependencies
echo "Installing system dependencies..."
sudo apt install -y mpg123 python3-venv python3-pip portaudio19-dev python3-pyaudio libasound2-dev zstd

# Virtual environment
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate and install Python packages
echo "Installing Python packages..."
source .venv/bin/activate
pip install --upgrade pip
pip install pyaudio
pip install -r requirements.txt

# Install Ollama if not present and enough RAM available
TOTAL_RAM=$(free -m | awk '/^Mem:/{print $2}')
if ! command -v ollama &> /dev/null; then
    if [ "$TOTAL_RAM" -gt 3000 ]; then
        echo "Installing Ollama..."
        curl -fsSL https://ollama.com/install.sh | sh
        echo "Pulling VORIS coding model..."
        ollama serve > /dev/null 2>&1 &
        sleep 3
        ollama pull qwen2.5-coder:3b
    else
        echo "Not enough RAM for Ollama on this device. Coding brain will use search fallback."
    fi
else
    echo "Ollama already installed."
fi

echo ""
echo "Setup complete. Run VORIS with:"
echo "source .venv/bin/activate && ollama serve > /dev/null 2>&1 & python voris.py"