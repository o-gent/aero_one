# puts all flight telemetry into a data file with appropriate timestamp.

class Record:
    def __init__(self, sock, nw, gw):
        self.sock = sock
        self.w = nw
        self.g = gw
    
    def update(self):
        pass
    
    def update_gps(self):
        pass