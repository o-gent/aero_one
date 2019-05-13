from client import Client
import os
import subprocess
import threading
import time
import numpy as np
from multiprocessing.pool import ThreadPool
from datetime import datetime
from record import Record
pool = ThreadPool(processes=2)

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
    except Exception as e: print("Make sure Kevin is on and/or restart pycom", end ='\n')
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


# function for fetching signal stregth using windows comands 
def signal_strength():
    return subprocess.check_output(["netsh", "wlan", "show", "network", "mode=Bssid"]).decode().splitlines()[9]

start = time.time()
signal = 0
thresh = 4



with open('kevin_{}.csv'.format(str(datetime.now().time()).replace('.', '_').replace(':', '_')), mode ='w+') as n:
    with open("gps_{}.csv".format(str(datetime.now().time()).replace('.', '_').replace(':', '_')), mode = 'w+') as g:
        r = Record(sock, n, g)

        # loop while connected
        while sock:
            # fetch new data
            try:
                sock.recieve()
                
                
                r.update()
                if sock.gps_data_recieved:
                    r.update_gps()
                
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

                try: print("speed: " + str(sock.gps.speed) + "                      ")
                except: pass
                try: print("altitude: " + str(sock.gps.altitude) + "                      ")
                except: pass
                try: print("heading: " + str(sock.gps.course) + "                      ")
                except: pass

                thetime = time.time()

                if thetime - start > thresh:
                    # start function in other thread
                    async_result = pool.apply_async(signal_strength)
                    thresh = 11
                
                if thetime - start > 5:
                    signal = async_result.get()
                    start = time.time()
                    thresh = 4
                
                sock.signal = signal
                print(signal, flush = True)

                # clear terminal
                print(3000 * '\b', flush= True)
            
            except KeyboardInterrupt:
                r.stop()
                exit()
            except Exception:
                r.stop()
                exit()