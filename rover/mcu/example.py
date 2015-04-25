import arduino
from example_header import *

ser = arduino.connect_to_serial()

arduino.write_port(ser, RED_LED_PIN, 100)  # set the red LED at pin 6 to brightness 100
arduino.write_port(ser, ELBOW_PIN, 90)  # set the servo at pin 9 to 90 degrees. 

