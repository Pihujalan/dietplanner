@echo off
title Diet Planner - Quick Install
color 0A

echo.
echo  ========================================
echo     DIET PLANNER - QUICK INSTALL
echo  ========================================
echo.
echo  This will install everything needed:
echo  - Git (version control)
echo  - Python 3.11 (programming language)  
echo  - VS Code (code editor)
echo  - All Python libraries
echo.
echo  Press any key to start installation...
pause >nul

echo.
echo  Starting installation...
echo.

REM Check for admin privileges
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo  ERROR: This needs Administrator privileges
    echo  Please right-click and "Run as Administrator"
    pause
    exit /b 1
)

REM Install Git
echo  [1/4] Installing Git...
where git >nul 2>&1
if %errorLevel% neq 0 (
    echo  Downloading and installing Git...
    powershell -Command "& {Invoke-WebRequest -Uri 'https://github.com/git-for-windows/git/releases/download/v2.43.0.windows.1/Git-2.43.0-64-bit.exe' -OutFile 'installers\Git-2.43.0-64-bit.exe'; Start-Process -FilePath 'installers\Git-2.43.0-64-bit.exe' -ArgumentList '/VERYSILENT','/NORESTART' -Wait}"
    echo  Git installed!
) else (
    echo  Git already installed
)

REM Install Python
echo  [2/4] Installing Python...
where python >nul 2>&1
if %errorLevel% neq 0 (
    echo  Downloading and installing Python...
    powershell -Command "& {Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.11.7/python-3.11.7-amd64.exe' -OutFile 'installers\python-3.11.7-amd64.exe'; Start-Process -FilePath 'installers\python-3.11.7-amd64.exe' -ArgumentList '/quiet','InstallAllUsers=1','PrependPath=1','Include_test=0' -Wait}"
    echo  Python installed!
    echo  Refreshing environment...
    call refreshenv
) else (
    echo  Python already installed
)

REM Install VS Code
echo  [3/4] Installing VS Code...
where code >nul 2>&1
if %errorLevel% neq 0 (
    echo  Downloading and installing VS Code...
    powershell -Command "& {Invoke-WebRequest -Uri 'https://code.visualstudio.com/sha/download?build=stable&os=win32-x64-user' -OutFile 'installers\VSCodeUserSetup-x64-1.84.2.exe'; Start-Process -FilePath 'installers\VSCodeUserSetup-x64-1.84.2.exe' -ArgumentList '/VERYSILENT','/NORESTART','/MERGETASKS=!runcode' -Wait}"
    echo  VS Code installed!
) else (
    echo  VS Code already installed
)

REM Setup project
echo  [4/4] Setting up project...
cd /d "%~dp0.."

if not exist venv (
    echo  Creating virtual environment...
    python -m venv venv
)

echo  Installing Python packages...
call venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r setup\requirements.txt

echo  Installing VS Code extensions...
where code >nul 2>&1
if %errorLevel% == 0 (
    code --install-extension ms-python.python --force
    code --install-extension ms-python.vscode-pylance --force
    code --install-extension ms-toolsai.jupyter --force
    code --install-extension ms-python.flake8 --force
    code --install-extension ms-python.black-formatter --force
)

echo.
echo  ========================================
echo        INSTALLATION COMPLETE!
echo  ========================================
echo.
echo  Everything is ready! VS Code will open now.
echo.
pause
start code "%~dp0.."
