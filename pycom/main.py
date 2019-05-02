import time
from machine import Timer
from machine import UART
import pycom
import math

from sensor_read import roll_pitch, pressure
from datalink import datalink_setup
from rcio import rc_read_write

# enable / disable features - telem, sensor, stability, rc
f = (1,1,1,1)



def main_loop(link):
    # executes while link to ground station is active - breaks upon lost connection
    time_running = 0
    dt = 0.02
    chrono = Timer.Chrono()
    rc_write = [0,0,0,0,0,0]

    while True:
        if f[1]:
            # SENSOR DATA
            roll, pitch, acc = roll_pitch()


        if f[2]:
            # STABILITY CALCULATIONS
            chrono.stop()

            dt = chrono.read()

            chrono.start()

            time_running+=dt
            test_servo = abs(int(1000 * math.sin(2*3.1416*time_running * 0.0001)))
            rc_write[0] = test_servo


        

        if f[3]:
            rc_read = rc_read_write(conn, rc_write)


        if f[0]:
            # TELEMETRY
            link.send(3, rc_read)
            link.send(2, [int(roll), int(pitch)])
            link.send(1, [acc[0], acc[1], acc[2]])



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
