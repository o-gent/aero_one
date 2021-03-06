# LEGACY

import socket

class datalink_setup():
    def __init__(self, mode):
        self.mode = mode

    def __enter__(self):
        return Datalink(self.mode)

    def __exit__(self, type, value, traceback):
            print(type)
            return True

class Datalink():
    def __init__(self, mode):
        self.mode = mode
        # start connection
        if mode == "client":
            self.sock = connect()
        if mode == "server":
            self.sock = serve()
        
        #initise class wide variables
        self.packets = {}
        self._queue = []
        self.temp_id = 0

    def _id_register(self, id_):
        # add an entry for new ids
        self.packets[id_] = {}
        self.packets[id_]['payload'] = [0]

    def refresh(self):
        """ send recieve new data changes """
        if self.mode == "client":
            self.sock.send(self.process_send().encode())
            self.process_recieve(self.sock.recv(1024))
        else:
            self.process_recieve(self.sock.recv(1024))
            self.sock.send(self.process_send().encode())
        
        # empty queue
        self._queue = []

    def process_recieve(self, recieved):
        for payload in string_to_list(recieved.decode()):
            try:
                self.packets[payload[0]]['payload'] = payload[1:]
            except:
                self._id_register(payload[0])
                self.packets[payload[0]]['payload'] = payload[1:]

    def process_send(self):
        try:
            to_send = []
            for id_ in self._queue:
                to_send.append([id_] + self.packets[id_]['payload'])
            return list_to_string(to_send)
        except:
            return list_to_string([0,0])

    def put(self, id_, message):
        # payload -> self.packets
        try:
            self.packets[id_]
        except:
            self._id_register(id_)

        self.packets[id_]['payload'] = message
        # append id_ to self.queue
        self._queue.append(id_)

    def get(self, id_):
        try: return self.packets[id_]['payload']
        except: return False

def list_to_string(the_list):
    """ converts list of ints to string """
    a = ''
    for secondary_list in the_list:
        a += ' '
        for item in secondary_list:
            a += str(item)
            a += ','
        a += ' '
    return a

def string_to_list(the_string):
    """ converts string to list of ints """
    l = []
    seperate_secondaries = the_string.split()
    for secondary in enumerate(seperate_secondaries):
        l.append([])
        for item in secondary[1].split(',')[:-1]:
            l[secondary[0]].append(int(item))
    return l


# socket connection functions 

def connect():
    sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM ) #socket.SOCK_DGRAM
    sock.connect(('192.168.4.1',5000))
    sock.send(b'initialise')
    print("connected!!")
    return sock

def serve():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    sock.bind(('0.0.0.0',5000))
    sock.listen()

    client, addr = sock.accept()
    print(addr, " connected!")
    # initialised messaged
    print(addr, client.recv(1024))
    
    return client