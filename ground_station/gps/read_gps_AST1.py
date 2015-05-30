import serial
import socket
import time
import pygame
from math import pi


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
regionx = 11000
regiony = 3800

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
w,h = red_rect.get_size()
x_scale = 1.2
y_scale = 1.2
red_rect = pygame.transform.scale(red_rect, (int(w*x_scale),int(h*y_scale)))

arrow = pygame.image.load('triangle.png')
arrow = pygame.transform.scale(arrow, (20,20))


"""Change the Location of the astronaut"""
ast_1_lon = 11078.3154
ast_1_lat = 3841.5861

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

while(True):
    #label = myfont.render(pos, 1, (0,0,0))
        
    #lon = readgps(latitude,longitude)[0]
    #lat = readgps(latitude,longitude)[1]
    lon = 11078.3154
    lat = 3841.5861
    #lon = raw_input("Enter longitude: ")
    #lat = raw_input("Enter latiitude: ")
    print("============lat,long=============")
    print(lon,lat)
    print("=========================")    
    x = processAdress(lon,lat)['lon']
    y = processAdress(lon,lat)['lat']

    arrowangle = 0

    x = processAdress(lon,lat)['lon']
    y = processAdress(lon,lat)['lat']

    #ast1x = processAdress(ast_1_lon,ast_1_lat)['lon']
    #ast1y = processAdress(ast_1_lon,ast_1_lat)['lat']

    #ast2x = processAdress(ast_2_lon,ast_2_lat)['lon']
    #ast2y = processAdress(ast_2_lon,ast_2_lat)['lat']

    #ast3x = processAdress(ast_3_lon,ast_3_lat)['lon']
    #ast3y = processAdress(ast_3_lon,ast_3_lat)['lat']

    #ast4x = processAdress(ast_4_lon,ast_4_lat)['lon']
    #ast4y = processAdress(ast_4_lon,ast_4_lat)['lat']

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

    print("*****...********************")
    print(int(x),int(y))
    print("*************************")

    newArrow = rot_center(arrow, arrowangle)
    screen.blit(red_rect,(0,0))
    
    #pygame.draw.circle(screen, GREEN, [int(ast1x), int(ast1y)], 10)
    #pygame.draw.circle(screen, WHITE, [int(ast2x), int(ast2y)], 10)
    #pygame.draw.circle(screen, BLACK, [int(ast3x), int(ast3y)], 10)
    #pygame.draw.circle(screen, BLUE, [int(ast4x), int(ast4y)], 10)
    #pygame.draw.circle(screen, BLUE, [int(ast5x), int(ast5y)], 10)
    #pygame.draw.circle(screen, BLUE, [int(ast6x), int(ast6y)], 10)
    #pygame.draw.circle(screen, BLUE, [int(ast7x), int(ast7y)], 10)
    pygame.draw.circle(screen, BLUE, [imagex1, imagey1], 10)
    pygame.draw.circle(screen, WHITE, [imagex2, imagey2], 10)
    pygame.draw.circle(screen, BLUE, [imagex3, imagey3], 10)
    pygame.draw.circle(screen, WHITE, [imagex4, imagey4], 10)
    screen.blit(newArrow,(int(x),int(y)))

    #screen.blit(label,(x-30,y-10))

    pygame.display.flip()

pygame.quit()

