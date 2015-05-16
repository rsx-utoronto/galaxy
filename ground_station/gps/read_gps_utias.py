#working

import serial
import socket
import time
# Import a library of functions called 'pygame'
import pygame
from math import pi
 
# Initialize the game engine
pygame.init()
 
# Define the colors we will use in RGB format
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)
GREEN = (  0, 255,   0)
RED =   (255,   0,   0)
 
# Set the height and width of the screen
size = [1090, 440]
screen = pygame.display.set_mode(size)
oldx = 0
oldy = 0
pygame.display.set_caption("Example code for the draw module")

myfont = pygame.font.SysFont("monospace", 15)
 
#Loop until the user clicks the close button.
done = False
clock = pygame.time.Clock()
#Reference = '4346.9244', '07927.9656'
reference_y1 = 4346.9244
reference_x1 = 7927.9656
reference_y2 = 4346.9266
reference_x2 = 7927.9259
#4346.9212 7928.0415
reference_y3 = 4346.9212
reference_x3 = 7928.0415
#4346.9695 7928.0534
reference_y4 = 4346.9695
reference_x4 = 7928.0534
#4346.9705 7927.8968
reference_y5 = 4346.9705
reference_x5 = 7927.8968

ser = serial.Serial('/dev/ttyUSB0', 4800, timeout=1)
latitude = ''
longitude = ''

red_rect = pygame.image.load('utias.jpg')
w,h = red_rect.get_size()
x_scale = 0.8
y_scale = 0.8
red_rect = pygame.transform.scale(red_rect, (int(w*x_scale),int(h*y_scale)))

# 4378.2122, 7946.6208
# 4378.2078, 7946.7341
# 4378.2089, 7946.5451
# 4378.2838, 76.7566

"""
ast_1_lon = raw_input("Input Astronaut 1's longitude: ")
ast_1_lat = raw_input("Input Astronaut 1's latitude: ")

ast_2_lon = raw_input("Input Astronaut 2's longitude: ")
ast_2_lat = raw_input("Input Astronaut 2's latitude: ")

ast_3_lon = raw_input("Input Astronaut 3's longitude: ")
ast_3_lat = raw_input("Input Astronaut 3's latitude: ")

ast_4_lon = raw_input("Input Astronaut 4's longitude: ")
ast_4_lat = raw_input("Input Astronaut 4's latitude: ")

ast_1_x = 695 + (float(ast_1_lon) - reference_x)*(-10500/2)
ast_1_y = 400 + (float(ast_1_lat) - reference_y)*(-15600/2)

ast_2_x = 695 + (float(ast_2_lon) - reference_x)*(-10500/2)
ast_2_y = 400 + (float(ast_2_lat) - reference_y)*(-15600/2)

ast_3_x = 695 + (float(ast_3_lon) - reference_x)*(-10500/2)
ast_3_y = 400 + (float(ast_3_lat) - reference_y)*(-15600/2)

ast_4_x = 695 + (float(ast_4_lon) - reference_x)*(-10500/2)
ast_4_y = 400 + (float(ast_4_lat) - reference_y)*(-15600/2)
"""
def readgps(latitude,longitude):
    #Read the GPG LINE using the NMEA standard
    while True:
        line = ser.readline()
        if "GPGGA" in line:
            latitude = line[18:27] #Yes it is positional info for lattitude
            longitude = line[30:40] #do it again
            return(latitude,longitude)
    print "Finished"

while(not done):
    """
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        print 'hi'
        x-=v
        if x==-1:
            x=0
    if keys[pygame.K_d]:
        x+=v
        if x==1501:
            x=1500
    if keys[pygame.K_w]:
        y-=v
        if y==-1:
            y=0
    if keys[pygame.K_s]:
        y+=v
        if y==601:
            y=600
    """
#Reference = '4346.9244', '07927.9656'
    #pos = str(x)+" "+str(600 - y)
    #label = myfont.render(pos, 1, (0,0,0))
    
    #print(readgps(latitude, longitude)[0], 'N ', readgps(latitude, longitude)[1], 'W')
    #print('\n')
    #print(readgps(latitude,longitude))
    #print('\n')
    
    lon = readgps(latitude,longitude)[1]
    lat = readgps(latitude,longitude)[0]
    
    #x1 = 695 + (float(lon) - reference_x1)*(-10500/2)
    #y1 = 400 + (float(lat) - reference_y1)*(-15600/2)
    x2 = 930 + (float(lon) - reference_x2)*(-10500/2)
    y2 = 365 + (float(lat) - reference_y2)*(-15600/2)
    x3 = 290 + (float(lon) - reference_x3)*(-10500/2)
    y3 = 375 + (float(lat) - reference_y3)*(-15600/2)
    x4 = 220 + (float(lon) - reference_x4)*(-10500/2)
    y4 = 45 + (float(lat) - reference_y4)*(-15600/2)
    x5 = 1075 + (float(lon) - reference_x5)*(-10500/2)
    y5 = 20 + (float(lat) - reference_y5)*(-15600/2)

    x = (x2+x3+x4+x5)/4
    y = (y2+y3+y4+y5)/4

    #print(pos)
    # This limits the while loop to a max of 10 times per second.
    # Leave this out and we will use all CPU we can.
    #clock.tick(10)
    
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done=True # Flag that we are done so we exit this loop
    
    screen.blit(red_rect,(0,0))
    pygame.draw.circle(screen, RED, [int(x), int(y)], 10)
    #print("diffx: ")
    #print((float(ast_1_lon) - reference_x))
    #print("\ndiffy: ")
    #print((float(ast_1_lat) - reference_y))
    """
    print("\n astx: ")
    print(ast_1_x)
    print("\n asty: ")
    print(ast_1_y)
    print("\n")
    pygame.draw.circle(screen, BLUE, [int(ast_1_x), int(ast_1_y)], 10)
    pygame.draw.circle(screen, GREEN, [int(ast_2_x), int(ast_2_y)], 10)
    pygame.draw.circle(screen, GREEN, [int(ast_3_x), int(ast_3_y)], 10)
    pygame.draw.circle(screen, GREEN, [int(ast_4_x), int(ast_4_y)], 10)
    """
    #screen.blit(label,(x-30,y-10))

    #pygame.draw.line(screen, GREEN, [oldx, oldy], [int(x),int(y)], 5)
    pygame.display.flip()
# Be IDLE friendly
pygame.quit()
