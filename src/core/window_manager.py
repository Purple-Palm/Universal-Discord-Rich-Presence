import sys
import psutil

# Conditional import for platform-specific window management
if sys.platform == "win32":
    import win32gui
    import win32process
else:
    # Placeholder for Linux/macOS in the future probably without macOS support.
    # Might use libraries like 'Xlib' for Linux or 'AppKit' for macOS but Im not sure that we gonna make it work on macOS lol.
    pass

class WindowManager:
    """
    Handles detecting the currently focused window and its associated process.
    Currently implemented for Windows.
    """
    def get_active_window_executable(self):
        """
        Returns the process name of the currently focused window.
        Returns None if the process can't be identified.
        """
        if sys.platform != "win32":
            print("[WARNING] Window monitoring is only supported on Windows.")
            return None
            
        try:
            hwnd = win32gui.GetForegroundWindow()
            if not hwnd:
                return None

            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            if pid == 0:
                return None
                
            process = psutil.Process(pid)
            return process.name()
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            # These exceptions are common (e.g., when switching to system processes) and can be safely ignored.
            
            return None
        except Exception:
            # Catch other potential errors with win32gui/psutil
            return None

