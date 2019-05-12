import socket
import select
from microgps import MicropyGPS

class Client():
    def __init__(self, ip):
        self.data = {}
        self.gps = MicropyGPS()

        try:
            #'192.168.4.1'
            sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM ) #socket.SOCK_DGRAM
            sock.connect((ip,5000))
            sock.send(b'initialise')
            #sock.setblocking(0)
            self.sock = sock
        
        except Exception as e:
            self.sock = None
            print("Socket failed to connect! exception {}".format(e))
    
    def recieve(self):
        try:
            raw = self.sock.recv(1024)
            raw = raw.decode()
            
            raw = raw.splitlines()
            
            for line in raw:
                if line.startswith('$'):
                    for x in line:
                        self.gps.update(x)

                else:
                    line = line.strip().split('@')
                    line.pop()

                    for data in line:
                        id_ = int(data[0])
                        message = data[3:-1]
                        message = message.split(',')
                        l = []
                        for i in message:
                            l.append(float(i))
                        message = l

                        self.data[id_] = message

        except Exception as e:
            #print(e)
            pass


if __name__ == "__main__":
    sock = Client('192.168.4.1')
    while sock:
        sock.recieve()
        print(sock.data)
        #print(sock.gps_data)
