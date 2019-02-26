import time
from machine import Timer
import pycom
import time

from sensor_read import roll_pitch, pressure
from datalink import datalink_setup
from ppm import Wppm 


def main_loop(link):
    # executes while link to ground station is active - breaks upon lost connection
    
    while True:
        roll, pitch= roll_pitch()
        link.put(1, [int(roll), int(pitch)])
        link.refresh()
        time.sleep(0.005)


def backup_loop():
    # to be executed when telemetry to ground station has been lost
    # all ground station only accessible functions to be set to defaults
    
    pycom.rgbled(0x7f0000) # red
    print("connection lost - moved to fallback loop")


# set up link to ground station
with datalink_setup() as link:
    pycom.heartbeat(False)
    pycom.rgbled(0x007f00) # green
    main_loop(link)


# if connection fails
backup_loop()