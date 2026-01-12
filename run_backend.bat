@echo off
echo ========================================
echo Starting Football XAI Backend API
echo ========================================
echo.

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Start the FastAPI server
echo Starting FastAPI server on http://127.0.0.1:8000
echo Press Ctrl+C to stop the server
echo.
uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000

pause
