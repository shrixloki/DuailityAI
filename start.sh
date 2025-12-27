#!/bin/bash

echo "🚀 DUALITY AI - Full Stack Startup (Linux/Mac)"
echo "=============================================="

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found. Please install Python 3.8+"
    exit 1
fi

# Check if Node.js is available
if ! command -v node &> /dev/null; then
    echo "❌ Node.js not found. Please install Node.js from https://nodejs.org/"
    exit 1
fi

echo "✅ Python and Node.js found"
echo ""

# Make the script executable
chmod +x run_full_stack.py

# Run the full stack script
python3 run_full_stack.py "$@"