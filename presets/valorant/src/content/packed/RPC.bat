@echo off
echo Starting main.bat...
echo Current working directory: %cd%
cd venv\Scripts
call activate.bat
cd ..\..
cd lib
python RPC.py

pause

