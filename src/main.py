import time
import sys
import os
import subprocess
import yaml

# This allows running the script from the root directory and finding the 'core' modules
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from core.config_manager import ConfigManager
from core.window_manager import WindowManager
# NEW: Import the server runner from our new integrated mode module
from core.mode_integrated import run_server as run_integrated_mode

def load_settings():
    """
    Loads the global settings from settings.yml.
    Returns the settings dictionary or None if an error occurs.
    """
    try:
        with open("settings.yml", "r") as f:
            settings = yaml.safe_load(f)
            if not settings:
                print("[ERROR] settings.yml is empty or invalid.")
                return None
            return settings
    except FileNotFoundError:
        print("[ERROR] settings.yml not found! Please run the installer first.")
        return None
    except Exception as e:
        print(f"[ERROR] Could not load settings.yml: {e}")
        return None

def run_external_mode():
    """
    Contains the original logic for running in External Mode.
    This launches and manages subprocesses for each configured application.
    """
    print("--- Starting in External Mode ---")
    config_manager = ConfigManager()
    window_manager = WindowManager()
    config = config_manager.load_config()
    if not config:
        return # Error handled in manager

    print("Configuration loaded. Monitoring for focused applications...")
    last_executable = None
    current_rpc_process = None

    try:
        while True:
            active_executable = window_manager.get_active_window_executable()

            if active_executable != last_executable:
                print(f"\nFocus changed: {last_executable or 'None'} -> {active_executable or 'None'}")
                last_executable = active_executable

                if current_rpc_process and current_rpc_process.poll() is None:
                    print(f"Stopping previous RPC process (PID: {current_rpc_process.pid})...")
                    current_rpc_process.terminate()
                    try:
                        current_rpc_process.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        print(f"Process {current_rpc_process.pid} did not terminate in time, killing.")
                        current_rpc_process.kill()
                current_rpc_process = None

                program_config = config_manager.get_program_config(active_executable)

                if program_config and program_config.get('enable', False):
                    prog_name = program_config.get('name', 'Unknown Program')
                    print(f"Found enabled config for: '{prog_name}'")

                    custom_path = program_config.get('custom_rpc_executable_path')

                    if custom_path:
                        print(f"Launching custom RPC script: '{custom_path}'")
                        try:
                            current_rpc_process = subprocess.Popen(custom_path, shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
                            print(f"Started custom RPC process (PID: {current_rpc_process.pid})")
                        except Exception as e:
                            print(f"[ERROR] Failed to launch custom script: {e}")
                    else:
                        python_executable = os.path.join(".venv", "Scripts", "python.exe")
                        default_module_path = os.path.join("src", "modules", "default.py")
                        command = [python_executable, default_module_path, active_executable]

                        try:
                            current_rpc_process = subprocess.Popen(command, creationflags=subprocess.CREATE_NO_WINDOW)
                            print(f"Started default module handler (PID: {current_rpc_process.pid})")
                        except Exception as e:
                             print(f"[ERROR] Failed to launch default module: {e}")
                else:
                     print(f"No enabled configuration found for '{active_executable}'.")

            time.sleep(1)

    except KeyboardInterrupt:
        print("\nShutting down by user request...")
    finally:
        if current_rpc_process and current_rpc_process.poll() is None:
            print("Cleaning up active RPC process...")
            current_rpc_process.kill()

def main():
    """
    The main entry point for the application.
    It reads the mode from settings.yml and launches the appropriate logic.
    """
    print("--- Universal Discord RPC ---")
    settings = load_settings()
    if not settings:
        input("Press Enter to exit.")
        sys.exit(1)

    mode = settings.get('rpc_mode', 'external') # Default to 'external' if key is missing

    if mode == 'integrated':
        run_integrated_mode()
    elif mode == 'external':
        run_external_mode()
    else:
        print(f"[ERROR] Invalid rpc_mode '{mode}' in settings.yml. Please choose 'integrated' or 'external'.")

    print("\nGoodbye!")
    # The input is commented out to allow the script to close cleanly when run as pythonw.exe
    # input("Press Enter to exit.")

if __name__ == "__main__":
    main()
