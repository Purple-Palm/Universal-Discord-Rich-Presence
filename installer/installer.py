import os
import sys
import subprocess
import shutil
import platform
import time
import json
import stat

# --- Installer Dependencies ---
INSTALLER_DEPS = ['winshell', 'win10toast', 'InquirerPy', 'pyyaml', 'psutil']
VENV_DIR = ".venv"
REQUIREMENTS_FILE = "requirements.txt"
SETTINGS_FILE = "settings.yml" # MODIFIED: Use the new settings file
MAIN_SCRIPT_PATH = os.path.join("src", "main.py")
SHORTCUT_NAME = "Universal Discord RPC.lnk"
VENCORD_REPO_URL = "https://github.com/Vendicated/Vencord.git"
VENCORD_PLUGIN_SRC = os.path.join("assets", "vencord_plugin", "index.tsx")
VENCORD_DIR = "Vencord"

# --- Helper Functions (No changes) ---
def print_step(message):
    """Prints a formatted step message."""
    print(f"\n{'='*10} {message} {'='*10}")

def print_success(message):
    """Prints a formatted success message."""
    print(f"  -> SUCCESS: {message}")

def print_error(message, is_fatal=True):
    """Prints a formatted error message and optionally exits."""
    print(f"\n  [!] ERROR: {message}")
    if is_fatal:
        input("      Press Enter to exit.")
        sys.exit(1)

def print_info(message):
    """Prints an informational message."""
    print(f"  [i] {message}")

def run_command(command, cwd=None, error_msg="Command failed to execute.", interactive=False, auto_enter=False):
    """
    Runs a command with options for silent, interactive, or automated input.
    """
    try:
        if interactive:
            print_info(f"Running interactive command: '{command}'")
            subprocess.check_call(command, shell=True, cwd=cwd)
        else:
            # For silent or auto-enter modes
            process = subprocess.Popen(
                command,
                shell=True,
                cwd=cwd,
                stdin=subprocess.PIPE if auto_enter else None,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding='utf-8',
                creationflags=subprocess.CREATE_NO_WINDOW if platform.system() == "Windows" else 0
            )

            stdout, stderr = process.communicate(input='\n' if auto_enter else None)

            if process.returncode != 0:
                full_error_msg = f"{error_msg}\n      Return Code: {process.returncode}\n      STDERR: {stderr.strip()}"
                print_error(full_error_msg, is_fatal=False)
                return False
        return True
    except Exception as e:
        print_error(f"An unexpected error occurred while running '{command}': {e}", is_fatal=False)
        return False

def remove_readonly(func, path, excinfo):
    """Error handler for shutil.rmtree that removes read-only flags and retries."""
    os.chmod(path, stat.S_IWRITE)
    func(path)

# --- Step 0: Dependency Self-Check (No changes) ---
def ensure_installer_deps():
    print_step("Checking Installer Sanity")
    try:
        import psutil, winshell, yaml
        from win10toast import ToastNotifier
        from InquirerPy import inquirer
        print_success("Installer dependencies are met.")
    except ImportError:
        print_info("Missing one or more installer dependencies. Attempting to install...")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + INSTALLER_DEPS)
            print_success("Dependencies installed.")
            print_info("Please re-run the installer to continue.")
            input("Press Enter to exit.")
            sys.exit(0)
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            print_error(f"Could not install dependencies. Ensure Python and pip are installed correctly. Details: {e}")

ensure_installer_deps()

import psutil
from InquirerPy import inquirer
from InquirerPy.validator import Validator, ValidationError
import yaml
import winshell
from win10toast import ToastNotifier

# --- Discord Process Management Class (No changes) ---
class DiscordManager:
    @staticmethod
    def find_and_kill_discord():
        print_info("Searching for Discord and related processes...")
        processes_to_kill = ['discord.exe', 'vencordinstallercli.exe']
        killed = False
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['name'].lower() in processes_to_kill:
                try:
                    p = psutil.Process(proc.info['pid'])
                    p.kill()
                    print_info(f"  - Terminated {proc.info['name']} (PID: {proc.info['pid']})")
                    killed = True
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
        if killed:
            print_success("Discord-related processes terminated.")
            time.sleep(2)
        else:
            print_info("No running Discord process found.")

    @staticmethod
    def start_discord():
        print_info("Starting Discord...")
        try:
            if platform.system() == "Windows":
                update_exe = os.path.join(os.getenv('LOCALAPPDATA'), 'Discord', 'Update.exe')
                if os.path.exists(update_exe):
                    subprocess.Popen([update_exe, '--processStart', 'Discord.exe'])
                    print_success("Discord startup command issued.")
                    return True
            print_error("Could not find Discord's Update.exe at the default location.", is_fatal=False)
            return False
        except Exception as e:
            print_error(f"Failed to start Discord: {e}", is_fatal=False)
            return False

    @staticmethod
    def get_vencord_settings_path():
        if platform.system() == "Windows":
            return os.path.join(os.getenv('APPDATA'), 'Vencord', 'settings', 'settings.json')
        return None

# --- Main Installer Logic ---

def check_prerequisites():
    print_step("Checking Prerequisites for Integrated Mode")
    tools = {"Git": "git --version", "Node.js": "node --version", "pnpm": "pnpm --version"}
    all_ok = all(run_command(cmd, error_msg=f"{tool} not found.") for tool, cmd in tools.items())
    if not all_ok:
        print_error("One or more prerequisites are missing. Please install them and re-run the installer.")
    print_success("All prerequisites for Integrated Mode are installed.")

class AgreementValidator(Validator):
    def validate(self, document):
        if document.text.strip().upper() != 'AGREE':
            raise ValidationError(message="Please type 'AGREE' to continue or Ctrl+C to exit.", cursor_position=len(document.text))

def get_user_choice():
    print_step("User Agreement & Mode Selection")
    print("""
    Welcome! Please choose your desired mode:
    1. External Mode (Legacy): Safe, but requires manual app creation on Discord's Dev Portal.
    2. Integrated Mode (Recommended): Fully dynamic RPC using Vencord. Easier, but modifies your client.

    RISK ACKNOWLEDGEMENT: Modifying the client is against Discord's ToS.
    While safe for cosmetic purposes, you proceed at your own risk.
    """)
    try:
        inquirer.text(message="Please type 'AGREE' to accept and continue:", validate=AgreementValidator()).execute()
    except KeyboardInterrupt:
        print("\nInstallation cancelled."); sys.exit(0)
    return inquirer.select(message="Which mode would you like to install?", choices=[{"name": "Integrated Mode (Recommended)", "value": "integrated"}, {"name": "External Mode (Legacy)", "value": "external"}], default="integrated").execute()

def enable_plugin_in_settings():
    print_info("Attempting to enable PythonBridge plugin automatically...")
    settings_path = DiscordManager.get_vencord_settings_path()
    if not settings_path or not os.path.exists(settings_path):
        print_error("Vencord settings file not found. Please enable 'PythonBridge' manually.", is_fatal=False)
        return
    try:
        with open(settings_path, 'r+') as f:
            settings = json.load(f)
            settings.setdefault("plugins", {})["PythonBridge"] = {"enabled": True}
            f.seek(0)
            json.dump(settings, f, indent=4)
            f.truncate()
        print_success("PythonBridge plugin enabled in Vencord settings.")
    except Exception as e:
        print_error(f"Could not modify Vencord settings.json: {e}. Please enable the plugin manually.", is_fatal=False)

def install_vencord():
    print_step("Starting Vencord Installation")
    use_default_path = inquirer.confirm(message="Is your Discord installed in the default location?", default=True).execute()
    if not os.path.exists(VENCORD_DIR):
        print_info("Cloning Vencord repository..."); run_command(f"git clone {VENCORD_REPO_URL}", error_msg="Failed to clone Vencord.")
    plugin_dest_dir = os.path.join(VENCORD_DIR, "src", "userplugins", "uDRP")
    os.makedirs(plugin_dest_dir, exist_ok=True)
    shutil.copy(VENCORD_PLUGIN_SRC, os.path.join(plugin_dest_dir, "index.tsx"))
    print_success("Placed custom RPC plugin.")
    print_info("Installing Vencord dependencies (this may take a while)..."); run_command("pnpm install --frozen-lockfile", cwd=VENCORD_DIR, error_msg="pnpm install failed.")
    print_info("Building Vencord..."); run_command("pnpm build", cwd=VENCORD_DIR, error_msg="pnpm build failed.")
    for i in range(3, 0, -1):
        sys.stdout.write(f"\r  [i] Closing Discord in {i} second(s)..."); sys.stdout.flush(); time.sleep(1)
    print()
    DiscordManager.find_and_kill_discord()
    print_info("Injecting Vencord into Discord...")
    if use_default_path:
        run_command("pnpm inject", cwd=VENCORD_DIR, error_msg="Automated injection failed. Please try again, selecting 'No' for default location.", auto_enter=True)
    else:
        print_info("Please follow the on-screen prompts to select your Discord installation path.")
        run_command("pnpm inject", cwd=VENCORD_DIR, error_msg="pnpm inject failed.", interactive=True)
    DiscordManager.start_discord()
    print_info("Waiting 10 seconds for Discord to initialize Vencord settings...")
    time.sleep(10)
    DiscordManager.find_and_kill_discord()
    enable_plugin_in_settings()
    print_success("Vencord installation and configuration complete.")
    DiscordManager.start_discord()

def setup_python_env():
    print_step("Setting up Python Environment")
    if not os.path.exists(VENV_DIR):
        run_command(f"{sys.executable} -m venv {VENV_DIR}", error_msg="Failed to create venv.")
    python_executable = os.path.join(VENV_DIR, "Scripts", "python.exe")
    run_command(f"{python_executable} -m pip install -r {REQUIREMENTS_FILE}", error_msg="Failed to install project dependencies.")
    print_success("Project environment is ready.")

def create_shortcut():
    print_step("Creating Desktop Shortcut")
    target_executable = os.path.join(os.getcwd(), VENV_DIR, "Scripts", "pythonw.exe")
    script_to_run = os.path.join(os.getcwd(), MAIN_SCRIPT_PATH)
    icon_path = os.path.join(os.getcwd(), "assets", "icons", "app.ico")
    with winshell.shortcut(os.path.join(winshell.desktop(), SHORTCUT_NAME)) as shortcut:
        shortcut.path, shortcut.arguments, shortcut.working_directory = target_executable, f'"{script_to_run}"', os.getcwd()
        shortcut.description, shortcut.icon_location = "Universal Discord Rich Presence", (icon_path, 0)
    print_success(f"Shortcut created on your desktop.")

def update_settings(mode):
    """MODIFIED: Updates the new settings.yml file."""
    print_step("Finalizing Configuration")
    try:
        with open(SETTINGS_FILE, 'w') as f:
            settings_data = {'rpc_mode': mode}
            yaml.dump(settings_data, f, default_flow_style=False)
        print_success(f"Configuration set to '{mode}' mode in {SETTINGS_FILE}.")
    except Exception as e:
        print_error(f"Could not write to {SETTINGS_FILE}: {e}")

def notify_completion():
    print_step("Installation Complete")
    try:
        ToastNotifier().show_toast("Installation Complete!", "Universal Discord RPC is ready.", icon_path=os.path.join(os.getcwd(), "assets", "icons", "app.ico"), duration=10)
    except Exception: pass
    print_info("Setup is complete. You can now run the application from the desktop shortcut.")

def main():
    chosen_mode = get_user_choice()
    if chosen_mode == 'integrated':
        check_prerequisites()
        install_vencord()
    setup_python_env()
    update_settings(chosen_mode) # MODIFIED: Call the new settings function
    create_shortcut()
    notify_completion()
    input("\nPress Enter to close the installer.")

if __name__ == "__main__":
    main()
