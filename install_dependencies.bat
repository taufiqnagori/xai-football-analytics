@echo off
echo ========================================
echo Installing Dependencies
echo ========================================
echo.

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install all requirements
echo Installing packages from requirements.txt...
echo.
pip install -r requirements.txt

echo.
echo ========================================
echo Installation complete!
echo ========================================
pause
