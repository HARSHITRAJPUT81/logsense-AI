@echo off
title LogSense AI Installer
color 0A

echo.
echo  ====================================
echo   LogSense AI - Windows Installer
echo  ====================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo  Python not found. Downloading Python...
    curl -o python_installer.exe https://www.python.org/ftp/python/3.12.0/python-3.12.0-amd64.exe
    echo  Installing Python...
    python_installer.exe /quiet InstallAllUsers=1 PrependPath=1
    del python_installer.exe
    echo  Python installed successfully!
)

:: Check if Git is installed
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo  Git not found. Downloading Git...
    curl -o git_installer.exe https://github.com/git-for-windows/git/releases/download/v2.43.0.windows.1/Git-2.43.0-64-bit.exe
    git_installer.exe /VERYSILENT /NORESTART
    del git_installer.exe
    echo  Git installed successfully!
)

:: Clone the repo
if not exist "logsense" (
    echo  Downloading LogSense AI...
    git clone https://github.com/HARSHITRAJPUT81/logsense.git
)

cd logsense

:: Setup virtual environment
echo  Setting up Python environment...
python -m venv venv
call venv\Scripts\activate.bat
pip install -r requirements.txt -q
pip install -e . -q
echo  Libraries installed!

:: Ask for API key
echo.
echo  You need a FREE Groq API key
echo  1. Go to: https://console.groq.com
echo  2. Sign up free with Google
echo  3. Click API Keys - Create API Key
echo  4. Copy the key starting with gsk_...
echo.
set /p GROQ_KEY="Paste your Groq API key here: "

:: Create .env file
echo GROQ_API_KEY=%GROQ_KEY% > .env
echo LOGSENSE_MODEL=claude-sonnet-4-6 >> .env
echo LOGSENSE_DB=%USERPROFILE%\.logsense\history.db >> .env

:: Add to PATH
setx PATH "%PATH%;%CD%\venv\Scripts" /M >nul 2>&1

echo.
echo  LogSense AI installed successfully!
echo.
echo  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo   Available Commands:
echo.
echo   Analyze Windows System logs:
echo   logsense analyze "%SYSTEMROOT%\System32\winevt\Logs\System.evtx"
echo.
echo   Analyze Application logs:
echo   logsense analyze "%SYSTEMROOT%\System32\winevt\Logs\Application.evtx"
echo.
echo   See history:
echo   logsense report
echo  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.
echo  Please restart your terminal before using logsense
echo.
pause





@echo off
title LogSense AI Installer
color 0A

echo.
echo  ====================================
echo   LogSense AI - Windows Installer
echo  ====================================
echo.

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo  Python not found. Downloading...
    curl -o python_installer.exe https://www.python.org/ftp/python/3.12.0/python-3.12.0-amd64.exe
    python_installer.exe /quiet InstallAllUsers=1 PrependPath=1
    del python_installer.exe
    echo  Python installed!
)

git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo  Git not found. Downloading...
    curl -o git_installer.exe https://github.com/git-for-windows/git/releases/download/v2.43.0.windows.1/Git-2.43.0-64-bit.exe
    git_installer.exe /VERYSILENT /NORESTART
    del git_installer.exe
    echo  Git installed!
)

if not exist "logsense" (
    git clone https://github.com/HARSHITRAJPUT81/logsense.git
)

cd logsense
python -m venv venv
call venv\Scripts\activate.bat
pip install -r requirements.txt -q
pip install -e . -q

echo.
echo  You need a FREE Groq API key
echo  1. Go to: https://console.groq.com
echo  2. Sign up free with Google
echo  3. Click API Keys - Create API Key
echo  4. Copy key starting with gsk_...
echo.
set /p GROQ_KEY="Paste your Groq API key: "

echo GROQ_API_KEY=%GROQ_KEY% > .env
echo LOGSENSE_MODEL=claude-sonnet-4-6 >> .env
echo LOGSENSE_DB=%USERPROFILE%\.logsense\history.db >> .env

setx PATH "%PATH%;%CD%\venv\Scripts" /M >nul 2>&1

echo.
echo  ====================================
echo   LogSense AI installed successfully!
echo  ====================================
echo.
echo  Commands to use:
echo.
echo  Analyze Windows System logs:
echo  logsense analyze "%SYSTEMROOT%\System32\winevt\Logs\System.evtx"
echo.
echo  Analyze Application logs:
echo  logsense analyze "%SYSTEMROOT%\System32\winevt\Logs\Application.evtx"
echo.
echo  See history:
echo  logsense report
echo.
echo  Restart your terminal before using logsense!
echo.
pause