@echo off
echo ===============================
echo        VORIS Setup - Windows
echo ===============================

:: Check Python 3.11
echo Checking Python 3.11...
py -3.11 --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python 3.11 not found. Installing...
    py install 3.11
)

:: Create venv
echo Creating virtual environment...
if not exist ".venv" (
    py -3.11 -m venv .venv
)

:: Activate and install
echo Installing Python packages...
call .venv\Scripts\activate.bat
pip install --upgrade pip
pip install pyaudio
pip install windows-curses

:: Remove Linux only packages from requirements
echo Installing requirements...
pip install -r requirements.txt

:: Check mpg123
echo Checking mpg123...
mpg123 --version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo mpg123 not found.
    echo Please download from https://www.mpg123.de/download.shtml
    echo Extract to C:\mpg123 and add to PATH
    echo Then run this script again.
    pause
    exit /b
)

:: Install Ollama
echo Checking Ollama...
ollama --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing Ollama...
    winget install Ollama.Ollama
    echo Waiting for Ollama to install...
    timeout /t 10
)

:: Pull coding model
echo Pulling VORIS coding model...
start /b ollama serve
timeout /t 5
ollama pull qwen2.5-coder:3b

:: Check .env
if not exist ".env" (
    echo.
    echo WARNING: .env file not found.
    echo Create .env with your Twilio credentials before running VORIS.
    echo See VORIS documentation for details.
)

echo.
echo ===============================
echo        Setup Complete
echo ===============================
echo.
echo To run VORIS:
echo   .venv\Scripts\activate
echo   python voris.py
echo.
echo To run with voice and mic:
echo   python voris.py --voice --mic
echo.
pause