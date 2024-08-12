import os
import shutil
import subprocess
from distutils.dir_util import copy_tree
import win32com.client
import win10toast
from win10toast import ToastNotifier

def compile_to_exe():
    # Path to the script to compile and the icon
    script_path = 'run.py'
    icon_path = os.path.join('icons', 'custom-logo2.ico')
    
    # Compile the script to an executable
    subprocess.call([
        'pyinstaller', 
        '--onefile', 
        '--windowed', 
        f'--icon={icon_path}', 
        script_path
    ])

    dist_path = os.path.join(os.getcwd(), 'dist', 'run.exe')
    target_path = os.path.join(os.getcwd(), 'run.exe')
    shutil.move(dist_path, target_path)

def delete_original_shortcuts():
    user_profile = os.environ['USERPROFILE']
    start_menu_path = os.path.join(user_profile, 'AppData', 'Roaming', 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Discord Inc')
    desktop_path = os.path.join(user_profile, 'Desktop')
    startup_path = os.path.join(user_profile, 'AppData', 'Roaming', 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
    
    discord_shortcut_name = 'Discord.lnk'
    
    try:
        os.remove(os.path.join(start_menu_path, discord_shortcut_name))
    except FileNotFoundError:
        pass
    
    try:
        os.remove(os.path.join(desktop_path, discord_shortcut_name))
    except FileNotFoundError:
        pass
    
    try:
        os.remove(os.path.join(startup_path, discord_shortcut_name))
    except FileNotFoundError:
        pass

def create_shortcut(target, shortcut_path, description, icon, working_directory):
    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortcut(shortcut_path)
    shortcut.TargetPath = target
    shortcut.WorkingDirectory = working_directory
    shortcut.IconLocation = icon
    shortcut.Description = description
    shortcut.save()

def create_new_shortcuts():
    user_profile = os.environ['USERPROFILE']
    start_menu_path = os.path.join(user_profile, 'AppData', 'Roaming', 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Discord Inc')
    desktop_path = os.path.join(user_profile, 'Desktop')
    startup_path = os.path.join(user_profile, 'AppData', 'Roaming', 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
    
    if not os.path.exists(start_menu_path):
        os.makedirs(start_menu_path)

    target_path = os.path.join(os.getcwd(), 'run.exe')
    config_path = os.path.join(os.getcwd(), 'setup.yml')
    working_directory = os.path.dirname(target_path)
    
    # Copy setup.yml to the target locations
#    shutil.copy(config_path, start_menu_path)    ###Not including startup folder
#    shutil.copy(config_path, desktop_path)    ###Not including startup folder
#    shutil.copy(config_path, startup_path)    ###Not including startup folder

    # Create new shortcuts with "Start In" property
    create_shortcut(
        target=target_path,
        shortcut_path=os.path.join(start_menu_path, 'Discord.lnk'),
        description='Custom Discord Shortcut',
        icon=target_path,
        working_directory=working_directory
    )
    
    create_shortcut(
        target=target_path,
        shortcut_path=os.path.join(desktop_path, 'Discord.lnk'),
        description='Custom Discord Shortcut',
        icon=target_path,
        working_directory=working_directory
    )
    
    create_shortcut(
        target=target_path,
        shortcut_path=os.path.join(startup_path, 'Discord.lnk'),
        description='Custom Discord Shortcut',
        icon=target_path,
        working_directory=working_directory
    )

def send_notification():
    toaster = ToastNotifier()
    toaster.show_toast("🎉 Success!", "Everything is set up correctly. Cleaning up and starting modified Discord. 🚀", duration=10)

def cleaning():
    bat_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'postinstaller.bat')
    subprocess.Popen([bat_path], shell=True)

if __name__ == "__main__":
    compile_to_exe()
    delete_original_shortcuts()
    create_new_shortcuts()
    send_notification()
    cleaning()
