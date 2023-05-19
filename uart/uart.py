import serial # https://pythonhosted.org/pyserial/pyserial_api.html#classes

class UART:
	def __init__(self):
		self.__port = '/dev/serial0'
		self.__baudrate = 9600
		self.__bytesize = serial.EIGHTBITS

		self.channel = serial.Serial(port=self.__port, baudrate=self.__baudrate, bytesize=self.__bytesize)
		self.channel.reset_input_buffer()
		self.channel.reset_output_buffer()

	def write(self, package):
		self.channel.write(bytes(package))

	def read(self):
		pass
	
	def close(self):
		self.channel.reset_input_buffer()
		self.channel.reset_output_buffer()
		self.channel.close()