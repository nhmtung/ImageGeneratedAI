@echo off
rem Local environment setup script for Windows
echo === Setting up AI Fashion Editor local environment ===

rem 1. Create python virtual environment
if not exist .venv (
    echo Creating virtual environment...
    python -m venv .venv
) else (
    echo Virtual environment already exists.
)

rem 2. Activate virtual environment
call .venv\Scripts\activate.bat

rem 3. Upgrade pip and install dependencies
echo Installing dependencies...
python -m pip install --upgrade pip
if exist requirements.txt (
    pip install -r requirements.txt
) else (
    echo WARNING: requirements.txt not found. Skipping dependency installation.
)

rem 4. Install pre-commit hooks
echo Setting up pre-commit...
pip install pre-commit
pre-commit install

rem 5. Run hardware system verification
if exist scripts\check_system.py (
    echo Verifying hardware requirements...
    python scripts\check_system.py
)

echo === Setup Complete ===
pause
