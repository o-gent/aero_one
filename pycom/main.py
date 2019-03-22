import time
from machine import Timer
from machine import UART
import pycom
import time

from sensor_read import roll_pitch, pressure
from datalink import datalink_setup
from rcio import Rppm, rc_read_write

# enable / disable features - telem, sensor, stability, rc
f = (1,1,0,1)


def main_loop(link):
    # executes while link to ground station is active - breaks upon lost connection
    while True:
        
        if f[1]:
            # SENSOR DATA
            roll, pitch= roll_pitch()


        if f[2]:
            # STABILITY CALCULATIONS
            pass


        if f[3]:
            # RC IO
            rc_read = rc_read_write(conn, rc_write)


        if f[0]:
            # TELEMETRY
            link.put(3, rc_read)
            link.put(2, [int(roll), int(pitch)])
            link.refresh()



def backup_loop():
    # to be executed when telemetry to ground station has been lost
    # all ground station only accessible functions to be set to defaults
    
    pycom.rgbled(0x7f0000) # red
    print("connection lost - moved to fallback loop")



if f[3]:
    # set up serial connection to arduino using custom pins
    conn = UART(1, baudrate = 115200, pins = ('P4', 'P10'))
    # initialise variables for clarity
    rc_write = [0,0,0,0,0,0]   #6 channels
    rc_read = [0,0,0,0,0,0]     # ""


if f[0]:
    # set up link to ground station
    with datalink_setup() as link:
        pycom.heartbeat(False)
        pycom.rgbled(0x007f00) # green
        main_loop(link)


    # if connection fails
    backup_loop()

else:
    main_loop(None)
