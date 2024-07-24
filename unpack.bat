@echo off
setlocal EnableDelayedExpansion

REM Change to the "packed" directory
cd presets\valorant\src\content\packed

REM Loop through all files in the "packed" directory
for %%f in (*) do (
    REM Move the file to the parent directory
    move "%%f" ..\..\..\..\..

    REM Wait for 1 second
    timeout /t 1 /nobreak >nul
)

REM Start setup.bat after all files have been moved
echo Please wait..
cd ..
cd ..
cd ..
cd ..
cd ..
call setup.bat

endlocal
