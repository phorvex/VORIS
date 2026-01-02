#!/bin/bash
# Quick test script for VORIS new features

echo "╔══════════════════════════════════════════════════════════╗"
echo "║              VORIS Quick Feature Test                   ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

cd /home/phorvex/LLM/VORIS/VORIS

# Activate virtual environment
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "✓ Virtual environment activated"
else
    echo "✗ Virtual environment not found"
    exit 1
fi

# Run comprehensive tests
echo ""
echo "Running comprehensive feature tests..."
echo ""
python3 test_new_features.py

echo ""
echo "Test complete! Check results above."
echo ""
echo "To start VORIS interactively:"
echo "  python3 voris_advanced.py"
echo ""
echo "To use voice mode:"
echo "  python3 voris_advanced.py --voice"
echo ""
