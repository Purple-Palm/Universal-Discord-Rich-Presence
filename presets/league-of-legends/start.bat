@echo off
cd ..
cd ..
cd venv\Scripts
call activate.bat
cd ..\..
cd presets
cd league-of-legends
python __main__.py

pause
