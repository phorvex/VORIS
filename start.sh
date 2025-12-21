#!/bin/bash

# Voris AI Quick Start Script

echo "╔══════════════════════════════════════════════════════════╗"
echo "║   VORIS AI - Installation and Setup                     ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

# Check Python version
echo "[1/5] Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.7 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "✅ Python $PYTHON_VERSION found"
echo ""

# Create virtual environment (optional but recommended)
echo "[2/5] Setting up virtual environment (optional)..."
read -p "Create a virtual environment? (recommended) [Y/n]: " create_venv

if [[ $create_venv != "n" && $create_venv != "N" ]]; then
    if [ ! -d "venv" ]; then
        python3 -m venv venv
        if [ $? -eq 0 ]; then
            echo "✅ Virtual environment created"
        else
            echo "⚠️  Virtual environment creation failed"
            echo "   Continuing with system Python..."
        fi
    else
        echo "ℹ️  Virtual environment already exists"
    fi
    
    if [ -f "venv/bin/activate" ]; then
        source venv/bin/activate
        echo "✅ Virtual environment activated"
    else
        echo "⚠️  Could not activate virtual environment"
        echo "   Using system Python instead"
    fi
else
    echo "⚠️  Skipping virtual environment"
fi
echo ""

# Install dependencies
echo "[3/5] Installing dependencies..."
if [ -f "venv/bin/pip" ]; then
    venv/bin/pip install -r requirements.txt
else
    # Try with --user flag if system is externally managed
    pip install -r requirements.txt 2>/dev/null || pip install --user -r requirements.txt 2>/dev/null || {
        echo "⚠️  Unable to install with pip. Trying alternative methods..."
        echo ""
        echo "Your system uses externally-managed Python. Options:"
        echo "1. Create virtual environment manually:"
        echo "   python3 -m venv venv"
        echo "   source venv/bin/activate"
        echo "   pip install -r requirements.txt"
        echo ""
        echo "2. Install system packages (Kali/Debian):"
        echo "   sudo apt install python3-psutil python3-pyttsx3 python3-speechrecognition"
        echo ""
        echo "3. Use pipx (if available):"
        echo "   pipx install voris"
        echo ""
    }
fi

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully"
else
    echo "⚠️  Some dependencies may have failed to install"
    echo "   You can manually install them later with: pip install -r requirements.txt"
fi
echo ""

# Check for audio support
echo "[4/5] Checking audio support..."
if python3 -c "import pyaudio" 2>/dev/null; then
    echo "✅ Audio support available"
else
    echo "⚠️  PyAudio not installed. Voice features will be limited."
    echo "   On Linux: sudo apt-get install portaudio19-dev python3-pyaudio"
    echo "   On macOS: brew install portaudio"
fi
echo ""

# Setup complete
echo "[5/5] Setup complete!"
echo ""
echo "╔══════════════════════════════════════════════════════════╗"
echo "║   Ready to launch VORIS!                                ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""
echo "To start Voris:"
echo "  Text mode:  python3 voris_advanced.py"
echo "  Voice mode: python3 voris_advanced.py --voice"
echo ""
echo "For basic version:"
echo "  python3 voris_ai.py"
echo ""

# Ask if user wants to run now
read -p "Would you like to start Voris now? [Y/n]: " start_now

if [[ $start_now != "n" && $start_now != "N" ]]; then
    echo ""
    echo "Starting Voris in text mode..."
    echo ""
    python3 voris_advanced.py
fi
