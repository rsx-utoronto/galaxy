#!/usr/bin/python

# Apr. 30/2015 This code currently connects to the Pi on the UofT network, important that both client and host are on UofT, and that the IP address of the Pi is correct. I have configured it such that the IP address should remain static on the Pi WRT UofT network.

import socket

s = socket.socket()
host = "192.168.1.114"
port = 8000

s.connect((host, port))
print s.recv(1024)
s.close  
