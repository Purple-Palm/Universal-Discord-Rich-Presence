@echo off
echo Starting exit.bat...
taskkill /F /IM python.exe /T
taskkill /F /IM pythonw.exe /T
taskkill /F /IM python3.11.exe /T
echo Current working directory: %cd%
cd ..
cd ..
call main-start.bat


pause
