#!/bin/bash
# Local environment setup script for Linux/macOS

set -e

echo "=== Setting up AI Fashion Editor local environment ==="

# 1. Create python virtual environment
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
else
    echo "Virtual environment already exists."
fi

# 2. Activate virtual environment
source .venv/bin/activate

# 3. Upgrade pip and install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
else
    echo "WARNING: requirements.txt not found. Skipping dependency installation."
fi

# 4. Install pre-commit hooks
echo "Setting up pre-commit..."
if command -v pre-commit &> /dev/null; then
    pre-commit install
else
    pip install pre-commit
    pre-commit install
fi

# 5. Run hardware system verification
if [ -f "scripts/check_system.py" ]; then
    echo "Verifying hardware requirements..."
    python scripts/check_system.py || echo "Warning: hardware system verification script failed, check output manually."
fi

echo "=== Setup Complete ==="
