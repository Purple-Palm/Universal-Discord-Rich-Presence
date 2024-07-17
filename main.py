import time
import os
import win32gui
import win32process
import psutil

def get_active_window_executable():
    window = win32gui.GetForegroundWindow()
    _, pid = win32process.GetWindowThreadProcessId(window)
    try:
        process = psutil.Process(pid)
        return process.name()
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        return None

def main():
    last_executable = ""
    while True:
        active_executable = get_active_window_executable()
        if active_executable and active_executable != last_executable:
            print(f"Active executable changed to: {active_executable}")
            if active_executable == "msedge.exe":
                os.system("python presets/msedge.py")
            elif active_executable == "Telegram.exe":
                os.system("python presets/telegram.py")
            elif active_executable == "ShareX.exe":
                os.system("python presets/ShareX.py")
            elif active_executable == "voicemeeter8x64.exe":
                os.system("python presets/voicemeeter8x64.py")
            elif active_executable == "Discord.exe":
                os.system("python presets/Discord.py")
            elif active_executable == "ayugram.exe":
                os.system("python presets/ayugram.py")
            elif active_executable == "explorer.exe":
                os.system("python presets/explorer.py")
            elif active_executable == "steamwebhelper.exe":
                os.system("python presets/steamwebhelper.py")
            elif active_executable == "vlc.exe":
                os.system("python presets/vlc.py")
            elif active_executable == "NZXT CAM.exe":
                os.system("python presets/NZXT_CAM.py")
            elif active_executable == "Notepad.exe":
                os.system("python presets/Notepad.py")
            elif active_executable == "Riot Client.exe":
                os.system("python presets/Riot_Client.py")
            elif active_executable == "EpicGamesLauncher.exe":
                os.system("python presets/EpicGamesLauncher.py")
            elif active_executable == "VALORANT-Win64-Shipping.exe":
                os.system("python presets/valorant/VALORANT-Win64-Shipping.py")
            elif active_executable == "vlc.exe":
                os.system("python presets/vlc.py")
            elif active_executable == "vlc.exe":
                os.system("python presets/vlc.py")
            elif active_executable == "vlc.exe":
                os.system("python presets/vlc.py")
            elif active_executable == "vlc.exe":
                os.system("python presets/vlc.py")
            elif active_executable == "vlc.exe":
                os.system("python presets/vlc.py")
            elif active_executable == "vlc.exe":
                os.system("python presets/vlc.py")
            last_executable = active_executable
        time.sleep(1)

if __name__ == "__main__":
    main()
