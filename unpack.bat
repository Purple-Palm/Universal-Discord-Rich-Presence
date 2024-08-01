@echo off
setlocal EnableDelayedExpansion
cd data\src-main
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
call BACKUP.bat
endlocal
