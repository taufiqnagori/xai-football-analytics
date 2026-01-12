@echo off
echo ========================================
echo Starting Football XAI Frontend
echo ========================================
echo.

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Start Streamlit frontend
echo Starting Streamlit frontend on http://localhost:8501
echo Press Ctrl+C to stop the server
echo.
streamlit run frontend/app.py

pause
