import json
import os
import logging


class ConfigManager:
    def __init__(self, config_file="config.json"):
        self.config_file = config_file
        self.config = {}
        self._last_mtime = 0
        self.load()

    def load(self):
        if not os.path.exists(self.config_file):
            logging.error(f"❌ Config file not found: {self.config_file}")
            # Create a basic skeleton if missing
            self.config = {"core": {"poll_interval": 2.5}, "rules": []}
            return

        try:
            mtime = os.path.getmtime(self.config_file)
            if mtime > self._last_mtime:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
                self._last_mtime = mtime
                logging.info("✅ Config loaded.")
        except Exception as e:
            logging.error(f"❌ Config Load Error: {e}")

    def check_hot_reload(self):
        if os.path.exists(self.config_file):
            if os.path.getmtime(self.config_file) > self._last_mtime:
                logging.info("♻️ Config file changed. Reloading...")
                self.load()

    def get_rule(self, process_name: str):
        process_name = process_name.lower()

        rules = self.config.get("rules", [])

        for rule in rules:
            if not rule.get("enabled", True):
                continue

            # Check if process_name is in the list for this rule
            # We enforce lowercase comparison
            proc_list = [p.lower() for p in rule.get("process_names", [])]

            if process_name in proc_list:
                return rule

        return None

    @property
    def client_id(self):
        return self.config.get("core", {}).get("client_id")

    @property
    def poll_interval(self):
        return self.config.get("core", {}).get("poll_interval", 2.0)