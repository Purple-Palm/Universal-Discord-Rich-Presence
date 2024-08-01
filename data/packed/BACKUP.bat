@echo off
setlocal

:: Define paths
set "user_profile=%USERPROFILE%"
set "start_menu_path=%user_profile%\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Discord Inc"
set "desktop_path=%user_profile%\Desktop"
set "startup_path=%user_profile%\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup"
set "origcut_path=%cd%\origcut"

:: Define original Discord shortcut paths
set "original_start_menu_shortcut=%origcut_path%\Discord.lnk"
set "original_desktop_shortcut=%origcut_path%\Discord.lnk"
set "original_startup_shortcut=%origcut_path%\Discord.lnk"

:: Replace shortcuts
if exist "%original_start_menu_shortcut%" (
    copy "%original_start_menu_shortcut%" "%start_menu_path%\Discord.lnk" /Y
)
if exist "%original_desktop_shortcut%" (
    copy "%original_desktop_shortcut%" "%desktop_path%\Discord.lnk" /Y
)
if exist "%original_startup_shortcut%" (
    copy "%original_startup_shortcut%" "%startup_path%\Discord.lnk" /Y
)

echo Shortcuts have been restored to their original versions.
call setup.bat
endlocal
