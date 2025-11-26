@echo off
echo ========================================
echo AI Image Generator - Installation
echo ========================================
echo.

echo Step 1: Creating virtual environment...
python -m venv venv
echo.

echo Step 2: Activating virtual environment...
call venv\Scripts\activate.bat
echo.

echo Step 3: Upgrading pip...
python -m pip install --upgrade pip
echo.

echo Step 4: Installing dependencies...
pip install -r requirements.txt
echo.

echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Download AI model: python utils\model_downloader.py
echo 2. Run application: run_app.bat
echo.

pause
