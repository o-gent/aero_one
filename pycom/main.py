import time
from machine import Timer
from machine import UART
import pycom
import time

from sensor_read import roll_pitch, pressure
from datalink import datalink_setup
from rcio import rc_read_write

# enable / disable features - telem, sensor, stability, rc
f = (1,1,0,1)
dt = 0.02
prev_time = 0



def main_loop(link):
    # executes while link to ground station is active - breaks upon lost connection
    while True:
        if f[1]:
            # SENSOR DATA
            roll, pitch, acc = roll_pitch()


        if f[2]:
            # STABILITY CALCULATIONS
            
            rc_write = [0,0,0,0,0,0]
            dt = (time.ticks_ms() / 1000) - prev_time # calculate time step to be used in calculations (e.g. integration, differentiation)
            prev_time = time.ticks_ms() / 1000 # set the previous time value for the next iteration to be equal to the current time value in this iteration
            test_servo = 180 * sin(2*3.1416*(time.ticks_ms()/1000))
            rc_write[2] = test_servo

        if f[3]:
            # RC IO
            try:
                rc_read = rc_read_write(conn, rc_write)
            except:
                rc_read = [0,0,0,0,0,0]
                pass


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
