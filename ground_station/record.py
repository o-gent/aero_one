# puts all flight telemetry into a data file with appropriate timestamp.
import csv
from datetime import datetime

class Record:
    def __init__(self, sock, nw, gw):
        self.sock = sock
        
        self.sock.gps.start_logging('gps_log{}'.format(str(datetime.now().time()).replace('.', '_').replace(':', '_')))

        # write header for normal file
        self.n_writer = csv.writer(nw, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL, lineterminator = '\n')
        self.n_writer.writerow(['time', 'loop time', 'ACC raw', 'roll/pitch', 'radio channel', 'channel target', 'pressure data', 'signal strength'])
        

        self.g_writer = csv.writer(gw, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL, lineterminator = '\n')
        self.g_writer.writerow(['time', 'speed', 'altitude', 'heading'])
    
    def update(self):
        self.n_writer.writerow([str(datetime.now().time()), self.sock.data[0], self.sock.data[1], self.sock.data[2], self.sock.data[3], self.sock.data[4], self.sock.data[5], self.sock.signal])
    
    def update_gps(self):
        self.g_writer.writerow([str(datetime.now().time()), self.sock.gps.speed, self.sock.gps.altitude, self.sock.gps.course])
    
    def stop(self):
        self.sock.gps.stop_logging()