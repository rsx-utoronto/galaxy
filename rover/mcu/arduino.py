# arduino.py
# Create a one-size-fits-all interface between Python (computer or Raspberry Pi) and Arduino.  

import serial
from time import *

def connect_to_serial(): # def connect_to_serial(digital_outs):
        """
        Establish a connection to the serial port and return it. 
        The name of the USB port is irregular depending on OS and computer. 
        Also, decide which ports are for output. 

        Parameters:
        digital_outs: a list of digital pins to set to output. 

        Returns:
        the serial port as a serial.Serial object

        Raises:
        serial.SerialException if no successful connection is made. 
        """
        ser = None

        # Linux. works on the RSX computer. 
        for i in range(100):
                try:
                        ser = serial.Serial("/dev/ttyACM" + str(i), timeout=0.1)
                        #print("Connected to port", i)
                        break
                except serial.SerialException:
                        pass
        # Windows. 
        for i in range(50):
                try:
                        ser = serial.Serial(i, timeout=1)
                        #print("Connected to port", i)
                        break
                except serial.SerialException:
                        pass

        if ser is None:
                raise Exception("Serial not connected")

        return ser

def write_port(serial, port, command):
        """ 
        Write a command to a port on the Arduino

        Parameters: 
        serial - an instance of serial.Serial, the serial connection
        port - an int (between 0 and 255) representing the port number. Analog pins are their number + 100
        command - an int (between 0 and 255) representing the command to send. 

        Returns:
        None
        """
        serial.write(chr(1))
        serial.write(chr(port))
        serial.write(chr(command))
        # print("wrote {} to port {}".format(command, port))  for debugging purposes

def read_port(serial, port):
        """
        Reads one byte from the Arduino. 

        Parameters:
        serial - an instance of serial.Serial, the serial connection
        port - an int (between 0 and 255) representing the port number. Analog pins are their number + 100

        Returns:
        an int
        """
        serial.write(chr(0)) #read data
        serial.write(chr(port))
        serial.write(chr(0)) # garbage
        o = ord(serial.read())
        return o

# USE KEYBOARD CONTROLS: 
if __name__ == '__main__':
        ser = connect_to_serial()
        port = 0

        print("Send a command to port 255 to read instead") 
        while(port != 255):
                port, command = [int (i) for i in raw_input("Enter the port number, then the command to write >>> ").split()]
                write_port(ser, port, command)

        while(True):
                port = int(raw_input("Which port should we read from >>> "))
                print(read_port(ser, port))
