import socket


class Client():
    def __init__(self, ip):
        self.data = {}

        try:
            #'192.168.4.1'
            sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM ) #socket.SOCK_DGRAM
            sock.connect((ip,5000))
            sock.send(b'initialise')
            self.sock = sock
        except Exception as e:
            print("Socket failed to connect! exception {}".format(e))
    
    def recieve(self):
        try:
            raw = self.sock.recv(1024)
            raw = raw.decode()

            raw = raw.strip().split('@')
            raw.pop()

            for data in raw:
                id_ = int(data[0])
                message = data[3:-1]
                message = message.split(',')
                l = []
                for i in message:
                    l.append(int(i))
                message = l

                self.data[id_] = message
        
        except Exception as e:
            pass


if __name__ == "__main__":
    sock = Client('192.168.4.1')
    while sock:
        sock.recieve()
        print(sock.data)
