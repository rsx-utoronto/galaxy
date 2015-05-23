import time, serial, math, socket, telnetlib

#tn = telnetlib.Telnet("192.168.1.101","51235")
tn = telnetlib.Telnet("100.64.244.34","51235")
#tn = telnetlib.Telnet("100.64.249.58","51236")
#100.64.247.43 
#

from serial import *

ser = Serial("/dev/ttyUSB0", 9600, timeout = 0.01, writeTimeout = 0.01)

import serial
import socket
import socket
import time

ser = serial.Serial('/dev/ttyUSB1', 4800, timeout=1)
latitude = ''
longitude = ''

def readgps(latitude,longitude):
    #Read the GPG LINE using the NMEA standard
    line = ser.readline()
    if "GPGGA" in line:
        latitude = line[18:27] #Yes it is positional info for lattitude
        longitude = line[30:40] #do it again
    return(latitude,longitude)

def test():
    while True:
	data = readgps(latitude,longitude)
	if data[0] == "":
		continue

	print('data')
	print(data)

	#time.sleep(1)
        lon = data[1] #Real lines
        lat = data[0]
	str_sent = lon + ',' + lat

	str_sensor = str_sent + ',' + ser.readline()
	tn.write(str_sensor)
	print(str_sensor)
	tn.write(str_sent)

if __name__ == '__main__':
   test()
