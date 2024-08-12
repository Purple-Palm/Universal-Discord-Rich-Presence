@echo off
setlocal EnableDelayedExpansion
cd presets\valorant\src\content\packed
for /d %%d in (*) do (
    move "%%d" ..\..\..\..\..
    REM Wait for 1 second
    timeout /t 1 /nobreak >nul
)
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
cd lib
call backup.bat
endlocal
