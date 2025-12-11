#!/usr/bin/env bash

echo "Current Directory: $(pwd)"
ls -la

# Self-Healing: Check if frontend is built
if [ ! -d "frontend/dist" ] && [ ! -d "../frontend/dist" ]; then
    echo "⚠️ Frontend build missing! Attempting to build now..."
    cd frontend
    npm install
    npm run build
    cd ..
    echo "✅ Frontend built successfully during startup."
fi

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
