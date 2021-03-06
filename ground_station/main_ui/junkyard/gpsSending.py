#to run, 'sudo python' then 'import gamepad' (this file), then 'gamepad.test()'
#to install pygame: apt-get install python-pygame

import pygame, time, serial, csv, motor_func, math, socket, telnetlib


#tn = telnetlib.Telnet("192.168.1.101","51235")
tn = telnetlib.Telnet("100.64.244.34","51235")
#100.64.247.43 

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
	print('str_sent')
	print(str_sent)

	#lon = 1234
	#lat = 6789
        #tn.write(str(readgps(latitude,longitude)).replace("(","").replace(")","").replace(" ",""))
	#tn.write(str((lon,lat)).replace("(","").replace(")","").replace(" ",""))
	tn.write(str_sent)

if __name__ == '__main__':
   test()