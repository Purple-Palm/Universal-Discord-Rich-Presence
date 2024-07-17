import os
import time
import subprocess

def open_discord():
    discord_path = os.path.join(os.getenv('LOCALAPPDATA'), 'Discord', 'Update.exe')
    subprocess.Popen([discord_path, '--processStart', 'Discord.exe'], shell=True)

def is_discord_open():
    try:
        # Check if Discord process is running
        output = subprocess.check_output(["tasklist"], creationflags=subprocess.CREATE_NO_WINDOW, text=True)
        return "Discord.exe" in output
    except subprocess.CalledProcessError:
        return False

def main():
    if not is_discord_open():
        print("Discord is not open. Opening Discord and playing sound.")
        open_discord()
        time.sleep(10)  # Give Discord some time to open
        if not is_discord_open():
            print("Failed to open Discord. Stopping script.")
            return
    print("Discord is open. Starting main script.")
    os.system("python main.py")

if __name__ == "__main__":
    main()