@echo off
title Personal Expense Tracker
echo Starting Personal Expense Tracker...

:: Check if virtual environment exists
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
) else (
    echo [ERROR] Virtual environment not found in .\venv
    echo Please create it using: python -m venv venv
    pause
    exit /b 1
)

:: Automatically open default browser after a short delay in background
start "" cmd /c "timeout /t 2 /nobreak >nul && start http://127.0.0.1:8000"

:: Start Uvicorn server
echo Server running at http://127.0.0.1:8000
echo Press CTRL+C to stop the server.
echo.
uvicorn app:app --reload --port 8000
