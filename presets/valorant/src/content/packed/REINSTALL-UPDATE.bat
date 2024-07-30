@echo off
setlocal

echo Current directory: %cd%
echo Starting cleanup process...

ping 127.0.0.1 -n 2 > nul

if exist "dist" (
    echo Found folder "dist", attempting to delete...
    rmdir /s /q "dist" && echo Deleted folder "dist" || echo Failed to delete folder "dist"
)
ping 127.0.0.1 -n 2 > nul

if exist "build" (
    echo Found folder "build", attempting to delete...
    rmdir /s /q "build" && echo Deleted folder "build" || echo Failed to delete folder "build"
)
ping 127.0.0.1 -n 2 > nul

if exist "origcut" (
    echo Found folder "origcut", attempting to delete...
    rmdir /s /q "origcut" && echo Deleted folder "origcut" || echo Failed to delete folder "origcut"
)
ping 127.0.0.1 -n 2 > nul

if exist "presets" (
    echo Found folder "presets", attempting to delete...
    rmdir /s /q "presets" && echo Deleted folder "presets" || echo Failed to delete folder "presets"
)
ping 127.0.0.1 -n 2 > nul

if exist "icons" (
    echo Found folder "icons", attempting to delete...
    rmdir /s /q "icons" && echo Deleted folder "icons" || echo Failed to delete folder "icons"
)
ping 127.0.0.1 -n 2 > nul

if exist "venv" (
    echo Found folder "venv", attempting to delete...
    rmdir /s /q "venv" && echo Deleted folder "venv" || echo Failed to delete folder "venv"
)
ping 127.0.0.1 -n 2 > nul

:: Deleting files with 1-second delay
if exist "BACKUP.bat" (
    echo Found file "BACKUP.bat", attempting to delete...
    del /f /q "BACKUP.bat" && echo Deleted file "BACKUP.bat" || echo Failed to delete file "BACKUP.bat"
)
ping 127.0.0.1 -n 2 > nul

if exist "config.yml" (
    echo Found file "config.yml", attempting to delete...
    del /f /q "config.yml" && echo Deleted file "config.yml" || echo Failed to delete file "config.yml"
)
ping 127.0.0.1 -n 2 > nul

if exist "main.bat" (
    echo Found file "main.bat", attempting to delete...
    del /f /q "main.bat" && echo Deleted file "main.bat" || echo Failed to delete file "main.bat"
)
ping 127.0.0.1 -n 2 > nul

if exist "README.md" (
    echo Found file "README.md", attempting to delete...
    del /f /q "README.md" && echo Deleted file "README.md" || echo Failed to delete file "README.md"
)
ping 127.0.0.1 -n 2 > nul

if exist "req.txt" (
    echo Found file "req.txt", attempting to delete...
    del /f /q "req.txt" && echo Deleted file "req.txt" || echo Failed to delete file "req.txt"
)
ping 127.0.0.1 -n 2 > nul

if exist "RPC.py" (
    echo Found file "RPC.py", attempting to delete...
    del /f /q "RPC.py" && echo Deleted file "RPC.py" || echo Failed to delete file "RPC.py"
)
ping 127.0.0.1 -n 2 > nul

if exist "run.exe" (
    echo Found file "run.exe", attempting to delete...
    del /f /q "run.exe" && echo Deleted file "run.exe" || echo Failed to delete file "run.exe"
)
ping 127.0.0.1 -n 2 > nul

if exist "run.py" (
    echo Found file "run.py", attempting to delete...
    del /f /q "run.py" && echo Deleted file "run.py" || echo Failed to delete file "run.py"
)
ping 127.0.0.1 -n 2 > nul

if exist "run.spec" (
    echo Found file "run.spec", attempting to delete...
    del /f /q "run.spec" && echo Deleted file "run.spec" || echo Failed to delete file "run.spec"
)
ping 127.0.0.1 -n 2 > nul

if exist "setup-step2.py" (
    echo Found file "setup-step2.py", attempting to delete...
    del /f /q "setup-step2.py" && echo Deleted file "setup-step2.py" || echo Failed to delete file "setup-step2.py"
)
ping 127.0.0.1 -n 2 > nul

if exist "setup.bat" (
    echo Found file "setup.bat", attempting to delete...
    del /f /q "setup.bat" && echo Deleted file "setup.bat" || echo Failed to delete file "setup.bat"
)
ping 127.0.0.1 -n 2 > nul

if exist "setup.yml" (
    echo Found file "setup.yml", attempting to delete...
    del /f /q "setup.yml" && echo Deleted file "setup.yml" || echo Failed to delete file "setup.yml"
)
ping 127.0.0.1 -n 2 > nul

:: Check and remove shortcut
set "desktop=%USERPROFILE%\Desktop"
set "shortcut=REINSTALL-UPDATE - Shortcut.url"

if exist "%desktop%\%shortcut%" (
    echo Found shortcut "%shortcut%", attempting to delete...
    del /f /q "%desktop%\%shortcut%" && echo Deleted shortcut "%shortcut%" || echo Failed to delete shortcut "%shortcut%"
) else (
    echo No shortcut "%shortcut%" found, continuing...
)

ping 127.0.0.1 -n 2 > nul

echo Cloning repository from GitHub...
git clone https://github.com/Purple-Palm/Universal-Discord-Rich-Presence.git
cd Universal-Discord-Rich-Presence

echo Moving files to parent directory...
for /f "delims=" %%i in ('dir /b /a') do move "%%i" ..

cd ..
rmdir /s /q Universal-Discord-Rich-Presence

echo Running unpack.bat...
call unpack.bat

echo Update/Reinstall process completed.
pause
