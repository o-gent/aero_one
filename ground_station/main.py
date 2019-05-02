from client import Client

# connect to drone
sock = Client('192.168.4.1')

# loop while connected
while sock:
    # fetch new data
    sock.recieve()

    # ACC raw data
    try: print(sock.data[1])
    except: pass
    
    # roll/pitch data   
    try: print(sock.data[2])
    except: pass
    
    # Radio channel data
    try: print(sock.data[3])
    except: pass
