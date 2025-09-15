========================================
    DIET PLANNER - COMPLETE SETUP
========================================

This folder contains everything needed to install and run the Diet Planner project on a brand new Windows laptop.

QUICK START:
1. Right-click "INSTALL.bat" and select "Run as Administrator"
2. Wait for installation to complete
3. VS Code will open automatically with your project

WHAT THIS INSTALLS:
✓ Git (version control)
✓ Python 3.11 (programming language)
✓ VS Code (code editor with extensions)
✓ All Python libraries needed for the project
✓ Virtual environment for the project

FILES IN THIS FOLDER:
- INSTALL.bat          → One-click installer (run as Administrator)
- requirements.txt     → Python package dependencies
- download_installers.ps1 → Downloads installer files (optional)

AFTER INSTALLATION:
1. VS Code will open with your project
2. Select Python interpreter: Ctrl+Shift+P → "Python: Select Interpreter" → choose "venv\Scripts\python.exe"
3. Open diet_planner.py to start coding!

TROUBLESHOOTING:
- If installation fails, make sure you're running as Administrator
- If Python interpreter isn't found, restart VS Code after installation
- If you get permission errors, run PowerShell as Administrator and execute: Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

That's it! Your Diet Planner project is ready to use.
