import shutil
import subprocess
import psutil
import logging
from typing import Tuple, Optional
from src.detectors.base import BaseDetector


class KDEWaylandDetector(BaseDetector):
    def __init__(self):
        # Graceful Dependency Check
        if not shutil.which("kdotool"):
            print("\n" + "=" * 50)
            print("❌ CRITICAL ERROR: 'kdotool' is missing!")
            print("This is required for Linux KDE Wayland support.")
            print("👉 Please run: sudo pacman -S kdotool (or yay -S kdotool)")
            print("=" * 50 + "\n")
            raise SystemExit(1)

    def _run_cmd(self, args: list) -> Optional[str]:
        try:
            return subprocess.check_output(
                ["kdotool"] + args,
                text=True,
                stderr=subprocess.DEVNULL
            ).strip()
        except Exception:
            return None

    def get_active_window(self) -> Tuple[Optional[str], Optional[str]]:
        win_id = self._run_cmd(["getactivewindow"])
        if not win_id:
            return None, None

        title = self._run_cmd(["getwindowname", win_id])
        pid_str = self._run_cmd(["getwindowpid", win_id])

        process_name = None

        # Try finding process name via PID
        if pid_str and pid_str.isdigit():
            try:
                proc = psutil.Process(int(pid_str))
                process_name = proc.name().lower()
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

        # Fallback to Window Class if PID fails
        if not process_name:
            cls = self._run_cmd(["getwindowclassname", win_id])
            if cls:
                process_name = cls.lower()

        return process_name, title