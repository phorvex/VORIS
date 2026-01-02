#!/bin/bash
# Quick interactive test of VORIS with pre-filled commands

echo "Testing VORIS with Ollama integration..."
echo ""

# Run VORIS with test commands
python3 voris_advanced.py <<EOF
what is your name
who are you
bye
EOF
