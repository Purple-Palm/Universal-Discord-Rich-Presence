import os
import requests
import yaml
import shutil
import ctypes
from win10toast import ToastNotifier
import subprocess

# Define paths
working_dir = os.path.dirname(os.path.realpath(__file__))
version_file_path = os.path.join(working_dir, 'version.yml')
desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
bat_file_path = os.path.join(working_dir, 'REINSTALL-UPDATE.bat')

# Load the local version
with open(version_file_path, 'r') as version_file:
    local_version = str(yaml.safe_load(version_file)['Version']).strip()

# Fetch the GitHub README.md
url = "https://raw.githubusercontent.com/Purple-Palm/Universal-Discord-Rich-Presence/main/README.md"
response = requests.get(url)
github_readme = response.text

# Extract the version from the README.md
version_prefix = "Version: "
github_version = None

for line in github_readme.split('\n'):
    if line.startswith(version_prefix):
        github_version = line.split(version_prefix)[-1].strip()
        break

if github_version is None:
    raise ValueError("Version information not found in README.md")

# Debug: Print versions
print(f"Local version: '{local_version}'")
print(f"GitHub version: '{github_version}'")

# Initialize toaster
toaster = ToastNotifier()

# Compare versions
if local_version != github_version:
    # Debug: Version mismatch
    print("Versions do not match. Update found. 🔄")

    # Send notification for update
    toaster.show_toast(f"🔄 {github_version} Update Found", f"An update for the RPC is available. You are on V{local_version}. Updating...", icon_path="icons/custom-logo2.ico", duration=10)

    # Run the batch file directly
    subprocess.Popen(bat_file_path, creationflags=subprocess.CREATE_NO_WINDOW)

    # Terminate the script
    exit()
else:
    # Debug: Version match
    print("Versions match. No update found. ✅")

    # Send notification for no update
    toaster.show_toast("✅ No Update Found", "RPC script is up-to-date.", duration=10)

# If no update, run main.bat in the background
main_bat_path = os.path.join('main-start.bat')
subprocess.Popen(main_bat_path, creationflags=subprocess.CREATE_NO_WINDOW)
