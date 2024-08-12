@echo off
echo Starting main.bat...
::taskkill /F /IM python.exe /T
::taskkill /F /IM pythonw.exe /T
::taskkill /F /IM python3.11.exe /T
echo Current working directory: %cd%
cd venv\Scripts
call activate.bat
cd ..\..
cd lib
python updater.py

pause

