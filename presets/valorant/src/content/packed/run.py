import os
import time
import subprocess
import yaml
from InquirerPy.utils import color_print
from updater import check_for_updates


def open_discord():
    discord_path = os.path.join(os.getenv('LOCALAPPDATA'), 'Discord', 'Update.exe')
    subprocess.Popen([discord_path, '--processStart', 'Discord.exe'], shell=True)

def is_discord_open():
    try:
        output = subprocess.check_output(["tasklist"], creationflags=subprocess.CREATE_NO_WINDOW, text=True)
        return "Discord.exe" in output
    except subprocess.CalledProcessError:
        return False

def read_config():
    with open("setup.yml", 'r') as stream:
        config = yaml.safe_load(stream)
    print(f"Config work_dir: {config['work_dir']}")
    return config['work_dir']

def main():
    if not is_discord_open():
        color_print(
            [
                ('Skyblue', "Discord"),
                ('Red', " is not "),
                ('', 'open!'),
            ]
        )
        open_discord()
        time.sleep(10)  # Give Discord some time to open
        if not is_discord_open():
            color_print(
                [
                    ('Red', "Failed"),
                    ('', "to open "),
                    ('Skyblue', "Discord"), ('', '. '),
                    ('Red', "Stopping script"), ('', '. ')
                ]
            )
            return
    color_print(
        [
            ('Blue', "Discord"),
            ('Green', ' is open! '),
            ('Green', "Starting"), ('', ' RPC script.')
        ]
    )
    #work_dir = read_config()
    #bat_path = os.path.join(work_dir, "main.bat")
    #print(f"Running {bat_path}...")
    #subprocess.Popen([bat_path], shell=True)
    #print("Updater started. Exiting run.py.")
    
if __name__ == "__main__":
    print("By Cactus and VGSS_")
    check_for_updates()
    main()

