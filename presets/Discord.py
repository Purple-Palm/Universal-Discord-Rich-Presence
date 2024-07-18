import time
import os
import win32gui
import win32process
import psutil
from pypresence import Presence

def get_active_window_executable():
    window = win32gui.GetForegroundWindow()
    _, pid = win32process.GetWindowThreadProcessId(window)
    try:
        process = psutil.Process(pid)
        return process.name()
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        return None

def main():
    client_id = '1262946659701096498'
    RPC = Presence(client_id)
    RPC.connect()

    print("RPC connected, updating presence for Discord...")

    start_time = time.time()
    while True:
        if get_active_window_executable() != "Discord.exe":
            print("Discord is no longer in focus. Restarting main.py...")
            RPC.clear()  # Clear the presence
            RPC.close()  # Close the RPC connection
            os.system("python main.py")
            break

        RPC.update(
            state="Chillin' in Discord",
            details="  ",
            large_image="1",
            start=start_time
        )
        time.sleep(15)  # Update every 15 seconds

if __name__ == "__main__":
    main()