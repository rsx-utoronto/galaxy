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
size = [1500, 600]
screen = pygame.display.set_mode(size)
oldx = 0
oldy = 0
pygame.display.set_caption("Example code for the draw module")

myfont = pygame.font.SysFont("monospace", 15)
 
#Loop until the user clicks the close button.
done = False
clock = pygame.time.Clock()


#ser = serial.Serial('/dev/ttyUSB0', 4800, timeout=1)
latitude = ''
longitude = ''

red_rect = pygame.image.load('utias.jpg')
w,h = red_rect.get_size()
x_scale = 0.8
y_scale = 0.8
red_rect = pygame.transform.scale(red_rect, (int(w*x_scale),int(h*y_scale)))
arrow = pygame.image.load('green-arrow.png')
arrow = pygame.transform.scale(arrow, (20,20))
x = 100
y = 100
v = 10
arrowangle = 0
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
"""
"""
def rot_center(image, angle):
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image
"""
def rotatefunc(angle, gameObject, rotations={}):
    #r = rotations.get(gameObject,0) + angle
    r = angle
    rotations[gameObject] = r
    return pygame.transform.rotate(gameObject, r)

while(not done):
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
    if keys[pygame.K_q]:
        arrowangle+=v
        if arrowangle==366:
            arrowangle=0
    if keys[pygame.K_e]:
        arrowangle-=v
        if arrowangle==-1:
            arrowangle=0
    pos = str(x)+" "+str(600 - y)
    label = myfont.render(pos, 1, (0,0,0))
    
    #print(readgps(latitude, longitude)[0], 'N ', readgps(latitude, longitude)[1], 'W')
    #print(readgps(latitude,longitude))
    #time.sleep(1) 
    #x = 500 + (float(readgps(latitude,longitude)[1]) - 7927.9652)*50000
    #y = 500 + (float(readgps(latitude,longitude)[0]) - 4346.9310)*50000
    print(pos)
    # This limits the while loop to a max of 10 times per second.
    # Leave this out and we will use all CPU we can.
    clock.tick(10)
    
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done=True # Flag that we are done so we exit this loop
    
    newArrow = rotatefunc(arrowangle, arrow)
    screen.blit(red_rect,(0,0))
    screen.blit(newArrow,(int(x),int(y)))
    #pygame.draw.circle(screen, BLUE, [int(x), int(y)], 3)




    #my_polygon = pygame.draw.polygon(screen, BLUE, [[int(x)-5,int(y)+15],[int(x),int(y)],[int(x)+5,int(y)+15]],3)






    screen.blit(label,(x-30,y-10))    
    #pygame.draw.line(screen, GREEN, [oldx, oldy], [int(x),int(y)], 5)
    pygame.display.flip()
# Be IDLE friendly
pygame.quit()
