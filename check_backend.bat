@echo off
echo Checking if backend is running...
echo.

call venv\Scripts\activate.bat
python -c "import requests; r = requests.get('http://127.0.0.1:8000/health', timeout=2); print('Backend is running!'); print(r.json())" 2>nul

if errorlevel 1 (
    echo.
    echo Backend is NOT running!
    echo.
    echo To start the backend, run:
    echo   run_backend.bat
    echo.
    echo Or manually:
    echo   venv\Scripts\activate
    echo   uvicorn backend.main:app --reload
) else (
    echo.
    echo Backend is running successfully!
)

pause
