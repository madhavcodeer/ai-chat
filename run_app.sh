#!/usr/bin/env bash

echo "Current Directory: $(pwd)"
ls -la

if [ -f "main.py" ]; then
    echo "Found main.py in current directory. Running..."
    python main.py
elif [ -f "backend/main.py" ]; then
    echo "Found backend/main.py. Running..."
    python backend/main.py
else
    echo "ERROR: Could not find main.py!"
    exit 1
fi
