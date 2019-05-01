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
    rc_read = str(conn.readline())[2:] # example: "b'0@500@500@0@500@992@\n'"
    return list(map(int,rc_read.split('@')[1:-1]))



class Rppm():
    """
    Read a combined PPM signal from a R/C radio.
    @note, this uses timer 2.
    """
    timer = None
    def __init__(self, pin, numChannels):
        """

        """
        self.pin = pin
        self.pin.callback(Pin.IRQ_RISING | Pin.IRQ_FALLING, self.callback)
        #self.pin.callback(Pin.IRQ_RISING, self.callback)

        self.timer = machine.Timer.Chrono()
        self.start = 0
        self.width = 0
        self.channel = 0
        self.numChannels = numChannels
        
        self.ch = []
        self.sync_width = 0
        self.capture = 0
        self.timer.start()
        self.before = 0
        self.state = 0

    def callback(self, arg):
        if self.state != pin():
            self.now = self.timer.read_us()
            print(pin(), self.now - self.before)
            self.before = self.now
        
        self.state = pin()

        """
        if self.width > 4000.0:
            self.channel = 0
            self.sync_width = self.width
            
            self.timer.reset()
            return
        
        #if self.channel == self.numChannels:
            #return
        
        self.ch.append(self.width)
        """


if __name__ == "__main__":
    # requires a signal (CPPM from a radio) on P10.
    micropython.alloc_emergency_exception_buf(100)

    pin = Pin('P10', mode=Pin.IN, pull=Pin.PULL_DOWN)
    ppm_out = Rppm(pin, 10)

    #while True:
        #print(ppm_out.ch, ppm_out.sync_width)