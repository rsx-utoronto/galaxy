#to run, 'sudo python' then 'import gamepad' (this file), then 'gamepad.test()'
#to install pygame: apt-get install python-pygame

import pygame, time, serial, csv, motor_func, math, socket, telnetlib

pygame.init()
j = pygame.joystick.Joystick(0)
j.init()

tn = telnetlib.Telnet("192.168.1.114","51234")

output_delay = 0.25

def get():
    out = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    it = 0
    pygame.event.pump()
    
    #Read input from the two joysticks
    for i in range(0, j.get_numaxes()):
        out[it] = round(j.get_axis(i), 2)
        it+=1
        
    #Read input from buttons
    for i in range(0, j.get_numbuttons()):
        out[it] = j.get_button(i)
        it+=1
    return out

    for i in range(0, j.get_numhats()):
        out[it] = j.get_hat(i)
        it+=1
    return out

def test():
    while True:
        time.sleep(float(output_delay))
        joystick_info = get()
        tn.write(str(joystick_info).replace(" ","").replace("[","").replace("]",""))
        print str(joystick_info)

if __name__ == '__main__':
    test()




