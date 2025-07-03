import time
import sys
import os
from flask import Flask, jsonify
from flask_cors import CORS

# This allows the script to find the 'core' modules when run by main.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.config_manager import ConfigManager
from core.window_manager import WindowManager

# --- Flask App Setup ---
app = Flask(__name__)
CORS(app)

# --- Globals & Caching ---
config_manager = ConfigManager()
window_manager = WindowManager()
config = config_manager.load_config()

last_executable = None
last_payload = None

# --- Presence Type Mapping ---
PRESENCE_TYPE_MAP = {
    "playing": 0,
    "streaming": 1,
    "listening": 2,
    "watching": 3,
    "competing": 5
}

def build_rpc_payload(program_config):
    """
    Builds a Rich Presence payload dictionary from a given program's configuration.
    """
    app_id = program_config.get('app_id') or config.get('default_app_id')
    
    if not app_id:
        print(f"  -> [ERROR] No app_id found for '{program_config.get('name')}'. Cannot create presence.")
        return None

    print(f"  -> Using app_id: {app_id}")
    print(f"  -> Building payload for '{program_config.get('name')}'")
    
    rpc_details = program_config.get('discord_rpc', {})
    
    # --- MODIFIED: Create a "flat" payload structure ---
    payload = {
        "application_id": str(app_id),
        "name": program_config.get('name', 'Live Status'),
        "type": PRESENCE_TYPE_MAP.get(rpc_details.get('presence_type', 'playing').lower(), 0),
        "flags": 1
    }

    # Add text details directly to the main payload
    if 'details' in rpc_details: payload['details'] = rpc_details['details']
    if 'state' in rpc_details: payload['state'] = rpc_details['state']
    if 'url' in rpc_details and payload['type'] == 1: payload['url'] = rpc_details['url']
        
    # Add image assets directly to the main payload, not a nested 'assets' object
    if 'large_image' in rpc_details: payload['large_image'] = str(rpc_details['large_image'])
    if 'large_text' in rpc_details: payload['large_text'] = rpc_details['large_text']
    if 'small_image' in rpc_details: payload['small_image'] = str(rpc_details['small_image'])
    if 'small_text' in rpc_details: payload['small_text'] = rpc_details['small_text']

    # Add buttons
    if 'buttons' in rpc_details: payload['buttons'] = rpc_details['buttons']
    
    # Timestamp Configuration Logic
    timestamps_config = rpc_details.get('timestamps', {}) 

    if 'end' in timestamps_config:
        payload['timestamps'] = {'end': int(timestamps_config['end'])}
    elif timestamps_config.get('elapsed') == True:
        payload['timestamps'] = {'start': int(time.time())}
        
    return payload

@app.route("/status")
def get_status():
    """
    This is the main endpoint the Vencord plugin will poll.
    It uses a cache to efficiently return the RPC payload for the active window.
    """
    global last_executable, last_payload

    active_executable = window_manager.get_active_window_executable()

    if active_executable != last_executable:
        print(f"\nFocus changed: {last_executable or 'None'} -> {active_executable or 'None'}")
        last_executable = active_executable
        
        program_config = config_manager.get_program_config(active_executable)
        
        if program_config and program_config.get('enable', False):
            last_payload = build_rpc_payload(program_config)
        else:
            last_payload = None
            print("  -> No enabled config found. Clearing payload.")
    
    return jsonify(last_payload or {})

def run_server():
    """Starts the Flask server for Integrated Mode."""
    print("--- Starting in Integrated Mode (Final) ---")
    print("Flask server is running. Vencord plugin can now connect.")
    app.run(host="localhost", port=8765, debug=False)

if __name__ == '__main__':
    run_server()
