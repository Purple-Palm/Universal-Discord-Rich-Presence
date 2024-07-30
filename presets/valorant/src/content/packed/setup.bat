@echo off
del unpack.bat
echo Setting things up...

echo Version: 3.8 > version.yml

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

:: Create origcut folder
set "origcut_path=%cd%\origcut"
if not exist "%origcut_path%" (
    mkdir "%origcut_path%"
)

:: Find and copy the original Discord shortcut to origcut
set "user_profile=%USERPROFILE%"
set "start_menu_path=%user_profile%\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Discord Inc"
set "discord_shortcut_name=Discord.lnk"

if exist "%start_menu_path%\%discord_shortcut_name%" (
    copy "%start_menu_path%\%discord_shortcut_name%" "%origcut_path%\%discord_shortcut_name%" /Y
)

:: Run the second setup script
python setup-step2.py

endlocal
