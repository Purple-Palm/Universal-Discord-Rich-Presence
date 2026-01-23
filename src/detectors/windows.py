import ctypes
import psutil
from typing import Tuple, Optional


class WindowsDetector:
    def __init__(self):
        self.user32 = ctypes.windll.user32

    def get_active_window(self) -> Tuple[Optional[str], Optional[str]]:
        hwnd = self.user32.GetForegroundWindow()
        if not hwnd:
            return None, None

        pid = ctypes.c_ulong()
        self.user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))

        if pid.value == 0:
            return None, None

        try:
            # Optimized: We only need the name, not the full object
            proc = psutil.Process(pid.value)
            process_name = proc.name().lower()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            return None, None

        length = self.user32.GetWindowTextLengthW(hwnd)
        if length > 0:
            buff = ctypes.create_unicode_buffer(length + 1)
            self.user32.GetWindowTextW(hwnd, buff, length + 1)
            window_title = buff.value
        else:
            window_title = ""

        return process_name, window_title