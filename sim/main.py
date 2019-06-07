import math
import matplotlib.pyplot as plt
from filters import *
from Utility import *
from Actuator import *

# A small program for 2D simulation of the aircraft around its pitch axis.

g = 9.80665
rad = 57.2958 # converting from radians to degrees

rho = 1.225 # assume sea level

dt = 0.001 # time step for euler integration

# SETTING UP INITIAL CONDITIONS:
t = 0
alpha = 10 / rad # initial angle of attack to simulate disturbance at t = 0

q = 0 # non-dimensional pitch rate
omega = 0 # pitch rate
pitch = 10 / rad # pitch angle, 10 degrees due to the initial angle of attack in steady level flight
velocity = 13.333 # at cruise
u = velocity*math.cos(alpha) # horizontal velocity component for the body reference frame (X-axis)
w = -velocity*math.sin(alpha) # vertical velocity component for the for the body reference frame (Z-axis), chosen to be positive UPWARDS

# Elevator = Actuator(50, 3.5, 90)
PitchDamper = WashoutFilter(2) # setting the pitch damper as a washout filter with the time constant of 2
sas_e = 0 # stability augmentation input for elevator
inp = 0 # pilot's input (not used, since always zero)
# -----------------------------

AccDot = Differentiator(1) # getting the rate of change of acceleration (was only tested for the alternative damping system< NOT used further)

# Defining stability derivatives
_CLa = 0.076 * rad # lift curve slope
_CL0 = 0.4 # lift coefficient at zero angle of attack
_Cma = -0.94 # pitching moment derivative with respect to angle of attack
_Cmq = -10.8 # ... with respect to non-dimensional pitch rate
_Cm0 = 0.046 # pitching moment coefficient at zero angle of attack
_Iyy = 0.18 # moment of inertia about the aircraft pitching axis

_Sref = 0.45
c = 0.3
m = 3

time_array = [] # list of all the discrete time values
alpha_array = [] # ... angle of attack values
array = [] # ... of any other alternative measurement

#time_array.append(t)
#alpha_array.append(alpha)
#az_array.append(0)

# FIRST RUN WITH STABILITY AUGMENTATION ON

for i in range(3000):

    t += dt
    q_ = 0.5 * rho * velocity**2
    L = (_CLa * alpha + _CL0) * q_ * _Sref
    az = L / m - g
    nz = L / (m*g)
    u += omega * w * dt
    w += (az - omega*u)*dt
    #inp = 5*math.sin(2*math.pi*2*t)
    Mz = (_Cm0 + _Cma * alpha + _Cmq * q + (sas_e + inp) * 0.02) * _Sref * c * q_
    omegaDot = Mz / _Iyy
    omega += omegaDot * dt
    pitch += omega * dt
    q = omega*c / (2*velocity)
    alpha = math.atan(-w / u)

    #sas_e = limit(-0.05*PitchDamper.step(AccDot.step(az, dt), dt), 10, -10)
    sas_e = limit(-0.3 * PitchDamper.step(omega*rad, dt), 10, -10)

    time_array.append(t)
    alpha_array.append(alpha)
    array.append(sas_e)


#print(alpha_array)
plt.plot(time_array, [x*rad for x in alpha_array], label = 'Damped')
#plt.plot(time_array, array)

# -------------------------------------

# Clear all the arrays for the next run
time_array.clear()
alpha_array.clear()
array.clear()

# Initial conditions again
t = 0
alpha = 10 / rad

q = 0
omega = 0
pitch = 10 / rad
u = velocity*math.cos(alpha)
w = -velocity*math.sin(alpha)

sas_e = 0
inp = 0

# SECOND RUN WITHOUT STABILITY AUGMENTATION

for i in range(3000):

    t += dt
    q_ = 0.5 * rho * velocity**2
    L = (_CLa * alpha + _CL0) * q_ * _Sref
    az = L / m - g
    nz = L / (m*g)
    u += omega * w * dt
    w += (az - omega*u)*dt
    #inp = 5*math.sin(2*math.pi*2*t)
    Mz = (_Cm0 + _Cma * alpha + _Cmq * q + (sas_e + inp) * 0.02) * _Sref * c * q_
    omegaDot = Mz / _Iyy
    omega += omegaDot * dt
    pitch += omega * dt
    q = omega*c / (2*velocity)
    alpha = math.atan(-w / u)

    #sas_e = limit(-0.05*PitchDamper.step(AccDot.step(az, dt), dt), 10, -10)
    #sas_e = limit(-0.3 * PitchDamper.step(omega*rad, dt), 10, -10)

    time_array.append(t)
    alpha_array.append(alpha)
    array.append(sas_e)

plt.plot(time_array, [x*rad for x in alpha_array], label = 'Undamped')

# Plotting graphs:

plt.xlabel('time (s)')
plt.ylabel('angle of attack (deg)')

plt.legend()
plt.minorticks_on()
plt.grid()
plt.grid(which = 'minor', linestyle = ':')
plt.show()
