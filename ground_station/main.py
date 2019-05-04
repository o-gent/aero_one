from client import Client
import os
import subprocess
import threading
import time
import numpy as np
import matplotlib.pyplot as plt

_ = os.system('cls')

print("""

 ▄▄▄      ▓█████  ██▀███   ▒█████      ▒█████   ███▄    █ ▓█████ 
▒████▄    ▓█   ▀ ▓██ ▒ ██▒▒██▒  ██▒   ▒██▒  ██▒ ██ ▀█   █ ▓█   ▀ 
▒██  ▀█▄  ▒███   ▓██ ░▄█ ▒▒██░  ██▒   ▒██░  ██▒▓██  ▀█ ██▒▒███   
░██▄▄▄▄██ ▒▓█  ▄ ▒██▀▀█▄  ▒██   ██░   ▒██   ██░▓██▒  ▐▌██▒▒▓█  ▄ 
 ▓█   ▓██▒░▒████▒░██▓ ▒██▒░ ████▓▒░   ░ ████▓▒░▒██░   ▓██░░▒████▒
 ▒▒   ▓▒█░░░ ▒░ ░░ ▒▓ ░▒▓░░ ▒░▒░▒░    ░ ▒░▒░▒░ ░ ▒░   ▒ ▒ ░░ ▒░ ░
  ▒   ▒▒ ░ ░ ░  ░  ░▒ ░ ▒░  ░ ▒ ▒░      ░ ▒ ▒░ ░ ░░   ░ ▒░ ░ ░  ░
  ░   ▒      ░     ░░   ░ ░ ░ ░ ▒     ░ ░ ░ ▒     ░   ░ ░    ░   
      ░  ░   ░  ░   ░         ░ ░         ░ ░           ░    ░  ░
                                                                 
""")


# wait to connect to the network
# netsh wlan connect name=PROFILE_NAME interface="[netsh wlan show interfaces]"
output = 0
while output != "Connection request was completed successfully.":
    try: output = subprocess.check_output(["netsh", "wlan", "connect" , "name=kevin"]).decode().strip()
    except Exception as e: output = e.output.decode(); print("Make sure Kevin is on and/or restart pycom", end ='\n')
    finished = output.splitlines()
    for line in finished: print(line, end = '\n')
    time.sleep(4)


# get signal of closest WiFi network
print(subprocess.check_output(["netsh", "wlan", "show", "network", "mode=Bssid"]).decode().splitlines()[9])

_ = os.system('cls')

print("""

 ██████╗ ███████╗███╗   ██╗████████╗
██╔════╝ ██╔════╝████╗  ██║╚══██╔══╝
██║  ███╗█████╗  ██╔██╗ ██║   ██║   
██║   ██║██╔══╝  ██║╚██╗██║   ██║   
╚██████╔╝███████╗██║ ╚████║   ██║   
 ╚═════╝ ╚══════╝╚═╝  ╚═══╝   ╚═╝   
                                    

""")

print("connecting...")
# connect to drone
sock = Client('192.168.4.1')

if not sock.sock:
    print("")
    print("Failed!")
    time.sleep(1)
    exit()

time.sleep(1)

_ = os.system('cls')



start = time.time()
signal = 0

try:
    # loop while connected
    while sock:
        # fetch new data
        sock.recieve()

        # ACC raw 
        try: print("ACC raw: " + str(sock.data[1]) + "                      " )
        except: pass
        
        # roll/pitch   
        try: print("roll/pitch: " + str(sock.data[2]) + "                      ")
        except: pass

        # Radio channel
        try: print("Radio channel: " + str(sock.data[3]) + "                      ")
        except: pass

        # channel target
        try: print("channel target: " + str(sock.data[4]) + "                      ")
        except: pass
        
        # pressure 
        try: print("pressure data: " + str(sock.data[5]) + "                      ")
        except: pass
        
        # pressure 
        try: print("loop time: " + str(sock.data[0]) + "                      ")
        except: pass
        
        if time.time() - start > 10:
            # this needs to be a call back rather than interupting the main loop
            signal = subprocess.check_output(["netsh", "wlan", "show", "network", "mode=Bssid"]).decode().splitlines()[9]
            start = time.time()
        print(signal, flush = True)

        # clear terminal
        print(2000 * '\b', flush= True)

except:
    sock.sock.close()