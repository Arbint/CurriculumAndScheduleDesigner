#!/bin/bash

# Check for Python 3.10+
PYTHON=""
for cmd in python3.13 python3.12 python3.11 python3.10 python3 python; do
    if command -v "$cmd" &>/dev/null; then
        if "$cmd" -c "import sys; exit(0 if sys.version_info >= (3,10) else 1)" 2>/dev/null; then
            PYTHON="$cmd"
            break
        fi
    fi
done

if [ -z "$PYTHON" ]; then
    echo "Python 3.10 or newer not found."
    echo "Install it with your package manager, e.g.:"
    echo "  Ubuntu/Debian: sudo apt install python3"
    echo "  Fedora:        sudo dnf install python3"
    echo "  Arch:          sudo pacman -S python"
    exit 1
fi

echo "Using $($PYTHON --version)"

# PySide6 on Linux may need xcb platform libs. Warn if libGL is missing.
if ! ldconfig -p 2>/dev/null | grep -q libGL; then
    echo "Warning: libGL not found. PySide6 may require it."
    echo "  Ubuntu/Debian: sudo apt install libgl1"
    echo "  Fedora:        sudo dnf install mesa-libGL"
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$SCRIPT_DIR/.venv"

# Create virtual environment if it doesn't exist
if [ ! -f "$VENV_DIR/bin/activate" ]; then
    echo "Creating virtual environment..."
    "$PYTHON" -m venv "$VENV_DIR"
fi

# Activate virtual environment
source "$VENV_DIR/bin/activate"

# Check and install dependencies inside venv
echo "Checking dependencies..."
if ! python -c "import PySide6" &>/dev/null; then
    echo "Installing PySide6..."
    python -m pip install PySide6
fi

if ! python -c "import openpyxl" &>/dev/null; then
    echo "Installing openpyxl..."
    python -m pip install openpyxl
fi

# Launch the app
export PYTHONPATH="$SCRIPT_DIR/src"
python -m degreeplaner.CurriculumPlaner
