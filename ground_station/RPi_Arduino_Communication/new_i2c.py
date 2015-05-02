import smbus, time

def read_int(address):
	"""
	Read 4 bytes (as a 32-bit int) from the i2c stream. The least significant bits are first. 
	
	Parameters:
	address -  address of the arduino
	
	Returns: 
	an int from the stream
	"""
	result = 0
	for i in range(4):
		result += bus.read_byte(address) << i * 8
	return result
	
def read_int_from_sensor(address, sensor_port):
	"""
	Read an integer from a specified sensor on the arduino. 
	
	Parameters:
	address - the address of the arduino
	sensor_port - the number of the sensor on the arduino (e.g. 0 for A0, 25 for 25, etc.)
	
	Returns:
	an int from the sensor
	"""
	bus.write_byte(address, sensor_port)
	time.sleep(0.05)  # for stability. If the commands lag, increase this. 
	return read_int(address)
			
if __name__ == '__main__':
	bus = smbus.SMBus(1)
	address = 0x2a  # address of the arduino

	while True:
		input = int(raw_input(" Which Arduino port to read from? >>> "))
		print(read_int_from_sensor(address, input))
		
		time.sleep(0.2)