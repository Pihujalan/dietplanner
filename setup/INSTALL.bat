@echo off
echo ========================================
echo    DIET PLANNER - ONE CLICK INSTALL
echo ========================================
echo.
echo This will install everything needed for the Diet Planner project
echo Press any key to continue or close this window to cancel...
pause > nul

echo.
echo [1/7] Checking for Administrator privileges...
net session >nul 2>&1
if %errorLevel% == 0 (
    echo ✓ Running with Administrator privileges
) else (
    echo ✗ This script requires Administrator privileges
    echo Please right-click and "Run as Administrator"
    pause
    exit /b 1
)

echo.
echo [2/7] Installing Git...
where git >nul 2>&1
if %errorLevel% == 0 (
    echo ✓ Git is already installed
) else (
    echo Installing Git...
    start /wait "" "%~dp0installers\Git-2.43.0-64-bit.exe" /VERYSILENT /NORESTART
    echo ✓ Git installation complete
)

echo.
echo [3/7] Installing Python...
where python >nul 2>&1
if %errorLevel% == 0 (
    echo ✓ Python is already installed
) else (
    echo Installing Python...
    start /wait "" "%~dp0installers\python-3.11.7-amd64.exe" /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
    echo ✓ Python installation complete
    echo Refreshing PATH...
    call refreshenv
)

echo.
echo [4/7] Installing VS Code...
where code >nul 2>&1
if %errorLevel% == 0 (
    echo ✓ VS Code is already installed
) else (
    echo Installing VS Code...
    start /wait "" "%~dp0installers\VSCodeUserSetup-x64-1.84.2.exe" /VERYSILENT /NORESTART /MERGETASKS=!runcode
    echo ✓ VS Code installation complete
)

echo.
echo [5/7] Setting up project environment...
cd /d "%~dp0.."
if not exist venv (
    echo Creating Python virtual environment...
    python -m venv venv
    echo ✓ Virtual environment created
)

echo.
echo [6/7] Installing Python dependencies...
call venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r setup\requirements.txt
echo ✓ Dependencies installed

echo.
echo [7/7] Installing VS Code extensions...
where code >nul 2>&1
if %errorLevel% == 0 (
    code --install-extension ms-python.python --force
    code --install-extension ms-python.vscode-pylance --force
    code --install-extension ms-toolsai.jupyter --force
    code --install-extension ms-python.flake8 --force
    code --install-extension ms-python.black-formatter --force
    echo ✓ VS Code extensions installed
)

echo.
echo ========================================
echo    INSTALLATION COMPLETE!
echo ========================================
echo.
echo Next steps:
echo 1. Open VS Code
echo 2. Open this project folder
echo 3. Select Python interpreter: Ctrl+Shift+P ^> Python: Select Interpreter ^> venv\Scripts\python.exe
echo 4. Start coding!
echo.
echo Press any key to open VS Code with this project...
pause > nul
start code "%~dp0.."
