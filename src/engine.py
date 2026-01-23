import time
import logging
import platform
import sys
from .config import ConfigManager
from .rpc import UniversalRPC


class Engine:
    def __init__(self):
        self.os_name = platform.system()
        self.setup_logging()
        self.config_mgr = ConfigManager()
        self.rpc = UniversalRPC(self.config_mgr.client_id)
        self.detector = self._get_detector()

        self.process_start_times = {}
        self.current_process = None

    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='[%(asctime)s] %(levelname)s: %(message)s',
            datefmt='%H:%M:%S'
        )

    def _get_detector(self):
        if self.os_name == "Windows":
            from .detectors.windows import WindowsDetector
            return WindowsDetector()
        elif self.os_name == "Linux":
            from .detectors.linux import KDEWaylandDetector
            return KDEWaylandDetector()
        else:
            logging.error(f"Unsupported OS: {self.os_name}")
            sys.exit(1)

    def run(self):
        logging.info(f"🚀 Starting Universal DRPC on {self.os_name}")
        self.rpc.connect()

        try:
            while True:
                self.config_mgr.check_hot_reload()

                proc_name, win_title = self.detector.get_active_window()

                if proc_name:
                    rule = self.config_mgr.get_rule(proc_name)

                    if rule:
                        # 1. Manage Timestamp
                        if self.current_process != proc_name:
                            self.current_process = proc_name
                            self.process_start_times[proc_name] = int(time.time())

                        start_time = self.process_start_times.get(proc_name) if rule.get("show_timestamp") else None

                        # 2. Parse Strings
                        # We combine 'details' and 'state' from config into one description line
                        # because 'Watching' only gives us two visible lines: The Name and the State.

                        raw_desc = rule.get("details", "{title}")  # Default to just title if missing
                        description = raw_desc.replace("{title}", win_title if win_title else "")

                        # 3. Construct the Payload
                        activity = {
                            "header_text": rule.get("display_name"),  # BECOMES BOLD
                            "description": description,  # BECOMES SECOND LINE

                            "large_image": rule.get("large_image"),
                            "small_image": rule.get("small_image"),
                            "small_text": rule.get("small_text"),
                            "buttons": rule.get("buttons"),
                            "start": start_time
                        }

                        self.rpc.update(activity)
                    else:
                        self.current_process = None
                        self.rpc.clear()
                else:
                    self.current_process = None
                    self.rpc.clear()

                time.sleep(self.config_mgr.poll_interval)

        except KeyboardInterrupt:
            logging.info("Stopping...")
            self.rpc.clear()
            sys.exit(0)