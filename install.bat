@echo off
REM ============================================================
REM NeuralTrade AI - Windows Installer
REM Developed by issu321
REM https://github.com/issu321/Stock-Price-Prediction-Using-Machine-Learning
REM ============================================================

echo ============================================
echo    NeuralTrade AI - Windows Installer
echo    Developed by issu321
echo ============================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH.
    echo Please install Python 3.11+ from https://python.org and try again.
    pause
    exit /b 1
)

echo ✅ Python found.

REM Create virtual environment
if not exist venv (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo 🔌 Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo ⬆️  Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies
echo 📥 Installing dependencies...
pip install -r requirements.txt

echo.
echo ============================================
echo ✅ Installation complete!
echo ============================================
echo.
echo 🚀 Launching NeuralTrade AI...
echo.

REM Launch Streamlit
streamlit run app.py

pause
