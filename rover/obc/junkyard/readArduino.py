from serial import *

ser = Serial("/dev/ttyUSB0", 9600, timeout = 0.01, writeTimeout = 0.01)

while(1):
	str = ser.readline()
	print(str)
