@echo off
echo ========================================
echo Training ML Models
echo ========================================
echo.

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Train models
echo Training all models...
echo.
python backend/train_models.py

echo.
echo ========================================
echo Model training complete!
echo ========================================
pause
