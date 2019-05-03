from client import Client
import os
import subprocess
import threading
import time

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
while output != "connected!":
    try: output = subprocess.check_output(["netsh", "wlan", "connect" , "name=IamDeath,DoW"]).decode()
    except Exception as e: output = e.output.decode(); print("Make sure Kevin is on and/or restart pycom", end ='\n')
    finished = output.splitlines()
    for line in finished: print(line, end = '\n')
    time.sleep(1)


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

_ = os.system('cls')



# loop while connected
while sock:
    # fetch new data
    sock.recieve()

    # ACC raw data
    try: print(sock.data[1], flush = True)
    except: pass
    
    # roll/pitch data   
    try: print(sock.data[2], flush = True)
    except: pass
    
    # Radio channel data
    try: print(sock.data[3], flush = True)
    except: pass

    print(subprocess.check_output(["netsh", "wlan", "show", "network", "mode=Bssid"]).decode().splitlines()[9], flush = True)

    # clear terminal
    print(100* '\b', flush= True)