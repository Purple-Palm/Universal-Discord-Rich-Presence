import os

FILES_TO_INCLUDE = [
    # Scripts
    ".py", ".bat",
    # Configs
    ".json", ".ini", ".cfg", ".toml", ".yaml", ".yml",
    # Dependencies & Docs
    "requirements.txt", ".env", "README.md"
]

# Name of the file that will contain all the collected data
OUTPUT_FILENAME = "all_project_files.txt"


def main():
    """
    Walks through the current directory and subdirectories, collecting the content
    of specified files into a single output file.
    """
    print(f"Starting to collect data into '{OUTPUT_FILENAME}'...")
    count = 0
    # Open the output file with UTF-8 encoding
    with open(OUTPUT_FILENAME, "w", encoding="utf-8") as outfile:
        # Walk through the directory tree starting from the current directory '.'
        for root, _, files in os.walk("."):
            for filename in files:
                # Check if the file should be included based on its extension or name
                if any(filename.endswith(ext) for ext in FILES_TO_INCLUDE) or filename in FILES_TO_INCLUDE:
                    # Skip the script itself
                    if filename == os.path.basename(__file__):
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

    print(f"\nFinished! Collected data from {count} files into '{OUTPUT_FILENAME}'.")


if __name__ == "__main__":
    main()