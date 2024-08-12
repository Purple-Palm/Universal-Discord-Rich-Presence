@echo off
setlocal

echo Current directory: %cd%
echo Starting cleanup process...

:: Terminate all Python processes
echo Terminating all Python processes...
taskkill /F /IM python.exe /T
taskkill /F /IM pythonw.exe /T
taskkill /F /IM python3.11.exe /T

ping 127.0.0.1 -n 2 > nul


if exist "compiler.py" (
    echo Found folder "compiler.py", attempting to delete...
    rmdir /s /q "compiler.py" && echo Deleted folder "compiler.py" || echo Failed to delete folder "compiler.py"
)
ping 127.0.0.1 -n 2 > nul

if exist "req.txt" (
    echo Found folder "req.txt", attempting to delete...
    rmdir /s /q "req.txt" && echo Deleted folder "req.txt" || echo Failed to delete folder "req.txt"
)
ping 127.0.0.1 -n 2 > nul

if exist "run.py" (
    echo Found folder "run.py", attempting to delete...
    rmdir /s /q "run.py" && echo Deleted folder "run.py" || echo Failed to delete folder "run.py"
)
ping 127.0.0.1 -n 2 > nul

if exist "setup.bat" (
    echo Found folder "setup.bat", attempting to delete...
    rmdir /s /q "setup.bat" && echo Deleted folder "setup.bat" || echo Failed to delete folder "setup.bat"
)
ping 127.0.0.1 -n 2 > nul

call RPC.bat