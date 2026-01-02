#!/bin/bash
# VORIS Web Setup Launcher
# Starts the interactive web-based configuration interface

echo "🚀 Starting VORIS Web Setup..."
echo "================================"

# Navigate to the VORIS directory
cd "$(dirname "$0")"

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    echo "✓ Activating virtual environment..."
    source venv/bin/activate
fi

# Install Flask if not already installed
echo "✓ Checking Flask installation..."
pip list | grep -q "^Flask " || {
    echo "📦 Installing Flask..."
    pip install flask
}

# Start the web setup server
echo ""
echo "🌐 Starting web server on http://localhost:8080"
echo "================================"
echo "Open your browser and navigate to:"
echo ""
echo "    http://localhost:8080"
echo ""
echo "Press Ctrl+C to stop the server when done."
echo ""

python3 web_setup.py
