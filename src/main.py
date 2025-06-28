import time
import sys
import os
import subprocess
import importlib.util

# This allows running the script from the root directory
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from core.config_manager import ConfigManager
from core.window_manager import WindowManager

def main():
    """
    The main entry point and loop for the Universal Discord RPC application.
    This function initializes the application, monitors for window focus changes,
    and manages the lifecycle of RPC modules.
    """
    print("--- Universal Discord RPC ---")
    print("Starting up...")

    # --- Initialization ---
    config_manager = ConfigManager()
    window_manager = WindowManager()

    # Load the configuration from config.yml
    config = config_manager.load_config()
    if not config:
        # Errors are handled within the manager, which will exit the script
        return

    print("Configuration loaded. Monitoring for focused applications...")

    # State Tracking
    last_executable = None
    current_rpc_process = None
    
    # Main Loop
    try:
        while True:
            # 1. Get the currently focused application executable
            active_executable = window_manager.get_active_window_executable()

            # 2. Check if the focused application has changed
            if active_executable != last_executable:
                print(f"\nFocus changed: {last_executable or 'None'} -> {active_executable or 'None'}")
                last_executable = active_executable

                # 3. Terminate the previous RPC process if it was running
                if current_rpc_process and current_rpc_process.poll() is None:
                    print(f"Stopping previous RPC process (PID: {current_rpc_process.pid})...")
                    current_rpc_process.terminate()
                    current_rpc_process.wait(timeout=5) # Wait for the process to terminate
                current_rpc_process = None

                # 4. Find the matching RPC configuration for the new executable
                program_config = config_manager.get_program_config(active_executable)

                if program_config and program_config.get('enable', False):
                    prog_name = program_config.get('name', 'Unknown Program')
                    print(f"Found enabled config for: '{prog_name}'")
                    
                    # 5. Launch the new RPC process based on the config
                    custom_path = program_config.get('custom_rpc_executable_path')
                    
                    if custom_path:
                        print(f"Launching custom RPC script: '{custom_path}'")
                        try:
                            current_rpc_process = subprocess.Popen(custom_path, shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
                            print(f"Started custom RPC process (PID: {current_rpc_process.pid})")
                        except Exception as e:
                            print(f"[ERROR] Failed to launch custom script: {e}")

                    else:
                        # Handle of the modular, non-custom RPCs
                        print(f"Standard RPC module for '{prog_name}' will be used.")
                        # This will be expanded to call src/modules/default.py with the specific program config

                        
                        # Run the default module handler
                        python_executable = os.path.join(".venv", "Scripts", "python.exe")
                        default_module_path = os.path.join("src", "modules", "default.py")
                        
                        # Pass the executable name as an argument to the module
                        command = [python_executable, default_module_path, active_executable]

                        try:
                            current_rpc_process = subprocess.Popen(command, creationflags=subprocess.CREATE_NO_WINDOW)
                            print(f"Started default module handler (PID: {current_rpc_process.pid})")
                        except Exception as e:
                             print(f"[ERROR] Failed to launch default module: {e}")
                else:
                     print(f"No enabled configuration found for '{active_executable}'.")

            # Polling interval to avoid high CPU usage
            time.sleep(1) # Check for focus change every 1 seconds

    except KeyboardInterrupt:
        print("\nShutting down by user request...")
    except Exception as e:
        print(f"\n[FATAL ERROR] An unexpected error occurred: {e}")
    finally:
        # --- Cleanup ---
        if current_rpc_process and current_rpc_process.poll() is None:
            print("Cleaning up active RPC process...")
            current_rpc_process.terminate()
        print("Goodbye!")
        input("Press Enter to exit.")

if __name__ == "__main__":
    main()
