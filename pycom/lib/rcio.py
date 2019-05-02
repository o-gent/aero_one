""" 
Any RC communication with servos & receiver. 
"""

from machine import Pin
import machine
import micropython
import time

def rc_read_write(conn, rc_write):
    """
    get/send new RC data from UART
    """

    try:
        i = str(rc_write)[1:-1].replace(" ", "") + "\n"
        conn.write(i.encode())    # definitly not great performance
        rc_read = conn.readline().decode() # example: "0@500@500@0@500@992@\n"
        return list(map(int,rc_read.split('@')[:-1]))

    except Exception as e:
        print("exception in rc_read_write: {}".format(e))
        return [0,0,0,0,0,0]



if __name__ =="__main__":
    conn = UART(1, baudrate = 57600, pins = ('P4', 'P10'))
    # initialise variables for clarity
    rc_write = [1000,0,0,0,0,0]   #6 channels
    rc_read = [0,0,0,0,0,0]     # ""

    conn.write("\n")
    print(conn.readline())

    time.sleep(3)

    while True:
        print(rc_read_write(conn, rc_write))
