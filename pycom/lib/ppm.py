import machine
import micropython


class Rppm():
    """
    Read a combined PPM signal from a R/C radio.
    @note, this uses timer 2.
    """
    timer = None
    def __init__(self, pin, numChannels = 8):
        """

        """
        self.pin = pin
        self.interrupt = self.pin.callback(machine.Pin.IRQ_FALLING | machine.Pin.IRQ_RISING, self.callback)
        self.timer = machine.Timer.Chrono()

        self.start = 0
        self.width = 0
        self.channel = 0
        self.numChannels = numChannels
        self.ch = [0]*numChannels
        self.sync_width = 0

    def callback(self, arg):
        self.width = (self.timer.read_us() - self.timer.start)
        self.timer.reset()
        self.start = self.timer.start()

        if self.width > 4000:
            self.channel = 0
            self.sync_width = self.width
            return
        if self.channel == self.numChannels:
            return
        self.ch[self.channel] = self.width
        self.channel += 1


class Wppm():
    """
    Write a PPM signal to a wire
    """
    def __init__(self):
        pass



if __name__ == "__main__":
    # requires a signal (CPPM from a radio) on P10.
    micropython.alloc_emergency_exception_buf(100)

    ppm_out = Rppm(machine.Pin('P10', mode=Pin.IN, pull=Pin.PULL_UP), 8)

    while True:
        print(ppm_out.ch, ppm_out.sync_width)