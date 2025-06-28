import sys
import os
import time
from pypresence import Presence

# Add the parent directory ('src') to the Python path to allow imports from the 'core' module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.config_manager import ConfigManager

def main(executable_name):
    """
    Handles displaying a generic Rich Presence based on the config file.
    
    Args:
        executable_name (str): The name of the focused executable, passed by main.py
    """
    print(f"--- Default Module Started for: {executable_name} ---")

    # Load Configuration
    config_manager = ConfigManager()
    config_manager.load_config()
    program_config = config_manager.get_program_config(executable_name)
    
    if not program_config:
        print(f"[ERROR] Could not find configuration for '{executable_name}'. Exiting module.")
        return

    # Extract RPC Details
    app_id = program_config.get('app_id')
    rpc_details = program_config.get('discord_rpc', {})
    
    if not app_id:
        print(f"[ERROR] 'app_id' is missing for '{executable_name}' in config.yml. Exiting module.")
        return
        
    print(f"Initializing RPC for '{program_config.get('name')}' with App ID: {app_id}")

    # Initialize and Connect RPC
    try:
        RPC = Presence(str(app_id))
        RPC.connect()
        print("Successfully connected to Discord.")
    except Exception as e:
        print(f"[ERROR] Failed to connect to Discord RPC: {e}")
        return # Exit if connection fails

    # Format the Presence Payload
    # We build the payload dictionary only with keys that exist in the config
    payload = {}
    if 'details' in rpc_details:
        payload['details'] = rpc_details['details']
    if 'state' in rpc_details:
        payload['state'] = rpc_details['state']
    if 'large_image' in rpc_details:
        payload['large_image'] = str(rpc_details['large_image'])
    if 'large_text' in rpc_details:
        payload['large_text'] = rpc_details['large_text']
    if 'small_image' in rpc_details:
        payload['small_image'] = str(rpc_details['small_image'])
    if 'small_text' in rpc_details:
        payload['small_text'] = rpc_details['small_text']
    if 'buttons' in rpc_details:
        payload['buttons'] = rpc_details['buttons']
        
    # Set the start time to show elapsed time
    payload['start'] = int(time.time())

    # --- Main Loop for this Module ---
    # The parent process (main.py) will kill this script when focus is lost.
    # So, we just need to keep the presence updated in a simple loop.
    try:
        print("Displaying Rich Presence...")
        RPC.update(**payload)
        
        while True:
            # This loop keeps the script alive
            # main.py handles killing it
            time.sleep(15) 
            
    except Exception as e:
        # This will catch errors if Discord closes, etc
        print(f"[ERROR] An error occurred in the presence loop: {e}")
    finally:
        RPC.close()
        print(f"--- Default Module for {executable_name} Shutting Down ---")


if __name__ == "__main__":
    # Allows the script to be run from the command line with an argument
    # main.py provides this argument when it launches the subprocess
    if len(sys.argv) > 1:
        target_executable = sys.argv[1]
        main(target_executable)
    else:
        print("[ERROR] No executable name provided. This module should be launched by main.py.")
        time.sleep(5)
