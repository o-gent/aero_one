import time
from machine import Timer
from machine import UART
import machine
import pycom
import math
from stability.Utility import limitByRate, mapInput, limit
from stability.filters import LowPassFilter

from sensor_read import roll_pitch, pressure
from datalink import datalink_setup
from rcio import rc_read_write

# enable / disable features - telem, sensor, stability, rc
f = (1,1,1,1)



def main_loop(link):
    # executes while link to ground station is active - breaks upon lost connection
    dt = 0.02
    chrono = Timer.Chrono()
    rc_write = [0,0,0,0,0,0]
    rc_read = [0,0,0,0,0,0]
    loop_time = Timer.Chrono()
    test_servo = 0
    pitch_prev = 0
    pitch_rate = 0
    l = 0.005
    lpf_pitch_rate = LowPassFilter(1,0.5)
    lpf_pitch = LowPassFilter(1,0.1)

    while True:
        loop_time.start()


        if f[1]:
            # SENSOR DATA
            roll, pitch, acc = roll_pitch()
            raw_pressure = pressure()


        if f[2]:
            # STABILITY CALCULATIONS
            """
            try:
                servo_rate = mapInput(rc_read[4], 0, 1000, 90, 300)
                test_servo = limitByRate((rc_read[0] + (acc[2] - 1)*500)

            except Exception as e:
                print(e)
            """
            try:
                pitch = lpf_pitch.step(pitch,l/1000)
                dt = loop_time.read()
                servo_rate = mapInput(rc_read[4], 0, 1000, 90, 300)
                pitch_rate = limit((pitch - pitch_prev)/(l/1000), 30, -30)  #lpf_pitch_rate.step(limit((pitch - pitch_prev)/(l/1000), 300, -300), l/1000)
                pitch_rate = lpf_pitch_rate.step(pitch_rate, l/1000)
                test_servo = limitByRate((rc_read[0] + limit(pitch_rate*30, 300, -300)), test_servo, (1000/180) * servo_rate, l/1000)
                rc_write[0] = limit(test_servo,1000, 0)
                pitch_prev = pitch

            except Exception as e:
                print(e)
            

        if f[3]:
            rc_read = rc_read_write(conn, rc_write)


        if f[0]:
            # TELEMETRY

            link.send(5, [raw_pressure])
            link.send(4, rc_write)
            link.send(3, rc_read)
            link.send(2, [roll, pitch])
            link.send(1, [acc[0], acc[1], acc[2]])
            
            l = loop_time.read_ms()
            # send time taken to do main loop
            link.send(0, [l])
            loop_time.reset()



def backup_loop():
    # to be executed when telemetry to ground station has been lost
    # all ground station only accessible functions to be set to defaults
    
    pycom.rgbled(0x7f0000) # red
    print("connection lost - moved to fallback loop")

# set colour
pycom.heartbeat(False)
pycom.rgbled(0xf200ea)

if f[3]:
    # set up serial connection to arduino using custom pins
    conn = UART(1, baudrate = 57600, pins = ('P4', 'P10'))
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

print("finish")
machine.reset()