#!/bin/bash

# ChironX Quick Start Script
echo "🚀 Starting ChironX..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies if needed
echo "📥 Installing dependencies..."
pip install flask flask-cors google-cloud-aiplatform google-cloud-texttospeech google-cloud-firestore google-cloud-storage google-generativeai opencv-python numpy

# Start the interactive startup script
echo "🎯 Starting ChironX..."
python start_chironx.py 