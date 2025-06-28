import os
import sys
import subprocess
import shutil
import winshell
from win10toast import ToastNotifier

# --- Configuration ---
VENV_DIR = ".venv"
REQUIREMENTS_FILE = "requirements.txt"
MAIN_SCRIPT_PATH = os.path.join("src", "main.py")
CONFIG_SRC_PATH = "config.yml"
SHORTCUT_NAME = "Universal Discord RPC.lnk"

def print_step(message):
    """Prints a formatted step message to the console."""
    print(f"\n[+] {message}")

def print_success(message):
    """Prints a formatted success message."""
    print(f"    -> Success: {message}")

def print_error(message):
    """Prints a formatted error message and exits."""
    print(f"\n[!] Error: {message}")
    input("    Press Enter to exit.")
    sys.exit(1)

def check_python():
    """Checks if Python is installed and accessible."""
    print_step("Checking for Python installation...")
    try:
        version = subprocess.check_output([sys.executable, "--version"], text=True).strip()
        print_success(f"Python found: {version}")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print_error("Python is not installed or not in your system's PATH. Please install Python 3.11+ and try again.")

def create_virtual_environment():
    """Creates a virtual environment if it doesn't exist."""
    print_step(f"Setting up virtual environment in '{VENV_DIR}'...")
    if os.path.exists(VENV_DIR):
        print_success("Virtual environment already exists.")
        return
    
    try:
        subprocess.check_call([sys.executable, "-m", "venv", VENV_DIR])
        print_success("Virtual environment created.")
    except subprocess.CalledProcessError as e:
        print_error(f"Failed to create virtual environment. Details: {e}")

def install_dependencies():
    """Installs dependencies from requirements.txt into the venv."""
    print_step("Installing required packages...")
    
    # Determine the correct path to the python executable in the venv
    if sys.platform == "win32":
        python_executable = os.path.join(VENV_DIR, "Scripts", "python.exe")
    else:
        python_executable = os.path.join(VENV_DIR, "bin", "python")

    if not os.path.exists(REQUIREMENTS_FILE):
        print_error(f"'{REQUIREMENTS_FILE}' not found. Cannot install dependencies.")

    try:
        # Install dependencies using the venv's pip
        subprocess.check_call([python_executable, "-m", "pip", "install", "-r", REQUIREMENTS_FILE])
        print_success("All dependencies installed successfully.")
    except subprocess.CalledProcessError as e:
        print_error(f"Failed to install dependencies. Details: {e}")

def create_desktop_shortcut():
    """Creates a desktop shortcut to run the main application."""
    print_step("Creating desktop shortcut...")
    
    desktop_path = winshell.desktop()
    shortcut_path = os.path.join(desktop_path, SHORTCUT_NAME)
    
    # The target is the venv's Python executable
    if sys.platform == "win32":
        target_executable = os.path.join(os.getcwd(), VENV_DIR, "Scripts", "python.exe")
    else:
        target_executable = os.path.join(os.getcwd(), VENV_DIR, "bin", "python")
        
    script_to_run = os.path.join(os.getcwd(), MAIN_SCRIPT_PATH)
    
    # Use winshell to create the shortcut
    try:
        with winshell.shortcut(shortcut_path) as shortcut:
            shortcut.path = target_executable
            shortcut.arguments = f'"{script_to_run}"'
            shortcut.working_directory = os.getcwd()
            shortcut.description = "Universal Discord Rich Presence"
            # You can set an icon if you have one in the assets folder
            icon_path = os.path.join(os.getcwd(), "assets", "icons", "app.ico")
            if os.path.exists(icon_path):
                shortcut.icon_location = (icon_path, 0)
        
        print_success(f"Shortcut created on your desktop: '{SHORTCUT_NAME}'")
    except Exception as e:
        print_error(f"Could not create desktop shortcut. Details: {e}")

def notify_completion():
    """Sends a desktop notification that the installation is complete."""
    print_step("Finishing up...")
    try:
        toaster = ToastNotifier()
        toaster.show_toast(
            "Installation Complete!",
            "Universal Discord RPC is ready. Use the desktop shortcut to start it.",
            duration=10
        )
        print_success("Setup is complete. You can now run the application from the desktop shortcut.")
    except Exception:
        # Fallback if notification fails
        print("\n--- Installation Complete! ---")
        print("Universal Discord RPC is ready. Use the desktop shortcut to start it.")


def main():
    """Main function to run the installer."""
    print("--- Universal Discord RPC Installer ---")
    
    check_python()
    create_virtual_environment()
    install_dependencies()
    create_desktop_shortcut()
    notify_completion()
    
    input("\nPress Enter to close the installer.")

if __name__ == "__main__":
    main()
