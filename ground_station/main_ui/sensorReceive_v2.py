import socket, threading
from serial import *
import time
import pygame
from math import pi

HOST = '192.168.1.100' #RPi IP address
PORT = 51239

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(4)
clients = [] #list of clients connected
lock = threading.Lock()
done = False

# Initialize the game engine
pygame.init()
# Define the colors we will use in RGB format
BLACK = ( 0, 0, 0)
WHITE = (255, 255, 255)
BLUE = ( 0, 0, 255)
GREEN = ( 0, 255, 0)
RED = (255, 0, 0)
# Set the height and width of the screen
size = [1500, 1500]
screen = pygame.display.set_mode(size)

clock = pygame.time.Clock()

pygame.display.set_caption("Example code for the draw module")
myfont = pygame.font.SysFont("monospace", 15)

"""Reference Point Definition"""
regionx = 11000
regiony = 3800

def decimal_gps(reference_x, reference_y):
    x = (reference_x - regionx)/60+regionx/100
    y = (reference_y - regiony)/60+regiony/100
    return (x,y) 

"""Reference Point Definition"""
#Reference1 = 11100.8749 3820.0719
reference_x1 = decimal_gps(11047.5157,3824.3837)[0]
reference_y1 = decimal_gps(11047.5157,3824.3837)[1]
#Reference2 = 11100.8906 3820.0510
reference_x2 = decimal_gps(11047.3920,3824.3128)[0]
reference_y2 = decimal_gps(11047.3920,3824.3128)[1]
#Reference1 = 11100.8749 3820.0719
reference_x3 = decimal_gps(11047.0378,3824.5186)[0]
reference_y3 = decimal_gps(11047.0378,3824.5186)[1]
#Reference2 = 11100.8906 3820.0510
reference_x4 = decimal_gps(11047.5536,3824.1356)[0]
reference_y4 = decimal_gps(11047.5536,3824.1356)[1]


imagex1 = 552 #Hab
imagey1 = 198
imagex2 = 608 #Fork right
imagey2 = 238
imagex3 = 774 #Apex sharp bend north
imagey3 = 114 
imagex4 = 532 #Apex sharp bend south
imagey4 = 346



senx = (imagex2-imagex1)/(reference_x2-reference_x1)
seny = (imagey2-imagey1)/(reference_y2-reference_y1)

#ser = serial.Serial('/dev/ttyUSB0', 4800, timeout=1)
latitude = ''
longitude = ''

"""Pictures of the Desert"""
red_rect = pygame.image.load('MDRS_USED.png')
w,h = red_rect.get_size()
x_scale = 0.8
y_scale = 0.8
red_rect = pygame.transform.scale(red_rect, (int(w*x_scale),int(h*y_scale)))

arrow = pygame.image.load('triangle.png')
arrow = pygame.transform.scale(arrow, (20,20))


"""Change the Location of the astronaut"""
ast_1_lon = 07927.9620
ast_1_lat = 4346.9230

ast_2_lon = 7927.9680 #white, increase lon --> decrease x
ast_2_lat = 4346.9290

ast_3_lon = 7927.9580 #black, decrease lat --> decrease y
ast_3_lat = 4346.9190

ast_4_lon = 7927.9550
ast_4_lat = 4346.9160


def rot_center(image, angle):
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image

def readgps(latitude,longitude):
    #Read the GPG LINE using the NMEA standard
    while True:
        line = ser.readline()
        if "GPGGA" in line:
            latitude = line[18:27] #Yes it is positional info for lattitude 3000
            longitude = line[30:40] #do it again 11100
	    print("============latitude, longitude=============")
	    print(latitude, longitude)
	    print("=========================")

            return(latitude,longitude)
    print "Finished"

def processAdress(lon, lat):
    (declon,declat) = decimal_gps(float(lon),float(lat))
    x1 = imagex1 + (declon-reference_x1)*senx
    y1 = imagey1 + (declat-reference_y1)*seny
    x2 = imagex2 + (declon-reference_x2)*senx
    y2 = imagey2 + (declat-reference_y2)*seny
    x3 = imagex3 + (declon-reference_x3)*senx
    y3 = imagey3 + (declat-reference_y3)*seny
    x4 = imagex4 + (declon-reference_x4)*senx
    y4 = imagey4 + (declat-reference_y4)*seny
    """
    print("============diff=============")
    print((declon-reference_x1)*senx, (declon-reference_x1))
    print((declat-reference_y1)*seny, (declat-reference_y1))
    print("=========================")
    """
    x = ((x1+x2+x3+x4)/4)
    y = ((y1+y2+y3+y4)/4)
    print("============diff=============")
    print(x, y)
    print("=========================")
    return {'lon':x, "lat":y}


class chatServer(threading.Thread):
    def __init__(self, (socket,address)):
        threading.Thread.__init__(self)
        self.socket = socket
        self.address= address

    def run(self):
        lock.acquire()
        clients.append(self)
        lock.release()
        print '%s:%s connected.' % self.address
        while True:
            data = self.socket.recv(1024)
            if not data:
                break

	    lon = 11047.3900
	    lat = 3824.3200
	    print("============lat,long=============")
	    print(data)
	    print("=========================")    
	    x = processAdress(lon,lat)['lon']
	    y = processAdress(lon,lat)['lat']

	    arrowangle = 0
            
           clock.tick(10)
	    for event in pygame.event.get(): # User did something
		if event.type == pygame.QUIT: # If user clicked close
		    done=True # Flag that we are done so we exit this loop
	    #screen.blit(red_rect,(0,0))
	    #pygame.draw.circle(screen, RED, [int(x), int(y)], 10)

	    print("*****...********************")
	    print(int(x),int(y))
	    print("*************************")

	    newArrow = rot_center(arrow, arrowangle)
	    screen.blit(red_rect,(0,0))
	    
	    pygame.draw.circle(screen, BLUE, [imagex1, imagey1], 10)
	    pygame.draw.circle(screen, WHITE, [imagex2, imagey2], 10)
	    pygame.draw.circle(screen, BLUE, [imagex3, imagey3], 10)
	    pygame.draw.circle(screen, WHITE, [imagex4, imagey4], 10)
	    screen.blit(newArrow,(int(x),int(y)))

	    #screen.blit(label,(x-30,y-10))

	    pygame.display.flip()

	pygame.quit()

        self.socket.close()
        print '%s:%s disconnected.' % self.address
        lock.acquire()
        clients.remove(self)
        lock.release()

while True: # wait for socket to connect
    # send socket to chatserver and start monitoring
    chatServer(s.accept()).start()
