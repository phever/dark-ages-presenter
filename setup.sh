#!/bin/bash
# Setup script for Dark Ages Presenter

echo "Setting up Dark Ages Presenter..."

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Make main script executable
chmod +x main.py

echo "Setup complete!"
echo ""
echo "Usage:"
echo "  source venv/bin/activate"
echo "  python main.py <text_file> [--delay 0.1]"
