@echo off
echo Starting main.bat...
echo Current working directory: %cd%
cd venv\Scripts
call activate.bat
cd ..\..
python RPC.py

pause

