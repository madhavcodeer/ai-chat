#!/usr/bin/env bash

echo "Current Directory: $(pwd)"
ls -la
echo "Frontend Directory Contents:"
ls -la frontend

# Check tools
echo "Node Version: $(node -v)"
echo "NPM Version: $(npm -v)"

# Self-Healing: Check if frontend is built
if [ ! -d "frontend/dist" ]; then
    echo "⚠️ Frontend build missing/incomplete! Attempting to build now..."
    cd frontend
    echo "Files in frontend before build:"
    ls -la
    npm install
    npm run build
    cd ..
    echo "✅ Frontend build attempt finished."
    echo "Checking for dist again:"
    ls -la frontend/dist || echo "❌ Still no dist folder!"
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
