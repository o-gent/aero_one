from record import Record
from datetime import datetime
import time

class GPS:
    def __init__(self):
        self.speed = 0
        self.altitude = 0
        self.course = 0

class Sock:
    def __init__(self):
        self.data = {0:[0],1:[1,2,3], 2:[3,4,5], 3:[1], 4:[5], 5:[7,8]}
        self.signal = 0
        self.gps_data_recieved = True
        self.gps = GPS()
        self.gps.speed = 1
        self.gps.altitude = 1
        self.gps.course = 1

sock = Sock()

with open('kevin_{}.csv'.format(str(datetime.now().time()).replace('.', '_').replace(':', '_')), mode ='w+') as n:
    with open("gps_{}.csv".format(str(datetime.now().time()).replace('.', '_').replace(':', '_')), mode = 'w+') as g:
        r = Record(sock, n, g)

        while True:
            time.sleep(0.5)
            r.update()
            if sock.gps_data_recieved:
                r.update_gps()
