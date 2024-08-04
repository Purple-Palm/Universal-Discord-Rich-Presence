from pypresence import Presence
from InquirerPy.utils import color_print
import glob, urllib, requests, json, os, time, win32gui, win32process, random , psutil, os, yaml

# Get data between lines of Roblox logs
def find_between(s, first, last):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

# Check if roblox window is in focus 
def check_roblox_focus():
        def get_active_window_process_name():
            hwnd = win32gui.GetForegroundWindow()
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            for proc in psutil.process_iter(['pid', 'name']):
                if proc.info['pid'] == pid:
                    return proc.info['name']
            return None

        # Exit the script in case window is not focused
        active_window_process = get_active_window_process_name()
        if active_window_process != "RobloxPlayerBeta.exe":
            exit_roblox_rpc()
        return True

# Exit the script 
def exit_roblox_rpc():
    #subprocess.Popen([sys.executable, "main.py"])
    print('leaving roblox rpc')
    os._exit(1)

# Get path to user folder
def getUser():
    return os.environ['USERPROFILE'].replace("C:\\Users\\", "")

# Load latest Roblox log file by creation time
def getCacheLog():
    list_of_files = glob.glob("C:\\Users\\" + getUser() + "\\AppData\\Local\\Roblox\\logs" + "\*.log") # get data about all .log files
    latest_file = max(list_of_files, key=os.path.getctime) # Get path to a latest created Roblox log file
    fin = open(latest_file, "r", encoding = "ISO-8859-1").readlines() # Open log file
    return fin

# Get required values from log file
def getValuesFromCacheLog(logFile):

    placeId = 0 
    jobId = 0
    lastJobid = 0
    serverIp = 0
    usrId = 1
    isPrivate = False
    connected = True 

    line_position = 0 
    for line in logFile: # Go through the log file
        
        # Getting placeId
        if line.find("place") > 0:
            toReplace = find_between(line, 'place ', " at")
            if toReplace != "":
                placeId = toReplace
                line_position = logFile.index(line)
                print(logFile.index(line), type(line), line)

        # Getting jobId
        if line.find("Joining game") > 0:
            toReplace = find_between(line, "Joining game '", "'")
            if toReplace != "":
                jobId = toReplace
                line_position = logFile.index(line)
                print(logFile.index(line), type(line), line)

        # Getting serverIp
        if line.find("UDMUX") > 0:
            toReplace = find_between(line, "UDMUX server ", ",")
            if toReplace != "":
                serverIp = toReplace.split(":")
                line_position = logFile.index(line)
                print(logFile.index(line), type(line), line)

        # Getting userId
        if line.find("userid") > 0:
            toReplace = find_between(line, "userid:", ",")
            if toReplace != "":
                usrId = toReplace
                line_position = logFile.index(line)
                print(logFile.index(line), type(line), line)

        # Is it a private server
        if line.find("joinGamePostPrivateServer") > 0:
            isPrivate = True
            line_position = logFile.index(line)
            print(logFile.index(line), type(line), line)

    # Determining if the most resent message was about being Disconnected
    for line in logFile:
        if line.find("Client:Disconnect") > 0 and logFile.index(line) > line_position:
            connected = False
            print(line_position)
            print(logFile.index(line), type(line), line)
        
    return connected, placeId, jobId, lastJobid, serverIp, usrId, isPrivate

# Merge data from log and config to create RPC options
def getDataForRPC(connected, placeId, jobId, lastJobid, usrId, isPrivate, config):
    rblx_logo = "https://blog.roblox.com/wp-content/uploads/2022/08/RBLX_Logo_Launch_Wordmark.png"
    activity = {} 

    activity['pid'] = os.getpid()   # Set process ID to close RPC as soon as this script is closed

    programs = config['programs'] # Getting data of all programs in config
    robloxSettings = programs["Dyl's Roblox RPC"] # Getting data of roblox-rpc settings
    robloxRPC = robloxSettings['discord_rpc'] # Getting rpc options

    # If not connected display idle status
    if connected == False:
        activity['details'] = "Idle in Menu"
        activity['large_image'] = rblx_logo

        return activity

    # if connected display all needed info
    elif placeId and jobId:
        if lastJobid != jobId:
            universalId = urllib.request.urlopen("https://apis.roblox.com/universes/v1/places/" + placeId + "/universe")
            universalData = json.loads(universalId.read())
            theId = universalData["universeId"]

            lastJobid = jobId

            # Getting data and images
            if theId:
                print(universalData, jobId, "to", lastJobid)
                
                response = urllib.request.urlopen("https://games.roblox.com/v1/games?universeIds=" + str(theId))
                data = json.loads(response.read())

                responsePlayer = urllib.request.urlopen("https://users.roblox.com/v1/users/" + str(usrId))
                dataPlayer = json.loads(responsePlayer.read())

                responeIcon = urllib.request.urlopen("https://thumbnails.roblox.com/v1/games/icons?universeIds=" + str(theId) + "&size=512x512&format=Png&isCircular=false")
                dataIcon = json.loads(responeIcon.read())

                responePfp = urllib.request.urlopen("https://thumbnails.roblox.com/v1/users/avatar-headshot?userIds=" + str(usrId) + "&size=48x48&format=Png&isCircular=false")
                dataPfp = json.loads(responePfp.read())

                gameIcon = dataIcon["data"][0]["imageUrl"]
                pfpIcon = dataPfp["data"][0]["imageUrl"]

        # Setting up the activity  
        activity['details'] = data["data"][0]["name"]
        activity['state'] = "By " + data["data"][0]["creator"]["name"]
        activity['large_image'] = gameIcon
        activity['large_text'] = data["data"][0]["name"]
        activity['small_image'] = pfpIcon
        activity['small_text'] = dataPlayer["name"]
        activity['buttons'] = [] 
        for button_dict in robloxRPC['buttons']: # Loop used to format values in buttons' urls
            updated_dict = {}
            for k, v in button_dict.items():
                updated_dict[k] = v.format(PLACEID=placeId, JOBID=jobId)
            activity['buttons'].append(updated_dict)

        # If private display about server being private
        if isPrivate:
            activity['small_image'] = rblx_logo
            activity['small_text'] = "Protected"
            activity['state'] = "Reversed server"
        
        return activity
    
    # In all other cases display idle
    else:
        activity['details'] = "Idle in Menu"
        activity['large_image'] = rblx_logo
        
        return activity

# Workflow to go through the functions and pass the data to create RPC options
def get_activity(config):
    logFile = getCacheLog()

    connected, placeId, jobId, lastJobid, serverIp, usrId, isPrivate = getValuesFromCacheLog(logFile)
    print(getValuesFromCacheLog(logFile))

    activity = getDataForRPC(connected, placeId, jobId, lastJobid, usrId, isPrivate, config)
    print(activity)

    return activity

# Get client id from config
def getConfigSettings(config):
    if config:
    
        programs = config['programs']
        robloxSettings = programs["Dyl's Roblox RPC"]
        clientId = robloxSettings['app_id']
        print('client id success')

        return clientId
    return None

# Load config file from top level folders
def loadConfig():
    script_dir = os.path.dirname(__file__)

    rel_path = "../../config.yml"

    abs_path = os.path.join(script_dir, rel_path)

    try:
        with open(abs_path, "r") as file:
            config = yaml.safe_load(file)
        print('success config')
        return config
        
    except Exception as error:
        color_print(
            [ 
                ('Red',"["), ('',"Error"),('Red',"]"),
                ('',f" occured while loading "), 
                ('Blue', f"Config file"), 
                ('',f"\n{type(error), error}") 
            ] 
        )
    return None

# Main workflow
def main():
    config = loadConfig()
    clientId = getConfigSettings(config)
    while check_roblox_focus() and clientId:
            
            activity = get_activity(config)
            print(activity)
            
            print("Starting Client")
            print("Waiting for Discord network...")

            RPC = Presence(clientId)
            RPC.connect()
            print("Connected to Discord network!")

            start_time = time.time()
            activity['start'] = start_time   # Set time of focused activity from the point of connection

            while True:
                check_roblox_focus()

                newActivity = get_activity(config)
                newActivity['start'] = start_time
                if activity != newActivity:
                    print(newActivity)
                    RPC.clear()  # Clear the presence
                    RPC.close()  # Close the RPC connection
                    break

                RPC.update(**activity)
            
                time.sleep(15)
    
if __name__ == "__main__":
        try:
            main()
        except Exception as error:
             color_print([('Red',f'{type(error), error}')])
