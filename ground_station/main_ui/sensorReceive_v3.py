import socket, threading
from serial import *
import time
import pygame
from math import pi

HOST = '192.168.1.100' #RPi IP address
PORT = 51240

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
ORANGE = (230,255,0)
YELLOW = (125,255,0)
PURPLE = (0,255,255)

# Set the height and width of the screen
size = [1500, 1500]
screen = pygame.display.set_mode(size)

clock = pygame.time.Clock()

pygame.display.set_caption("Example code for the draw module")
myfont = pygame.font.SysFont("monospace", 15)

"""Reference Point Definition"""
regionx = 11000 #For hab area
regiony = 3800
#regionx = 11100 #For motel area
#regiony = 3800


def decimal_gps(reference_x, reference_y):
    x = (reference_x - regionx)/60+regionx/100
    y = (reference_y - regiony)/60+regiony/100
    return (x,y) 

"""Reference Point Definition"""
#Reference1 = 11100.8749 3820.0719
reference_x1 = decimal_gps(11078.3533,3841.4673)[0]
reference_y1 = decimal_gps(11078.3533,3841.4673)[1]
#Reference2 = 11100.8906 3820.0510
reference_x2 = decimal_gps(11078.5696,3841.6433)[0]
reference_y2 = decimal_gps(11078.5696,3841.6433)[1]
#Reference1 = 11100.8749 3820.0719
reference_x3 = decimal_gps(11078.1611,3841.7795)[0]
reference_y3 = decimal_gps(11078.1611,3841.7795)[1]
#Reference2 = 11100.8906 3820.0510
reference_x4 = decimal_gps(11078.1156,3841.4285)[0]
reference_y4 = decimal_gps(11078.1156,3841.4285)[1]


imagex1 = 535 #ball center: 3841.4673 11078.3533
imagey1 = 340
imagex2 = 385 #left teeth: 3841.6433 11078.5696 
imagey2 = 180
imagex3 = 670 #mouth: 3841.7795 11078.1611
imagey3 = 60 
imagex4 = 700 #end: 3841.4285 11078.1156
imagey4 = 380

senx = (imagex2-imagex1)/(reference_x2-reference_x1)
seny = (imagey2-imagey1)/(reference_y2-reference_y1)

#ser = serial.Serial('/dev/ttyUSB0', 4800, timeout=1)
latitude = ''
longitude = ''

"""Pictures of the Desert"""

red_rect = pygame.image.load('ASTCapture.png')
"""
red_rect = pygame.image.load('Roadside.png')
"""
w,h = red_rect.get_size()
x_scale = 1.2
y_scale = 1.2
red_rect = pygame.transform.scale(red_rect, (int(w*x_scale),int(h*y_scale)))

arrow = pygame.image.load('triangle.png')
arrow = pygame.transform.scale(arrow, (15,15))


"""Change the Location of the astronaut"""
ast_1_lon = 11078.3150 #white
ast_1_lat = 3841.5865

ast_2_lon = 110 #black, increase lon --> decrease x
ast_2_lat = 38

ast_3_lon = 110 #red, decrease lat --> decrease y
ast_3_lat = 38

ast_4_lon = 110 #orange
ast_4_lat = 38

ast_5_lon = 110 #yellow
ast_5_lat = 38

ast_6_lon = 110 #green
ast_6_lat = 38

ast_7_lon = 110 #blue
ast_7_lat = 38

ast_8_lon = 110 #purple
ast_8_lat = 38


ast_9_lon = 110 
ast_9_lat = 38


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
	    #print("============latitude, longitude=============")
	    print(latitude, longitude)
	    #print("=========================")

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
    
    x = ((x1+x2+x3+x4)/4)
    y = ((y1+y2+y3+y4)/4)

    #print("============diff=============")
    #print(x, y)
    #print("=========================")
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
        done = False

        while not done:
            data = self.socket.recv(1024)
            print("##################")
            print(data)
            print("##################")

            if not data:
                break

            data_split = data.split(',')

            #print(float(data_split[0]),float(data_split[1]))
            lon = float(data_split[0])
            lat = float(data_split[1])
            

            x = processAdress(lon,lat)['lon']
            y = processAdress(lon,lat)['lat']
            
            ast_1_x = processAdress(ast_1_lon,ast_1_lat)['lon']
            ast_1_y = processAdress(ast_1_lon,ast_1_lat)['lat']

            ast_2_x = processAdress(ast_2_lon,ast_2_lat)['lon']
            ast_2_y = processAdress(ast_2_lon,ast_2_lat)['lat']

            ast_3_x = processAdress(ast_3_lon,ast_3_lat)['lon']
            ast_3_y = processAdress(ast_3_lon,ast_3_lat)['lat']

            ast_4_x = processAdress(ast_4_lon,ast_4_lat)['lon']
            ast_4_y = processAdress(ast_4_lon,ast_4_lat)['lat']

            ast_5_x = processAdress(ast_5_lon,ast_5_lat)['lon']
            ast_5_y = processAdress(ast_5_lon,ast_5_lat)['lat']

            ast_6_x = processAdress(ast_6_lon,ast_6_lat)['lon']
            ast_6_y = processAdress(ast_6_lon,ast_6_lat)['lat']

            ast_7_x = processAdress(ast_7_lon,ast_7_lat)['lon']
            ast_7_y = processAdress(ast_7_lon,ast_7_lat)['lat']

            ast_8_x = processAdress(ast_8_lon,ast_8_lat)['lon']
            ast_8_y = processAdress(ast_8_lon,ast_8_lat)['lat']


            arrowangle = 0
                
            clock.tick(10)
            for event in pygame.event.get(): # User did something
                if event.type == pygame.QUIT: # If user clicked close
                    done=True # Flag that we are done so we exit this loop
	        #screen.blit(red_rect,(0,0))
	        #pygame.draw.circle(screen, RED, [int(x), int(y)], 10)

            #print("*****...********************")
            #print(int(x),int(y))
            #print("*************************")

            newArrow = rot_center(arrow, arrowangle)
            screen.blit(red_rect,(0,0))

            #pygame.draw.circle(screen, BLUE, [imagex1, imagey1], 10)
            #pygame.draw.circle(screen, WHITE, [imagex2, imagey2], 10)
            #pygame.draw.circle(screen, BLUE, [imagex3, imagey3], 10)
            #pygame.draw.circle(screen, WHITE, [imagex4, imagey4], 10)
            pygame.draw.circle(screen, WHITE, [int(ast_1_x), int(ast_1_y)], 7)
            pygame.draw.circle(screen, BLACK, [int(ast_2_x), int(ast_2_y)], 7)
            pygame.draw.circle(screen, RED, [int(ast_3_x), int(ast_3_y)], 7)
            pygame.draw.circle(screen, ORANGE, [int(ast_4_x), int(ast_4_y)], 7)
            pygame.draw.circle(screen, YELLOW, [int(ast_5_x), int(ast_5_y)], 7)
            pygame.draw.circle(screen, GREEN, [int(ast_6_x), int(ast_6_y)], 7)
            pygame.draw.circle(screen, BLUE, [int(ast_7_x), int(ast_7_y)], 7)
            pygame.draw.circle(screen, PURPLE, [int(ast_8_x), int(ast_8_y)], 7)


            screen.blit(newArrow,(int(x),int(y)))
            pos1 = "A1"
            label1 = myfont.render(pos1, 1, (0,0,0))
            screen.blit(label1,(ast_1_x-8,ast_1_y-8))

            pos2 = "A2"
            label2 = myfont.render(pos2, 1, (0,0,0))
            screen.blit(label2,(ast_2_x-8,ast_2_y-8))

            pos3 = "A3"
            label3 = myfont.render(pos3, 1, (0,0,0))
            screen.blit(label3,(ast_3_x-8,ast_3_y-8))

            pos4 = "A4"
            label4 = myfont.render(pos4, 1, (0,0,0))
            screen.blit(label4,(ast_4_x-8,ast_4_y-8))

            pos5 = "A5"
            label5 = myfont.render(pos5, 1, (0,0,0))
            screen.blit(label5,(ast_5_x-8,ast_5_y-8))

            pos6 = "A6"
            label6 = myfont.render(pos6, 1, (0,0,0))
            screen.blit(label6,(ast_6_x-8,ast_6_y-8))

            pos7 = "A7"
            label7 = myfont.render(pos7, 1, (0,0,0))
            screen.blit(label7,(ast_7_x-8,ast_7_y-8))

            pos8 = "A8"
            label8 = myfont.render(pos8, 1, (0,0,0))
            screen.blit(label8,(ast_8_x-8,ast_8_y-8))

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
