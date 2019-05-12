import time
from machine import Timer
from machine import UART
import machine
import pycom
import math
import uasyncio as asyncio
import as_GPS

from sensor_read import roll_pitch, pressure
from datalink import datalink_setup
from rcio import rc_read_write

# enable / disable features - telem, sensor, stability, rc
f = (1,1,1,1)
GPS = False


# define global variables
roll, pitch, acc = 0,0,[1,2,3]
rc_read = [0,0,0,0,0,0]
rc_write = [0,0,0,0,0,0]
raw_pressure = 0
loop_time = 0
l = 0


async def main_loop(link):
    # executes while link to ground station is active - breaks upon lost connection
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
            pass

        if f[3]:
            rc_read = rc_read_write(conn, rc_write)
        
        l = loop_time.read_ms()
        loop_time.reset()

        # allow other tasks
        await asyncio.sleep(0)


async def telemetry(link):
    global roll, pitch, acc, rc_read, rc_write, raw_pressure, loop_time, l

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
        print("FAILED")
        machine.reset()


async def gps_basic(link):
    # runs each second
    while True:
        try:
            read = gps_uart.read()
            link.sock.send(read)
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