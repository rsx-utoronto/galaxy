# Serial protocols

## Objective: 
Create a standard for all connections over serial between the Raspberry Pi and the Arduino. 

## How it works: 
3 bytes are sent at a time: 

Byte | Range | Meaning
----------|--------|-----
**Byte 1**| 0 or 1 | Read or write data respectively
**Byte 2**| 0 - 255 | Which port to read/ write. Note that 100 means A0, 101 means A1, etc. 
**Byte 3**| 0 - 255 | The value to write. For digital pins, 0 is LOW, 1 is HIGH. For analog pins, the value is unchanged. When reading a value, this byte will be ignored. 

## Included files:
### createheader.py
Generates setup code for Python (example_header.py) and Arduino (example_header.c) from a pin configuration (e.g. example.txt). Note that the c header needs to be copied and pasted into the .ino file to be used because I couldn't figure out imports. The python file contains constants and needs to be imported. 

### serial_protocols.ino
This should be file running on the Arduino. It just reads commands over Serial and reads/ writes from the relevant ports. 

### example.py 
Example use case. It hasn't been tested yet because I don't have an Arduino. 

### arduino.py
Python module to be imported. If you run this as main, you get a command line interface that lets you send commands through serial. 

# Note: 
The Python .read command takes about 1 second to return anything because the minimum timeout is 1 s, and for some reason it waits for a timeout before doing anything. I'll need to play with some sensors to debug this. 