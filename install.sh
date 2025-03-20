#!/bin/bash

echo "Installing dependencies..."

# Update package list
sudo apt update && sudo apt upgrade -y

# Install system dependencies
sudo apt install -y python3 python3-pip python3-venv nodejs npm ffmpeg

# Set up Python Virtual Environment
python3 -m venv backend/venv
source backend/venv/bin/activate

# Install Python dependencies
pip install -r backend/requirements.txt

# Install Node.js dependencies
cd frontend
npm install

echo "Installation complete!"
