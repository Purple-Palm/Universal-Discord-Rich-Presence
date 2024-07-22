import os
import time
import subprocess
from InquirerPy.utils import color_print

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
        color_print(
                [
                    ('Skyblue', "Discord"),
                    ('Red'," is not "),
                    ('','open!'),
                ]
            )
        open_discord()
        time.sleep(10)  # Give Discord some time to open
        if not is_discord_open():
            color_print(
                [
                    ('Red', "Failed"),
                    ('',"to open "),
                    ('Skyblue', "Discord"),('','. '),
                    ('Red', "Stopping script"),('','. ')
                ]
            )
            return
    color_print(
                [
                    ('Blue', "Discord"),
                    ('Green',' is open! '),
                    ('Green', "Starting"),('',' RPC script.')
                ]
            )
    os.system("python RPC.py")

if __name__ == "__main__":
    print("By Cactus and VGSS_")
    main()