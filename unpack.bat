@echo off
setlocal EnableDelayedExpansion
cd presets\valorant\src\content\packed
for %%f in (*) do (
    move "%%f" ..\..\..\..\..
    REM Wait for 1 second
    timeout /t 1 /nobreak >nul
)
echo Please wait..
cd ..
cd ..
cd ..
cd ..
cd ..
call setup.bat
endlocal
