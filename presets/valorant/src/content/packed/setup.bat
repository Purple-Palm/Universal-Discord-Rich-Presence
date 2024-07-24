@echo off
del unpack.bat
echo Setting thing up...
:: Check for Python installation
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo No Python found, terminating
    timeout /t 5
    exit /b
)

:: Create a virtual environment
python -m venv venv

:: Activate the virtual environment
call venv\Scripts\activate.bat

:: Install required packages
pip install -r req.txt

:: Write the current working directory to setup.yml
setlocal enabledelayedexpansion
set "escaped_cd=%cd:\=\\%"
echo work_dir: "!escaped_cd!" > setup.yml

:: Run the second setup script
python setup-step2.py
