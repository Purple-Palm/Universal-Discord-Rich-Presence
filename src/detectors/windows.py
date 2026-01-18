import ctypes
from ctypes import wintypes
import time
import os

# --- Win32 API Constants & Structures ---
PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
psapi = ctypes.WinDLL('psapi')
kernel32 = ctypes.WinDLL('kernel32')
user32 = ctypes.WinDLL('user32')


def get_active_window_process_name():
    # 1. Get the handle of the active window
    hwnd = user32.GetForegroundWindow()

    if hwnd == 0:
        return None

    # 2. Get the Process ID (PID) from the window handle
    pid = wintypes.DWORD()
    user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))

    # 3. Open the process to read its information
    # We use PROCESS_QUERY_LIMITED_INFORMATION for better permissions compatibility
    process_handle = kernel32.OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, False, pid)

    if not process_handle:
        # If we can't open the process (e.g., it's a system process), return the PID or a placeholder
        return f"Protected Process (PID: {pid.value})"

    try:
        # 4. Get the full path of the executable
        # Create a buffer for the path (MAX_PATH is usually 260, but paths can be longer)
        buffer_size = 1024
        exe_path_buffer = ctypes.create_unicode_buffer(buffer_size)

        # Determine the length of the string
        buffer_len = wintypes.DWORD(buffer_size)

        success = kernel32.QueryFullProcessImageNameW(
            process_handle,
            0,
            exe_path_buffer,
            ctypes.byref(buffer_len)
        )

        if success:
            full_path = exe_path_buffer.value
            # 5. Extract just the filename from the path
            exe_name = os.path.basename(full_path)
            return exe_name
        else:
            return "Unknown"

    finally:
        # Always close the handle to prevent memory leaks
        kernel32.CloseHandle(process_handle)


def main():
    print("Monitoring active application EXE... (Press Ctrl+C to stop)")
    print("-" * 50)

    last_exe = None

    try:
        while True:
            current_exe = get_active_window_process_name()

            if current_exe != last_exe:
                if current_exe:
                    print(f"Active App: {current_exe}")
                last_exe = current_exe

            time.sleep(1)

    except KeyboardInterrupt:
        print("\nStopping monitor.")


if __name__ == "__main__":
    main()