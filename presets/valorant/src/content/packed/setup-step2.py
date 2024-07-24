import os
import shutil
import subprocess
from distutils.dir_util import copy_tree
import win32com.client

def compile_to_exe():
    # Path to the script to compile and the icon
    script_path = 'run.py'
    icon_path = os.path.join('icons', 'custom-logo.ico')
    
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
    
    discord_shortcut_name = 'Discord.lnk'
    
    try:
        os.remove(os.path.join(start_menu_path, discord_shortcut_name))
    except FileNotFoundError:
        pass
    
    try:
        os.remove(os.path.join(desktop_path, discord_shortcut_name))
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
    
    if not os.path.exists(start_menu_path):
        os.makedirs(start_menu_path)

    target_path = os.path.join(os.getcwd(), 'run.exe')
    config_path = os.path.join(os.getcwd(), 'setup.yml')
    working_directory = os.path.dirname(target_path)
    
    # Copy setup.yml to the target locations
    shutil.copy(config_path, start_menu_path)
    shutil.copy(config_path, desktop_path)

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

if __name__ == "__main__":
    compile_to_exe()
    delete_original_shortcuts()
    create_new_shortcuts()
