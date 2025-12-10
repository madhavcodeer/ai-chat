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

echo "Installing Backend Dependencies..."
pip install -r requirements.txt

echo "Build Finished!"
