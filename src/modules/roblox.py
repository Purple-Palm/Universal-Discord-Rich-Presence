import sys
import os
import time
import glob
import json
import urllib.request
import psutil
import win32gui
import win32process
from pypresence import Presence

# Add the parent directory ('src') to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.config_manager import ConfigManager

class RobloxRPC:
    """
    A dedicated class to handle the Rich Presence logic for Roblox.
    """
    def __init__(self):
        self.config_manager = ConfigManager()
        self.config = self.config_manager.load_config()
        self.program_config = self.config_manager.get_program_config("RobloxPlayerBeta.exe")
        
        if not self.program_config:
            print("[Roblox] ERROR: Could not find Roblox configuration in config.yml.")
            sys.exit(1)

        self.app_id = self.program_config.get("app_id")
        self.rpc_buttons = self.program_config.get("discord_rpc", {}).get("buttons", [])
        
        if not self.app_id:
            print("[Roblox] ERROR: 'app_id' missing for Roblox in config.yml.")
            sys.exit(1)

        self.RPC = None
        self.last_job_id = None

    def connect_rpc(self):
        """Initializes and connects to Discord RPC"""
        try:
            self.RPC = Presence(str(self.app_id))
            self.RPC.connect()
            print("[Roblox] Successfully connected to Discord RPC.")
        except Exception as e:
            print(f"[Roblox] ERROR: Failed to connect to Discord RPC: {e}")
            self.RPC = None

    def get_latest_log_file(self):
        """Finds and reads the latest Roblox log file"""
        try:
            user_profile = os.environ['USERPROFILE']
            logs_path = os.path.join(user_profile, "AppData", "Local", "Roblox", "logs", "*.log")
            list_of_files = glob.glob(logs_path)
            if not list_of_files:
                return None
            latest_file = max(list_of_files, key=os.path.getctime)
            with open(latest_file, "r", encoding="ISO-8859-1") as f:
                return f.readlines()
        except Exception:
            return None

    def parse_log_for_info(self, log_lines):
        """Parses log lines to find the current placeId and jobId"""
        place_id = None
        job_id = None
        
        if not log_lines:
            return None, None

        # Iterate backwards for speed, as recent info is at the end
        for line in reversed(log_lines):
            if not job_id and "Joining game" in line:
                try:
                    job_id = line.split("Joining game '")[1].split("'")[0]
                except IndexError:
                    continue
            if not place_id and "placeId" in line:
                try:
                    place_id = line.split("placeId: ")[1].strip()
                except IndexError:
                    continue
            # Stop if we found both
            if job_id and place_id:
                # Check if we disconnected after this join attempt
                if any("Client:Disconnect" in l for l in log_lines[log_lines.index(line):]):
                    return None, None
                return place_id, job_id
        return None, None

    def get_game_details(self, place_id):
        """Fetches game details from Roblox APIs"""
        try:
            # Get Universe ID
            universe_api_url = f"https://apis.roblox.com/universes/v1/places/{place_id}/universe"
            with urllib.request.urlopen(universe_api_url) as response:
                universe_data = json.loads(response.read())
            universe_id = universe_data.get("universeId")
            if not universe_id:
                return None, None

            # Get Game Details
            games_api_url = f"https://games.roblox.com/v1/games?universeIds={universe_id}"
            with urllib.request.urlopen(games_api_url) as response:
                game_data = json.loads(response.read())["data"][0]
            
            # Get Game Icon
            icon_api_url = f"https://thumbnails.roblox.com/v1/games/icons?universeIds={universe_id}&size=512x512&format=Png&isCircular=false"
            with urllib.request.urlopen(icon_api_url) as response:
                icon_data = json.loads(response.read())["data"][0]

            return game_data, icon_data.get("imageUrl")
        except Exception as e:
            print(f"[Roblox] API Error: {e}")
            return None, None

    def update_presence(self):
        """The main logic for updating the presence."""
        log_lines = self.get_latest_log_file()
        place_id, job_id = self.parse_log_for_info(log_lines)
        
        payload = {
            "large_image": "roblox_logo",
            "large_text": "Roblox",
            "details": "In the Menus",
            "start": int(time.time())
        }
        
        if place_id and job_id:
            if job_id != self.last_job_id:
                print(f"[Roblox] New game detected! Place: {place_id}, Job: {job_id}")
                self.last_job_id = job_id

            game_info, icon_url = self.get_game_details(place_id)
            if game_info:
                payload["details"] = game_info.get("name", "A Roblox Game")
                payload["state"] = f"By {game_info.get('creator', {}).get('name', 'a developer')}"
                payload["large_image"] = icon_url or "roblox_logo"
                payload["large_text"] = game_info.get("name", "Roblox")
                
                # Format buttons with dynamic IDs
                formatted_buttons = []
                for button in self.rpc_buttons:
                    formatted_buttons.append({
                        "label": button["label"],
                        "url": button["url"].format(PLACEID=place_id, JOBID=job_id)
                    })
                if formatted_buttons:
                    payload["buttons"] = formatted_buttons

        else: # If not in a game, reset job_id
            self.last_job_id = None

        if self.RPC:
            self.RPC.update(**payload)
            # print("[Roblox] Presence updated.")

    def run(self):
        """Main loop for the Roblox RPC module."""
        self.connect_rpc()
        
        if not self.RPC:
            return

        try:
            while True:
                self.update_presence()
                time.sleep(15) # Update every 15 seconds
        except KeyboardInterrupt:
            print("[Roblox] Module stopped by user.")
        except Exception as e:
            print(f"[Roblox] An unexpected error occurred in the run loop: {e}")
        finally:
            if self.RPC:
                self.RPC.close()
            print("[Roblox] Module has been shut down.")


if __name__ == "__main__":
    roblox_rpc = RobloxRPC()
    roblox_rpc.run()

