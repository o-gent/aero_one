from Utility import limitByRate, mapInput, limit
from filters import LowPassFilter

class Actuator:
    # class for the control surface actuator
    def __init__(self, max, servo_to_hinge, rate):
        self.max = max # max min limit of the FINAL control surface deflection in degrees (e.g. 30 degrees of aileron deflection is +-15 deg)
        self.in_to_servo = 1000/175 # ratio of input channel to the corresponding servo deflection in degrees (in our case 1000 equals ~170-175 deg)
        self.servo_to_hinge = servo_to_hinge # ratio of the servo deflection in degrees to the corresponding control surface deflection, depends on the mechanical arrangement
        self.rate = rate # target deflection speed of the control surface in deg / s
        self.output = 0 # set to zero to initialise
        self.antiAliasing = LowPassFilter(1, 0.05) # anti-wonkifying smoothing of the input signal to the servo

    def step(self, stick_input, sas_input, dt): #stick_input is in 0 to 1000 whereas sas_input is stability augmentation input in degrees corresponding to the surface deflection
        max_1 = max * self.servo_to_hinge * self.in_to_servo
        rate_1 = self.rate * self.servo_to_hinge * self.in_to_servo

        sas_to_in = sas_input * self.servo_to_hinge * self.in_to_servo

        input_1 = self.antiAliasing.step(limit(stick_input + sas_to_in, 1000, 0), dt)

        self.output = limitByRate(input_1, self.output, self.rate, dt)
        return self.output


