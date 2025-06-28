import os
import subprocess
import platform

# --- Configuration ---

# The file that will store the directory tree structure.
STRUCTURE_FILENAME = "project_structure.txt"

# The file that will contain all the collected source code and configs.
CONTENT_FILENAME = "all_project_files.txt"

# Add any other file extensions or exact filenames you want to include.
FILES_TO_INCLUDE = [
    # Scripts
    ".py", ".bat",
    # Configs
    ".json", ".ini", ".cfg", ".toml", ".yaml", ".yml",
    # Dependencies & Docs
    "requirements.txt", ".env", "README.md"
]

# --- NEW: Add folders you wish to ignore here ---
FOLDERS_TO_EXCLUDE = [
    ".venv",
    "__pycache__",
    ".git",
    ".vscode",
]

# --- End of Configuration ---


def generate_file_structure():
    """Generates a file and directory structure tree."""
    print(f"Generating project structure in '{STRUCTURE_FILENAME}'...")
    
    system = platform.system()
    command = ""

    if system == "Windows":
        command = f'tree /f /a > "{STRUCTURE_FILENAME}"'
    elif system in ["Linux", "Darwin"]: # Darwin is macOS
        try:
            subprocess.run(["tree", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            command = f'tree -a -I "{"|".join(FOLDERS_TO_EXCLUDE)}" > "{STRUCTURE_FILENAME}"'
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("  'tree' command not found. Falling back to 'ls -R' (cannot exclude folders).")
            command = f'ls -R > "{STRUCTURE_FILENAME}"'
    else:
        print(f"Unsupported operating system: {system}. Skipping structure generation.")
        return

    try:
        subprocess.run(command, shell=True, check=True)
        print(f"  [+] Successfully created '{STRUCTURE_FILENAME}'")
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"  [!] Failed to generate project structure. Error: {e}")


def collect_file_contents():
    """
    Walks through the directory, collecting the content of specified files.
    """
    print(f"\nCollecting file contents into '{CONTENT_FILENAME}'...")
    count = 0
    with open(CONTENT_FILENAME, "w", encoding="utf-8") as outfile:
        # Walk through the directory tree
        for root, dirs, files in os.walk("."):
            
            # --- MODIFIED: This line ignores the specified folders ---
            dirs[:] = [d for d in dirs if d not in FOLDERS_TO_EXCLUDE]
            
            for filename in files:
                # Check if the file should be included
                if any(filename.endswith(ext) for ext in FILES_TO_INCLUDE) or filename in FILES_TO_INCLUDE:
                    # Skip the script itself and the output files
                    if filename in [os.path.basename(__file__), STRUCTURE_FILENAME, CONTENT_FILENAME]:
                        continue
                        
                    file_path = os.path.join(root, filename)
                    
                    try:
                        # Write a separator with the file path
                        outfile.write(f"--- {file_path} ---\n\n")
                        
                        # Open the source file and write its content
                        with open(file_path, "r", encoding="utf-8", errors="ignore") as infile:
                            outfile.write(infile.read())
                        
                        outfile.write("\n\n")
                        count += 1
                        print(f"  [+] Added: {file_path}")

                    except Exception as e:
                        print(f"  [!] Could not read file {file_path}: {e}")

    print(f"\nFinished! Collected data from {count} files.")


def main():
    """Main function to run the data collection process."""
    generate_file_structure()
    collect_file_contents()
    print(f"\nAll done! Please share the contents of '{STRUCTURE_FILENAME}' and '{CONTENT_FILENAME}'.")


if __name__ == "__main__":
    main()