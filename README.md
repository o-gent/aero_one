# aero_one
UAV control for 2nd year project.


Consists of an Arduino to read RC signal and control servos as well as serving as a failsafe if the ESP32 fails. 


ESP32 - Specifically a Pycom WiPy 3.0 with a pysense shield runs micropython and sends telemetry through a TCP socket to a ground station as well as being able to Read/Send servo commands to the arduino over UART.
The Main purpose of the Pycom is to run control code such as attitude control for the drone. 

Running on release 1.18.x, performance drops by 2x on release 1.20
