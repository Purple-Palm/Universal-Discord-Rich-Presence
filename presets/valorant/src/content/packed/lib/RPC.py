import time
import os
import win32gui
import win32process
import psutil
import yaml
from pypresence import Presence
import asyncio
from InquirerPy.utils import color_print


# Detect active window
def get_active_window_executable():
    window = win32gui.GetForegroundWindow()
    _, pid = win32process.GetWindowThreadProcessId(window)

    try:
        process = psutil.Process(pid)
        return process.name()
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess, Exception):
        return None


# Find matching executable call in config
def get_matching_rpc_id(active_executable):
    global config
    
    is_present = False

    for prog in config['programs']:

        program = config['programs'][prog]

        if active_executable and program['executable'] == active_executable:
            is_present = True
            return is_present, prog

    color_print(
        [
            ('Skyblue',f"{active_executable}"),
            ('Yellow'," was not found"),
            (''," in the config. Nothing to display.")
        ]
    )
    return is_present, prog


# Retrieve RPC conmponents to display
def get_config_status_data(present, program_id):
    global config
    # print("[get_config_status_data]")
    # print("program_id:", program_id)
    if present and program_id:
        # try:

            # Get value of the force_default_id flag 
            force_default_id = config['force_default_id']
            # print("force_default_id:", force_default_id)

            # Set current program to received confing program_id
            program = config['programs'][program_id] 
            # print("program:", program)

            custom_rpc_exe = program.get('custom_rpc_executable_path', None)
            # print("custom_rpc_exe", custom_rpc_exe)

            enabled = program['enable']
            # print("enabled:", enabled)

            name = program['name']
            # print("name:", name)
            
            if custom_rpc_exe == None:

                # Assign defaul_app_id if flag set to true or app_id is not specified
                app_id = config['default_app_id'] if force_default_id or program['app_id'] == "" else program['app_id'] 
                # print("app_id:", app_id)

                # Pull all activity data for RPC from discord_rpc into a dictionary
                activity = {key: str(value) if type(value) is not list else value for key, value in program['discord_rpc'].items()}
                # print("activity:", activity)

            else: 
                app_id = None; activity = None
                
            return enabled, name, app_id, activity, custom_rpc_exe
        
        # except (FileNotFoundError, KeyError, ValueError, Exception) as error:
        #     print("ERROR DURING get_config_status_data: ", type(error), error)
    return False, None, None, None, None
    
# MAIN WORKFLOW
def main():
    
    # GET ALL NEEDED DATA FOR RPC
    active_executable = get_active_window_executable()
    color_print([('Green', f"Active executable changed to: "),('Skyblue', active_executable)])   # Display currently active executable in the console

    is_present, program_rpc_id = get_matching_rpc_id(active_executable)
    enabled, program_name, app_id, activity, custom_rpc_exe = get_config_status_data(is_present, program_rpc_id)

    while get_active_window_executable() == active_executable:
        if enabled and custom_rpc_exe == None:
            client_id = app_id
            RPC = Presence(client_id)
            color_print([('Green', f"RPC executable of "),('Skyblue',f"{program_name}"),('Green'," is specified.\nEstablishing  RPC connection...")])
            RPC.connect()
            color_print([('Green', f"RPC connected, displaying "),('Skyblue', program_name)])

            activity['start'] = time.time()    # Set time of focused activity from the point of connection
            
            activity['pid'] = os.getpid()   # Set process ID to close RPC as soon as this script is closed

            while True:
                if get_active_window_executable() != active_executable:
                    color_print([('Skyblue',f"{program_name}"),(''," is no longer in focus. Closing RPC connection.")])
                    RPC.clear()  # Clear the presence
                    RPC.close()  # Close the RPC connection
                    break

                RPC.update(**activity)  # Update RPC

                time.sleep(15)  # Update every 15 seconds
        
        elif enabled and custom_rpc_exe:
            color_print(
                [
                    ('Green',"Custom RPC executable of "), 
                    ('Skyblue', f"{program_name}"),
                    ('Green'," is specified.\nEstablishing  RPC connection..."),
                ] 
            )
            
            try:
                os.system(custom_rpc_exe)
            except Exception as error:
                color_print(
                    [ 
                        ('Red',"["), ('',"Error"),('Red',"]"),
                        (''," occured while running a "), 
                        ('Blue', "'custom_rpc_executable_path'"),
                        (''," of "),
                        ('Blue', f"'{program_rpc_id}'"),
                        ('',f"\n{type(error), error}") 
                    ] 
                )
                
    time.sleep(1)

# LOADING DATA FROM CONFIG 
try:
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'config.yml')
    with open(config_path, "r") as file:
        config = yaml.safe_load(file)
except Exception as error:
    color_print(
        [ 
            ('Red',"["), ('',"Error"),('Red',"]"),
            ('',f" occured while loading "), 
            ('Blue', f"Config file"), 
            ('',f"\n{type(error), error}") 
        ] 
    )


    

# KEEP RUNNING SCRIPT SEQUENCE
while True:
    if __name__ == "__main__":
        try:
            main()
        except Exception as error:
             color_print([('Red',f'{type(error), error}')])
             break

        