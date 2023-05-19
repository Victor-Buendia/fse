import sys
import struct # https://docs.python.org/2/library/struct.html#struct.pack

class Message:
	def __init__(self):
		self.__identifier = '0601'

	def get_package(self, command, message):
		"""
			Get package.
		"""
		message, command = self.cast(message)

		if isinstance(message, str):
			byte_array = [
				command,
				len(message),
				*[ord(char) for char in str(message)],
				*self.enrollment_id
			]
		else:
			byte_array = [
				command,
				*list(struct.pack("i" if isinstance(message, int) else "f", message)),
				*self.enrollment_id
			]
		return byte_array

	def cast(self, value):
		if value.isdigit():
			print('Sou INT')
			return int(value), 0xB1
		elif value.replace('.', '', 1).isdigit():
			print('Sou FLOAT')
			return float(value), 0xB2
		else:
			return value, 0xB3

	@property
	def enrollment_id(self):
		return [int(num) for num in str(self.__identifier)]