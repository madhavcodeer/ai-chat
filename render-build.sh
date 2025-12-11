#!/usr/bin/env bash
# exit on error
set -o errexit

echo "Build Start: Upgrading pip and build tools..."
pip install --upgrade pip setuptools wheel

echo "Building Frontend..."
cd frontend
npm install
npm run build
cd ..

# Ensure we stay in root
echo "Installing Backend Dependencies..."
pip install -r requirements.txt

# Verify build output
if [ -d "frontend/dist" ]; then
  echo "✅ Frontend build successful"
else
  echo "❌ Frontend build failed - Creating empty dist to prevent crash"
  mkdir -p frontend/dist
  echo "<h1>Build Failed</h1>" > frontend/dist/index.html
fi

echo "Build Finished!"
