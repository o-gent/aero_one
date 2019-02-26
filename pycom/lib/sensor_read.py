"""
Any direct maniupulation of sensor information to produce another measurement should be here
"""

import math

from pysense import Pysense
from LIS2HH12 import LIS2HH12
from LTR329ALS01 import LTR329ALS01
from MPL3115A2 import MPL3115A2,ALTITUDE,PRESSURE
from SI7006A20 import SI7006A20

py = Pysense()
attitude = LIS2HH12(py)
p = MPL3115A2(py,mode=PRESSURE)
temp = SI7006A20(py)

ground_pressure = p.pressure()
ground_temperature = temp.temperature()
print(ground_pressure)
print(ground_temperature)

def roll_pitch():
    x,y,z = attitude.acceleration()
    roll = math.atan2(-x, z) * (180 / math.pi)
    pitch = -math.atan2(y, (math.sqrt(x*x + z*z))) * (180 / math.pi)
    return roll, pitch

def pressure():
    return p.pressure()
"""
def pressure():
    return (((ground_pressure/p.pressure())**(1/5.258) - 1) * (ground_temperature + 273.15))/0.0065
"""