@echo off
echo ========================================
echo AI Image Generator - Quick Start
echo ========================================
echo.

echo Activating virtual environment (if exists)...
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
)

echo.
echo Starting Streamlit application...
echo.
echo The app will open in your browser at http://localhost:8501
echo.
echo Press Ctrl+C to stop the application
echo.

streamlit run app.py

pause
