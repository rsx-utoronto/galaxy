import socket, threading
from serial import *
import serial
import socket
import time
import pygame
from math import pi

#HOST = "192.168.1.101"
HOST = "100.64.244.34" #wlan address
#100.64.244.34
PORT = 51235

# Initialize the game engine
pygame.init()
# Define the colors we will use in RGB format
BLACK = ( 0, 0, 0)
WHITE = (255, 255, 255)
BLUE = ( 0, 0, 255)
GREEN = ( 0, 255, 0)
RED = (255, 0, 0)

# Set the height and width of the screen
size = [1090, 440]
screen = pygame.display.set_mode(size)

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
ast_1_lon = 07927.9620
ast_1_lat = 4346.9230
ast_2_lon = 7927.9680 #white, increase lon --> decrease x
ast_2_lat = 4346.9290
ast_3_lon = 7927.9580 #black, decrease lat --> decrease y
ast_3_lat = 4346.9190
ast_4_lon = 7927.9550
ast_4_lat = 4346.9160

def processAdress(lon, lat):
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
    return {'lon':x, "lat":y}

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(4)
clients = [] #list of clients connected
lock = threading.Lock()

#ser = Serial("/dev/ttyUSB0", 9600, timeout = 0.01, writeTimeout = 0.01)

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
            split_data = data.split(",")
            print(split_data)

            lon = float(split_data[1])
            lat = float(split_data[0])

            print('processed')
            print(lon,lat)

            x = processAdress(lat,lon)['lon']
            y = processAdress(lat,lon)['lat']

            print('pygame map coord:')
            print(x,y)

            ast1x = processAdress(ast_1_lon,ast_1_lat)['lon']
            ast1y = processAdress(ast_1_lon,ast_1_lat)['lat']
            ast2x = processAdress(ast_2_lon,ast_2_lat)['lon']
            ast2y = processAdress(ast_2_lon,ast_2_lat)['lat']
            ast3x = processAdress(ast_3_lon,ast_3_lat)['lon']
            ast3y = processAdress(ast_3_lon,ast_3_lat)['lat']
            ast4x = processAdress(ast_4_lon,ast_4_lat)['lon']
            ast4y = processAdress(ast_4_lon,ast_4_lat)['lat']

            # This limits the while loop to a max of 10 times per second.
            # Leave this out and we will use all CPU we can.
            #clock.tick(10)

            for event in pygame.event.get(): # User did something
                if event.type == pygame.QUIT: # If user clicked close
                    done=True # Flag that we are done so we exit this loop

            screen.blit(red_rect,(0,0))
            pygame.draw.circle(screen, RED, [int(x), int(y)], 10)
            pygame.draw.circle(screen, GREEN, [int(ast1x), int(ast1y)], 10)
            pygame.draw.circle(screen, WHITE, [int(ast2x), int(ast2y)], 10)
            pygame.draw.circle(screen, BLACK, [int(ast3x), int(ast3y)], 10)
            pygame.draw.circle(screen, BLUE, [int(ast1x), int(ast1y)], 10)

            #screen.blit(label,(x-30,y-10))
            #pygame.draw.line(screen, GREEN, [oldx, oldy], [int(x),int(y)], 5)
            pygame.display.flip()

            #for c in clients:
            #c.socket.send(data)
		    #print data
		    #ser.write(str(data) + "\n")

        self.socket.close()
        print '%s:%s disconnected.' % self.address
        lock.acquire()
        clients.remove(self)
        lock.release()

while True: # wait for socket to connect
    # send socket to chatserver and start monitoring
    chatServer(s.accept()).start()
pygame.quit()
