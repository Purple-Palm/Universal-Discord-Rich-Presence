import os
import yaml
import sys

class ConfigManager:
    """
    Handles loading, accessing, and validating the project's config.yml file.
    """
    def __init__(self, config_path="config.yml"):
        self.config_path = config_path
        self.config = None

    def load_config(self):
        """
        Loads the configuration from the config.yml file.
        If the file doesn't exist, it prints an error and exits.
        """
        if not os.path.exists(self.config_path):
            print(f"[ERROR] Configuration file not found at: {self.config_path}")
            print("        Please ensure 'config.yml' is in the root directory.")
            input("        Press Enter to exit.")
            sys.exit(1)
            
        try:
            with open(self.config_path, "r") as f:
                self.config = yaml.safe_load(f)
                if not self.config:
                    print(f"[ERROR] Configuration file '{self.config_path}' is empty or invalid.")
                    input("        Press Enter to exit.")
                    sys.exit(1)
            return self.config
        except yaml.YAMLError as e:
            print(f"[ERROR] Failed to parse 'config.yml'. Please check its formatting. Details: {e}")
            input("        Press Enter to exit.")
            sys.exit(1)

    def get_program_config(self, executable_name):
        """
        Finds and returns the configuration for a specific program
        based on its executable name.
        """
        if not self.config or 'programs' not in self.config:
            return None
            
        if not executable_name:
            return None

        for prog_id, prog_data in self.config.get('programs', {}).items():
            if prog_data.get('executable') and prog_data['executable'].lower() == executable_name.lower():
                return prog_data
                
        return None

