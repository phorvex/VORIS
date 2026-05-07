#!/bin/bash

echo "==============================="
echo "       VORIS Setup Script      "
echo "==============================="

# Detect OS
if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS=$ID
    OS_LIKE=$ID_LIKE
else
    echo "Cannot detect OS. Exiting."
    exit 1
fi

echo "Detected OS: $OS"

# Install system dependencies based on OS
install_deps() {
    case "$OS" in
        ubuntu|debian|linuxmint|pop)
            echo "Installing dependencies via apt..."
            sudo apt update -y
            sudo apt install -y mpg123 python3-venv python3-pip portaudio19-dev python3-pyaudio libasound2-dev zstd espeak ffmpeg curl
            ;;
        arch|manjaro|endeavouros)
            echo "Installing dependencies via pacman..."
            sudo pacman -Sy --noconfirm mpg123 python python-pip portaudio python-pyaudio alsa-lib zstd espeak-ng ffmpeg curl
            ;;
        fedora|rhel|centos|rocky|alma)
            echo "Installing dependencies via dnf..."
            sudo dnf install -y mpg123 python3 python3-pip portaudio-devel python3-pyaudio alsa-lib-devel zstd espeak ffmpeg curl
            ;;
        opensuse*|suse*)
            echo "Installing dependencies via zypper..."
            sudo zypper install -y mpg123 python3 python3-pip portaudio-devel python3-PyAudio alsa-devel zstd espeak ffmpeg curl
            ;;
        *)
            # Try apt as fallback
            if command -v apt &> /dev/null; then
                echo "Unknown OS, trying apt..."
                sudo apt update -y
                sudo apt install -y mpg123 python3-venv python3-pip portaudio19-dev python3-pyaudio libasound2-dev zstd espeak ffmpeg curl
            elif command -v pacman &> /dev/null; then
                echo "Unknown OS, trying pacman..."
                sudo pacman -Sy --noconfirm mpg123 python python-pip portaudio python-pyaudio alsa-lib zstd espeak-ng ffmpeg curl
            elif command -v dnf &> /dev/null; then
                echo "Unknown OS, trying dnf..."
                sudo dnf install -y mpg123 python3 python3-pip portaudio-devel python3-pyaudio alsa-lib-devel zstd espeak ffmpeg curl
            else
                echo "Could not detect package manager. Install dependencies manually."
            fi
            ;;
    esac
}

install_deps

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
        sleep 5
        ollama pull qwen2.5-coder:3b
    else
        echo "Not enough RAM for Ollama. Coding brain will use search fallback."
    fi
else
    echo "Ollama already installed."
    # Pull model if not present
    if ! ollama list 2>/dev/null | grep -q "qwen2.5-coder"; then
        echo "Pulling VORIS coding model..."
        ollama serve > /dev/null 2>&1 &
        sleep 5
        ollama pull qwen2.5-coder:3b
    fi
fi

echo ""
echo "==============================="
echo "        Setup Complete         "
echo "==============================="
echo ""
echo "To run VORIS:"
echo "  source .venv/bin/activate"
echo "  ollama serve > /dev/null 2>&1 &"
echo "  python3 voris.py"