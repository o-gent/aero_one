class Differentiator:
    def __init__(self, amp):
        self.amp = amp
        self.output = 0
        self.in_prev = 0

    def setReference(self, a):
        self.in_prev = a

    def clearOutput(self):
        self.output = 0

    def step(self, input_, dt):
        self.output = self.amp*((input_ - self.in_prev) / dt)
        self.in_prev = input_
        return self.output

class Integrator:
    def __init__(self, amp):
        self.amp = amp
        self.output = 0

    def setReference(self, a):
        self.output = a

    def step(self, input_, dt):
        self.output = self.amp*(self.output + input_*dt)
        return self.output

class LowPassFilter:
    def __init__(self, amp, tau):
        self.amp = amp
        self.tau = tau
        self.output = 0
        self.out_prev = 0
    
    def set_reference(self, var_a):
        self.out_prev = var_a
    
    def step(self, input_, dt):
        a = dt/(self.tau + dt)
        self.output = (1-a) * self.out_prev + a * input_ * self.amp
        self.out_prev = self.output
        return self.output

class WashoutFilter:
    def __init__(self, tau):
        self.tau = tau
        self.output = 0
        self.out_prev = 0
        self.in_prev = 0

    def step(self, input_, dt):
        a = self.tau / (self.tau + dt)
        self.output = a*self.out_prev + a*(input_ - self.in_prev)
        self.out_prev = self.output
        self.in_prev = input_
        return self.output
