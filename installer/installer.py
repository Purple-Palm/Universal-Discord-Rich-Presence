import os
import sys
import subprocess
import time

# These are the packages the installer script itself needs to run
INSTALLER_DEPS = ['winshell', 'win10toast']

def ensure_installer_deps():
    """
    Checks if the installer's own dependencies are met and installs them if not
    """
    print("[+] Checking for installer dependencies...")
    try:
        # Use the version of pip associated with the current python interpreter
        pip_executable = [sys.executable, '-m', 'pip']
        
        # Run pip list to get installed packages
        installed_packages_raw = subprocess.check_output(
            pip_executable + ['list'], 
            text=True, 
            encoding='utf-8'
        )
        installed_packages = {line.split()[0].lower() for line in installed_packages_raw.splitlines()[2:]}

        missing_deps = [dep for dep in INSTALLER_DEPS if dep.lower() not in installed_packages]

        if not missing_deps:
            print("    -> Success: All installer dependencies are present.")
            return True

        print(f"    -> Missing dependencies found: {', '.join(missing_deps)}. Installing...")
        
        # Install missing dependencies
        subprocess.check_call(pip_executable + ['install'] + missing_deps)
        
        print("    -> Success: Installer dependencies installed.")
        # Advise user to re-run if needed, as imports happen at the top level
        print("\n[*] Please re-run the installer to continue.")
        input("    Press Enter to exit.")
        sys.exit(0)

    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"\n[!] Error: Could not check or install dependencies. Ensure Python and pip are installed correctly. Details: {e}")
        input("    Press Enter to exit.")
        sys.exit(1)

# --- Main Script Logic ---
# First, ensure our own dependencies are met.
ensure_installer_deps()

# Now that we know the necessary packages are installed, we can import them.
# This prevents the ImportError you discovered.
import winshell
from win10toast import ToastNotifier

# --- Configuration ---
VENV_DIR = ".venv"
REQUIREMENTS_FILE = "requirements.txt"
MAIN_SCRIPT_PATH = os.path.join("src", "main.py")
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

def install_project_dependencies():
    """Installs dependencies from requirements.txt into the venv."""
    print_step("Installing project packages...")
    
    if sys.platform == "win32":
        python_executable = os.path.join(VENV_DIR, "Scripts", "python.exe")
    else:
        python_executable = os.path.join(VENV_DIR, "bin", "python")

    if not os.path.exists(REQUIREMENTS_FILE):
        print_error(f"'{REQUIREMENTS_FILE}' not found. Cannot install dependencies.")

    try:
        subprocess.check_call([python_executable, "-m", "pip", "install", "-r", REQUIREMENTS_FILE])
        print_success("All project dependencies installed successfully.")
    except subprocess.CalledProcessError as e:
        print_error(f"Failed to install project dependencies. Details: {e}")

def create_desktop_shortcut():
    """Creates a desktop shortcut to run the main application."""
    print_step("Creating desktop shortcut...")
    
    desktop_path = winshell.desktop()
    shortcut_path = os.path.join(desktop_path, SHORTCUT_NAME)
    
    if sys.platform == "win32":
        target_executable = os.path.join(os.getcwd(), VENV_DIR, "Scripts", "pythonw.exe") # Use pythonw.exe to run without a console
    else:
        target_executable = os.path.join(os.getcwd(), VENV_DIR, "bin", "python")
        
    script_to_run = os.path.join(os.getcwd(), MAIN_SCRIPT_PATH)
    
    try:
        with winshell.shortcut(shortcut_path) as shortcut:
            shortcut.path = target_executable
            shortcut.arguments = f'"{script_to_run}"'
            shortcut.working_directory = os.getcwd()
            shortcut.description = "Universal Discord Rich Presence"
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
            icon_path=os.path.join(os.getcwd(), "assets", "icons", "app.ico"),
            duration=10
        )
        print_success("Setup is complete. You can now run the application from the desktop shortcut.")
    except Exception:
        print("\n--- Installation Complete! ---")
        print("Universal Discord RPC is ready. Use the desktop shortcut to start it.")

def main():
    """Main function to run the installer."""
    print("--- Universal Discord RPC Installer ---")
    
    check_python()
    create_virtual_environment()
    install_project_dependencies()
    create_desktop_shortcut()
    notify_completion()
    
    input("\nPress Enter to close the installer.")

if __name__ == "__main__":
    main()
