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
    conn.write(str(rc_write)[1:len(rc_write)-1] + '\n')    # definitly not great performance
    rc_read = conn.readline().decode() # example: "0@500@500@0@500@992@\n"
    print(rc_read)
    return list(map(int,rc_read.split('@')[:-2]))
