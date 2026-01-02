#!/bin/bash
# Quick test runner for VORIS

echo "╔══════════════════════════════════════════════════════════╗"
echo "║           VORIS Test Suite Runner                       ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

cd "$(dirname "$0")"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "⚠️  Virtual environment not found!"
    echo "Creating it now..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -q pyttsx3 SpeechRecognition psutil requests
    echo "✅ Virtual environment created"
else
    source venv/bin/activate
fi

# Run tests
echo "Running comprehensive test suite..."
echo ""
python3 run_all_tests.py

# Check exit code
if [ $? -eq 0 ]; then
    echo ""
    echo "╔══════════════════════════════════════════════════════════╗"
    echo "║  ✅ All tests passed! VORIS is ready to use!           ║"
    echo "╚══════════════════════════════════════════════════════════╝"
    echo ""
    echo "Start VORIS with: ./start.sh"
    echo "       or: source venv/bin/activate && python3 voris_advanced.py"
else
    echo ""
    echo "╔══════════════════════════════════════════════════════════╗"
    echo "║  ⚠️  Some tests failed. Check output above.            ║"
    echo "╚══════════════════════════════════════════════════════════╝"
fi
