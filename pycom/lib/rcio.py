""" 
Any RC communication with servos & receiver. 
"""

from machine import Pin
import machine
import micropython
import time

def rc_read_write(conn, rc_write):
    """
    get/send new RC data from UART - no this is not nice.
    """
    conn.write(str(rc_write)[1:len(rc_write)-1] + '\n')    # definitly not great performance
    rc_read = str(conn.readline()) # example: "b'0@500@500@0@500@992@\n'"
    print(rc_read)
    return list(map(int,rc_read.split('@')[1:-1]))