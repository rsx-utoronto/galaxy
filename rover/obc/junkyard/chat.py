# A simple network chat program between to Raspberry Pi's

import network
import sys

def heard(phrase):
  print phrase

print "Galaxy Communication 1.0"

network.wait(whenHearCall=heard)
 
while True:

  if network.isConnected():
    phrase = raw_input()
    network.say(phrase)
  
  else:
    network.wait(whenHearCall=heard)
