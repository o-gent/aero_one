import time
from machine import Timer
from machine import UART
import machine
import pycom
import math
import uasyncio as asyncio
import as_GPS

from stability.Utility import limitByRate, mapInput, limit
from stability.filters import LowPassFilter
from stability.filters import WashoutFilter

from sensor_read import roll_pitch, pressure
from datalink import datalink_setup
from rcio import rc_read_write
from stability.actuator import Actuator
from stability.filters import Differentiator


# enable / disable features - telem, sensor, stability, rc
f = (1,1,1,1)
GPS = False
sd_card = True


# setup datalogging to SD card..
from machine import SD
import os

if sd_card:
    sd = SD()
    os.mount(sd, '/sd')

    # check the content
    print(os.listdir('/sd'))
    
    file_number = 0
    try:
        # check for files that exist until a free index is found
        for _ in range(100):
            if os.stat('/sd/gps{}.txt'.format(i)):
                file_number += 1
    except:
        # now open free file
        gps_file = open('/sd/gps{}.txt'.format(file_number), 'w+')
        normal_file = open('/sd/kevin{}.txt'.format(file_number), 'w+')


# define global variables
roll, pitch, acc = 0,0,[1,2,3]
rc_read = [0,0,0,0,0,0]
rc_write = [0,0,0,0,0,0]
raw_pressure = 0
loop_time = 0
l = 20
dt = 0.02


# stability classes
lpf_pitch_rate = LowPassFilter(1, 0.1)
lpf_pitch = LowPassFilter(1, 0.1)

lpf_roll_rate = LowPassFilter(1, 0.1)
lpf_roll = LowPassFilter(1, 0.1)

#LeftAileron = Actuator(40, 4, 40)  # channel 1
Aileron = Actuator(40, 4, 90)  # channel 0
Elevator = Actuator(50, 3.5, 90)  # channel 1
Rudder = Actuator(50, 3.5, 90)  # channel 3

PitchRate = Differentiator(1)
RollRate = Differentiator(1)

PitchDamper = WashoutFilter(2)
RollDamper = WashoutFilter(1)


async def main_loop(link):
    global roll, pitch, acc, rc_read, rc_write, raw_pressure, loop_time, l
    loop_time = Timer.Chrono()
    
    while True:
        loop_time.start()

        if f[1]:
            # SENSOR DATA
            roll, pitch, acc = roll_pitch()
            raw_pressure = pressure()

        if f[2]:
            # STABILITY CALCULATIONS
            dt = l / 1000
            """
            try:
                servo_rate = mapInput(rc_read[4], 0, 1000, 90, 300)
                test_servo = limitByRate((rc_read[0] + (acc[2] - 1)*500)

            except Exception as e:
                print(e)
            """
            try:

                if abs(roll) > 60 or abs(pitch) >60:
                    pitch_rate = 0
                    roll_rate = 0
                else:
                    pitch_rate = lpf_pitch_rate.step(PitchRate.step(lpf_pitch.step(pitch, dt), dt), dt) / (math.cos(roll / 57.2958))
                    roll_rate = lpf_roll_rate.step(RollRate.step(lpf_roll.step(roll, dt), dt), dt)

                # pitch = lpf_pitch.step(pitch,dt)
                # dt = loop_time.read()
                rc_write[1] = Elevator.step(rc_read[1], 0.1 * PitchDamper.step(pitch_rate, dt), dt)
                #rc_write[1] = LeftAileron.step(rc_read[1], 0.1 * RollDamper.step(roll_rate, dt), dt)
                rc_write[0] = Aileron.step(rc_read[0], 0.1 * PitchDamper.step(roll_rate, dt), dt)
                rc_write[3] = Rudder.step(rc_read[3], 0, dt)

                # servo_rate = mapInput(rc_read[4], 0, 1000, 90, 300)
                # pitch_rate = limit((pitch - pitch_prev)/(dt), 30, -30)  #lpf_pitch_rate.step(limit((pitch - pitch_prev)/(l/1000), 300, -300), l/1000)
                # pitch_rate = lpf_pitch_rate.step(pitch_rate, dt)
                # test_servo = limitByRate((rc_read[0] + limit(pitch_rate*30, 300, -300)), test_servo, (1000/180) * servo_rate, dt)
                # rc_write[0] = limit(test_servo,1000, 0)
                # pitch_prev = pitch


            except Exception as e:
                print(e)

        if f[3]:
            rc_read = rc_read_write(conn, rc_write)
        
        l = loop_time.read_ms()
        loop_time.reset()

        # allow other tasks
        await asyncio.sleep(0)


async def telemetry(link):
    global roll, pitch, acc, rc_read, rc_write, raw_pressure, loop_time, l
    global normal_file

    try:
        while True:
            
            link.send(5, [raw_pressure])
            await asyncio.sleep(0)
            
            link.send(4, rc_write)
            await asyncio.sleep(0)
            
            link.send(3, rc_read)
            await asyncio.sleep(0)
            
            link.send(2, [int(roll), int(pitch)])
            await asyncio.sleep(0)
            
            link.send(1, [acc[0], acc[1], acc[2]])
            await asyncio.sleep(0)

            link.send(0, [l])
            await asyncio.sleep(0)
    except:
        #print("FAILED")
        #machine.reset()
        # lost connection - just deal with it and continue writing sd data
        pass


async def gps_basic(link):
    global gps_file
    
    # runs each second
    while True:
        try:
            read = gps_uart.read()
            
            # send raw data over telemetry
            link.sock.send(read)
            
            # save data to file
            gps_file.write(read)
            
            
        except Exception as e:
            print("gps read failed: {}".format(e))
        await asyncio.sleep(1)


async def gps_data():
    print('waiting for GPS data')
    await gps.data_received(position=True, altitude=True)
    
    for _ in range(100):
        print(gps.latitude(), gps.longitude(), gps.altitude)
        await asyncio.sleep(2)


def backup_loop():
    # to be executed when telemetry to ground station has been lost
    # all ground station only accessible functions to be set to defaults
    
    pycom.rgbled(0x7f0000) # red
    print("connection lost - moved to fallback loop")

# set colour
pycom.heartbeat(False)
pycom.rgbled(0xf200ea)


try:
    gps_uart = UART(2, baudrate = 9600, pins = ('P9', 'P11'))
except:
    print("no gps")

if GPS:
    #set up GPS
    sreader = asyncio.StreamReader(gps_uart)  # Create a StreamReader
    gps = as_GPS.AS_GPS(sreader)  # Instantiate GPS


if f[3]:
    # set up serial connection to arduino using custom pins
    conn = UART(1, baudrate = 57600, pins = ('P4', 'P10'))
    # initialise variables for clarity
    rc_write = [0,0,0,0,0,0]   #6 channels
    rc_read = [0,0,0,0,0,0]     # ""


if f[0]:
    # set up link to ground station
    with datalink_setup() as link:
        link.file = normal_file

        pycom.heartbeat(False)
        pycom.rgbled(0x007f00) # green

        # EVENT SETUP :)  
        loop = asyncio.get_event_loop()
        loop.create_task(main_loop(link))
        loop.create_task(telemetry(link))
        if GPS:
            loop.create_task(gps_data())
        loop.create_task(gps_basic(link))
        loop.run_forever()


    # if connection fails
    backup_loop()

else:
    main_loop(None)

print("finish")
machine.reset()
