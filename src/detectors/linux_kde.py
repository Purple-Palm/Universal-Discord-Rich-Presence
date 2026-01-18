# KDE specific calls

# Dependencies: 'kdotool' (yay -S kdotool).

import subprocess
import logging
import shutil
import psutil
from typing import Tuple, Optional
from .base import BaseDetector


class KDEWaylandDetector(BaseDetector):
    def __init__(self):
        if not shutil.which("kdotool"):
            raise FileNotFoundError(
                "CRITICAL: 'kdotool' is missing. \n"
                "Since you are on Arch KDE, please install it: \n"
                "sudo pacman -S kdotool (or yay -S kdotool)"
            )

    def _run_kdotool(self, args: list) -> Optional[str]:
        try:
            result = subprocess.check_output(
                ["kdotool"] + args,
                stderr=subprocess.DEVNULL,
                text=True
            ).strip()
            return result
        except subprocess.CalledProcessError:
            return None

    def get_active_window(self) -> Tuple[Optional[str], Optional[str]]:
        window_id = self._run_kdotool(["getactivewindow"])
        if not window_id:
            return None, None

        window_title = self._run_kdotool(["getwindowname", window_id])

        pid_str = self._run_kdotool(["getwindowpid", window_id])

        process_name = None

        if pid_str and pid_str.isdigit():
            try:
                proc = psutil.Process(int(pid_str))
                process_name = proc.name().lower()  # e.g. "brave" or "steam"
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

        if not process_name:
            window_class = self._run_kdotool(["getwindowclassname", window_id])
            if window_class:
                process_name = window_class.lower()

        return process_name, window_title