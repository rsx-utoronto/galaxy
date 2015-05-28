import socket, threading
from serial import *
import serial
import socket
import time
import pygame
from math import pi

##########GROUND STATION SERVER RECEIVES SENSOR AND GPS VALUE FROM ##########

HOST = '192.168.1.105 ' #Laptop IP address
PORT = 51237

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(4)
clients = [] #list of clients connected
lock = threading.Lock()


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

pygame.display.set_caption("Example code for the draw module")
myfont = pygame.font.SysFont("monospace", 15)

"""Reference Point Definition"""
#Reference1 = 
reference_y1 = 3820.0749
reference_x1 = 11100.8749
#Reference2 =
reference_y2 = 3820.0510
reference_x2 = 11100.8906
#Reference3 =
reference_y3 = 4346.9212
reference_x3 = 7928.0415
#Reference4 =
reference_y4 = 4346.9695
reference_x4 = 7928.0534
#Reference5 =
reference_y5 = 4346.9705
reference_x5 = 7927.8968


#ser = serial.Serial('/dev/ttyUSB0', 4800, timeout=1)
latitude = ''
longitude = ''

"""Pictures of the Desert"""
red_rect = pygame.image.load('MDRS.png')
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

"""def readgps(latitude,longitude):
    #Read the GPG LINE using the NMEA standard
    while True:
        line = ser.readline()
        if "GPGGA" in line:
            latitude = line[18:27] #Yes it is positional info for lattitude
            longitude = line[30:40] #do it again
            return(latitude,longitude)
    print "Finished"
"""

def processAdress(lon, lat):
    x1 = 695 + (float(lon) - reference_x1)*(-10500/2)
    y1 = 400 + (float(lat) - reference_y1)*(-15600/2)
    x2 = 930 + (float(lon) - reference_x2)*(-10500/2)
    y2 = 365 + (float(lat) - reference_y2)*(-15600/2)
    x3 = 290 + (float(lon) - reference_x3)*(-10500/2)
    y3 = 375 + (float(lat) - reference_y3)*(-15600/2)
    x4 = 220 + (float(lon) - reference_x4)*(-10500/2)
    y4 = 45 + (float(lat) - reference_y4)*(-15600/2)
    x5 = 1075 + (float(lon) - reference_x5)*(-10500/2)
    y5 = 20 + (float(lat) - reference_y5)*(-15600/2)
    x = (x1+x2)/2
    y = (y1+y2)/2
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
            sensor_data = self.socket.recv(1024)
            print "Unprocessed data: " + sensor_data
            sensor_data_split = sensor_data.split(",")
            if not sensor_data:
                break
                    
            #lon = readgps(latitude,longitude)[1]
            #lat = readgps(latitude,longitude)[0]
            lon = sensor_data_split[0]
            lat = sensor_data_split[1]
            #arrowangle = sensor_data_split[len(sensor_data_split)-1]
            arrowangle = 0
            #print(lon,lat)
            x = processAdress(lon,lat)['lon']
            y = processAdress(lon,lat)['lat']
            print(x,y)
            ast1x = processAdress(ast_1_lon,ast_1_lat)['lon']
            ast1y = processAdress(ast_1_lon,ast_1_lat)['lat']

            ast2x = processAdress(ast_2_lon,ast_2_lat)['lon']
            ast2y = processAdress(ast_2_lon,ast_2_lat)['lat']

            ast3x = processAdress(ast_3_lon,ast_3_lat)['lon']
            ast3y = processAdress(ast_3_lon,ast_3_lat)['lat']

            ast4x = processAdress(ast_4_lon,ast_4_lat)['lon']
            ast4y = processAdress(ast_4_lon,ast_4_lat)['lat']

            #ast5x = processAdress(ast_4_lon,ast_4_lat)['lon']
            #ast5y = processAdress(ast_4_lon,ast_4_lat)['lat']
            #ast6x = processAdress(ast_4_lon,ast_4_lat)['lon']
            #ast6y = processAdress(ast_4_lon,ast_4_lat)['lat']
            #ast7x = processAdress(ast_4_lon,ast_4_lat)['lon']
            #ast7y = processAdress(ast_4_lon,ast_4_lat)['lat']

            for event in pygame.event.get(): # User did something
                if event.type == pygame.QUIT: # If user clicked close
                    done=True # Flag that we are done so we exit this loop
            #screen.blit(red_rect,(0,0))
            #pygame.draw.circle(screen, RED, [int(x), int(y)], 10)

            print("Processed Data: ")
            print(sensor_data_split)

            newArrow = rot_center(arrow, float(arrowangle))
            screen.blit(red_rect,(0,0))
            screen.blit(newArrow,(int(x),int(y)))

            #print(x, y)
            #print(ast1x,ast1y)
            
            pygame.draw.circle(screen, GREEN, [int(ast1x), int(ast1y)], 10)
            pygame.draw.circle(screen, WHITE, [int(ast2x), int(ast2y)], 10)
            pygame.draw.circle(screen, BLACK, [int(ast3x), int(ast3y)], 10)
            pygame.draw.circle(screen, BLUE, [int(ast4x), int(ast4y)], 10)
            #pygame.draw.circle(screen, BLUE, [int(ast5x), int(ast5y)], 10)
            #pygame.draw.circle(screen, BLUE, [int(ast6x), int(ast6y)], 10)
            #pygame.draw.circle(screen, BLUE, [int(ast7x), int(ast7y)], 10)

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
    #print sensor_data





