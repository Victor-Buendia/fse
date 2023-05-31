import sys
import struct # https://docs.python.org/2/library/struct.html#struct.pack
from crc import get_crc16
import constants as C

class Modbus:
	def __init__(self):
		self.__identifier = '0601'
		self.request = [0xA1, 0xA2, 0xA3, 0xC3, 0xC1, 0xC2]
		self.send	= [0xB1, 0xB2, 0xB3, 0xD3, 0xD5]

	def create_package(self, register_addr, func_code, data):
		byte_array = []
		if data[0] in self.request:
			# Request Data
			byte_array = [
				register_addr
				, func_code
				, *data
				, *self.enrollment_id
			]
		else:
			# Send Data
			message = self.cast(data[1]) if isinstance(data[1], str) else data[1]
			if isinstance(message, str):
				byte_array = [
					register_addr
					, func_code
					, command
					, len(message)
					, *[ord(char) for char in message]
					# , *self.enrollment_id
				]
			else:
				if data[0] in [0xD3, 0xD5]:
					_signal = struct.pack("B" if isinstance(message, int) else "f", message)
				else:
					_signal = struct.pack("i" if isinstance(message, int) else "f", message)

				byte_array = [
					register_addr
					, func_code
					, data[0]
					, *self.enrollment_id
					, *list(_signal)
				]
		crc = get_crc16(byte_array)
		byte_array = byte_array + list(struct.pack('H', crc))
		return byte_array

	def cast(self, value):
		if value.isdigit():
			return int(value)
		elif value.replace('.', '', 1).isdigit():
			return float(value)
		else:
			return value

	@property
	def enrollment_id(self):
		return [int(num) for num in str(self.__identifier)]