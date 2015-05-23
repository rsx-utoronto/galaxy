#to run, 'sudo python' then 'import gamepad' (this file), then 'gamepad.test()'
#to install pygame: apt-get install python-pygame

import time, serial, socket, telnetlib


#tn = telnetlib.Telnet("192.168.1.101","51235")
tn = telnetlib.Telnet("100.64.248.153","51235")
#tn = telnetlib.Telnet("100.64.249.58","51236")
#100.64.247.43 


from serial import *

ser = Serial("/dev/ttyUSB0", 9600, timeout = 0.01, writeTimeout = 0.01)

while(1):
	str_sensor = ser.readline()
	tn.write(str_sensor)
	print(str_sensor)
