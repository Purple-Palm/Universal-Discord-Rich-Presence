import ctypes
import psutil
from typing import Tuple, Optional


class WindowsDetector:
    def __init__(self):
        self.user32 = ctypes.windll.user32
        self.kernel32 = ctypes.windll.kernel32

    def get_active_window(self) -> Tuple[Optional[str], Optional[str]]:
        hwnd = self.user32.GetForegroundWindow()

        pid = ctypes.c_ulong()
        self.user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))

        if pid.value == 0:
            return None, None

        try:
            process = psutil.Process(pid.value)
            process_name = process.name().lower()
        except psutil.NoSuchProcess:
            return None, None

        length = self.user32.GetWindowTextLengthW(hwnd)
        buff = ctypes.create_unicode_buffer(length + 1)
        self.user32.GetWindowTextW(hwnd, buff, length + 1)
        window_title = buff.value

        return process_name, window_title