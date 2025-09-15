# Diet Planner - Automated Setup Script for Windows
# Run this script as Administrator

Write-Host "=== Diet Planner Setup Script ===" -ForegroundColor Green
Write-Host "Setting up everything needed for Diet Planner project..." -ForegroundColor Yellow

# Check if running as Administrator
if (-NOT ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Host "This script requires Administrator privileges. Please run PowerShell as Administrator." -ForegroundColor Red
    exit 1
}

# Function to check if a command exists
function Test-CommandExists {
    param($command)
    $null = Get-Command $command -ErrorAction SilentlyContinue
    return $?
}

# Step 1: Install Git
Write-Host "`n1. Checking Git installation..." -ForegroundColor Cyan
if (Test-CommandExists git) {
    Write-Host "Git is already installed: $(git --version)" -ForegroundColor Green
} else {
    Write-Host "Git not found. Please install Git manually from https://git-scm.com/download/win" -ForegroundColor Red
    Write-Host "After installation, restart this script." -ForegroundColor Yellow
    exit 1
}

# Step 2: Install Python
Write-Host "`n2. Checking Python installation..." -ForegroundColor Cyan
if (Test-CommandExists python) {
    $pythonVersion = python --version
    Write-Host "Python is installed: $pythonVersion" -ForegroundColor Green
    
    # Check if version is 3.9+
    $version = [version]($pythonVersion -replace 'Python ', '')
    if ($version.Major -ge 3 -and $version.Minor -ge 9) {
        Write-Host "Python version is compatible (3.9+)" -ForegroundColor Green
    } else {
        Write-Host "Python version is too old. Please install Python 3.9+ from https://www.python.org/downloads/" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "Python not found. Please install Python 3.9+ from https://www.python.org/downloads/" -ForegroundColor Red
    Write-Host "Make sure to check 'Add Python to PATH' during installation!" -ForegroundColor Yellow
    exit 1
}

# Step 3: Install pip
Write-Host "`n3. Checking pip installation..." -ForegroundColor Cyan
if (Test-CommandExists pip) {
    Write-Host "pip is installed: $(pip --version)" -ForegroundColor Green
} else {
    Write-Host "Installing pip..." -ForegroundColor Yellow
    python -m ensurepip --upgrade
}

# Step 4: Upgrade pip
Write-Host "`n4. Upgrading pip..." -ForegroundColor Cyan
python -m pip install --upgrade pip

# Step 5: Install VS Code if not installed
Write-Host "`n5. Checking VS Code installation..." -ForegroundColor Cyan
if (Test-CommandExists code) {
    Write-Host "VS Code is installed" -ForegroundColor Green
} else {
    Write-Host "VS Code not found. Please install VS Code from https://code.visualstudio.com/" -ForegroundColor Red
    Write-Host "After installation, restart this script." -ForegroundColor Yellow
}

# Step 6: Create virtual environment
Write-Host "`n6. Creating virtual environment..." -ForegroundColor Cyan
$projectPath = Split-Path -Parent $PSScriptRoot
$venvPath = Join-Path $projectPath "venv"

if (Test-Path $venvPath) {
    Write-Host "Virtual environment already exists" -ForegroundColor Yellow
} else {
    Write-Host "Creating virtual environment at: $venvPath" -ForegroundColor Yellow
    python -m venv $venvPath
}

# Step 7: Activate virtual environment and install dependencies
Write-Host "`n7. Installing project dependencies..." -ForegroundColor Cyan
$activateScript = Join-Path $venvPath "Scripts\Activate.ps1"

if (Test-Path $activateScript) {
    Write-Host "Activating virtual environment..." -ForegroundColor Yellow
    & $activateScript
    
    Write-Host "Installing dependencies from requirements.txt..." -ForegroundColor Yellow
    pip install -r requirements.txt
    
    Write-Host "Dependencies installed successfully!" -ForegroundColor Green
} else {
    Write-Host "Failed to create virtual environment. Please run manually:" -ForegroundColor Red
    Write-Host "python -m venv venv" -ForegroundColor Yellow
    Write-Host "venv\Scripts\activate" -ForegroundColor Yellow
    Write-Host "pip install -r requirements.txt" -ForegroundColor Yellow
}

# Step 8: Install VS Code extensions
Write-Host "`n8. Installing VS Code extensions..." -ForegroundColor Cyan
if (Test-CommandExists code) {
    $extensions = @(
        "ms-python.python",
        "ms-python.vscode-pylance", 
        "ms-toolsai.jupyter",
        "ms-python.flake8",
        "ms-python.black-formatter"
    )
    
    foreach ($extension in $extensions) {
        Write-Host "Installing extension: $extension" -ForegroundColor Yellow
        code --install-extension $extension --force
    }
    Write-Host "VS Code extensions installed!" -ForegroundColor Green
} else {
    Write-Host "VS Code not found. Please install extensions manually after installing VS Code." -ForegroundColor Yellow
}

# Step 9: Setup complete
Write-Host "`n=== Setup Complete! ===" -ForegroundColor Green
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Open VS Code" -ForegroundColor White
Write-Host "2. Open the project folder: $projectPath" -ForegroundColor White
Write-Host "3. Select Python interpreter: Ctrl+Shift+P -> 'Python: Select Interpreter' -> Choose venv\Scripts\python.exe" -ForegroundColor White
Write-Host "4. Open diet_planner.py and start coding!" -ForegroundColor White

Write-Host "`nTo activate virtual environment in future sessions:" -ForegroundColor Cyan
Write-Host "cd $projectPath" -ForegroundColor White
Write-Host "venv\Scripts\activate" -ForegroundColor White
