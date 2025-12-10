@echo off
echo ========================================
echo    AI Chat Application - Quick Start
echo ========================================
echo.

echo [1/4] Setting up Backend...
cd backend

echo [2/4] Creating virtual environment...
if not exist venv (
    python -m venv venv
    echo Virtual environment created!
) else (
    echo Virtual environment already exists.
)

echo [3/4] Activating virtual environment and installing dependencies...
call venv\Scripts\activate
pip install -r requirements.txt --quiet

echo [4/4] Creating .env file if it doesn't exist...
if not exist .env (
    copy .env.example .env
    echo .env file created! Please add your GEMINI_API_KEY to backend\.env
) else (
    echo .env file already exists.
)

echo.
echo ========================================
echo Backend setup complete!
echo ========================================
echo.
echo Now starting the backend server...
echo Backend will run at: http://localhost:8000
echo.
echo To start the frontend:
echo   1. Open a new terminal
echo   2. cd frontend
echo   3. npm install
echo   4. npm run dev
echo.
echo Press Ctrl+C to stop the backend server
echo ========================================
echo.

python main.py
