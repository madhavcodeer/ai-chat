#!/usr/bin/env bash
# exit on error
set -o errexit

echo "Build Start: Upgrading pip and build tools..."
pip install --upgrade pip setuptools wheel

# Check if pre-built files exist (from git)
if [ -d "frontend/dist" ]; then
  echo "✅ Pre-built frontend found. Skipping npm install."
else
  # Only try building if absolutely necessary (fallback)
  echo "⚠️ Pre-built frontend MISSING. This might fail on Python runtime."
  if command -v npm &> /dev/null; then
      cd frontend
      npm install
      npm run build
      cd ..
  fi
fi

# Ensure we stay in root and install backend deps
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

# Fix for user's specific Render setting expecting 'ai' directory
echo "Copying to 'ai' directory to match Render settings..."
rm -rf ai
cp -r frontend/dist ai

echo "Build Finished!"
