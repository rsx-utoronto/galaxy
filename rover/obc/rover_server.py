#!/usr/bin/python

import socket, time

s = socket.socket()
host = "100.64.246.12"
port = 8000
s.bind((host, port))

s.listen(5)

while True:
   c, addr = s.accept()
   print 'Got connection from', addr
   c.send('To infinity.')

   while True:
      c.send("hi")
      time.sleep(1)

c.close()
