@echo off
echo ========================================
echo   AI Chat Application - Frontend Start
echo ========================================
echo.

cd frontend

echo [1/2] Installing dependencies...
if not exist node_modules (
    echo Installing npm packages...
    call npm install
) else (
    echo Dependencies already installed.
)

echo.
echo [2/2] Starting development server...
echo Frontend will run at: http://localhost:5173
echo.
echo Press Ctrl+C to stop the frontend server
echo ========================================
echo.

call npm run dev
