import socket

class datalink_setup():
    def __enter__(self):
        return Server()

    def __exit__(self, type, value, traceback):
            print(type)
            return True


class Server():
    def __init__(self):
        self.string = " "
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            sock.bind(('0.0.0.0',5000))
            sock.listen()

            client, addr = sock.accept()
            print(addr, " connected!")
        
            # initialised messaged
            print(addr, client.recv(1024))
            
            self.sock = client #socket connection to client
        
        except Exception as e:
            print("there was an exception! {}".format(e))
            sock.close()
        
    def send(self, id_, message):
        try:
            self.string = str(id_) + "_" + str(message) + "@"
            self.sock.send(self.string.encode())
        except Exception as e:
            print(e)
        
        #string = str(id_) + "_" + str(message) + "@"
        #self.sock.send(string.encode())