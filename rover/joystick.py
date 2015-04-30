#to run, 'sudo python' then 'import gamepad' (this file), then 'gamepad.test()'
#to install pygame: apt-get install python-pygame

import pygame, time, serial, csv, motor_func, math

pygame.init()
j = pygame.joystick.Joystick(0)
j.init()

# This is for the output write (change it accordingly, i.e: /dev/ttyUSB0):
#output_ser_path = raw_input("Please enter your serial port number: ")

output_delay = 0.1
"""
for i in range(10):
    try:
        output_ser_path = str(i)
    except Exception:
        pass
print(output_ser_path)




ser = serial.Serial("Port_#0002.Hub_#0004")
ser.baudrate = 9600
ser.write('Initialized Joystick : %s' % j.get_name())
print('Initialized Joystick : %s' % j.get_name())

ser.timeout = 1
"""

def get():
    out = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    it = 0 #iterator
    pygame.event.pump()
    
    #Read input from the two joysticks
    for i in range(0, j.get_numaxes()):
        out[it] = round(j.get_axis(i), 2)
        it+=1
        
    #Read input from buttons
    for i in range(0, j.get_numbuttons()):
        #print (j.get_numbuttons())
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
		print (joystick_info)

		#ser.write(str(joystick_info))
		#def motor_move(motor, speed_fb,speed_lr,ser)
#		motor_func.motor_move(1,joystick_info[1]*0.5*(joystick_info[3] + 1),joystick_info[0]*0.5*(joystick_info[3] + 1),joystick_info[2]*0.5*(joystick_info[3] + 1),ser)
#		motor_func.motor_move(2,joystick_info[1]*0.5*(joystick_info[3] + 1),joystick_info[0]*0.5*(joystick_info[3] + 1),joystick_info[2]*0.5*(joystick_info[3] + 1),ser)

if __name__ == '__main__':
    test()




