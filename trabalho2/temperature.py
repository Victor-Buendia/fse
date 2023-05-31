import time
import struct # https://docs.python.org/3/library/struct.html
from crc import get_crc16

class Temperature:
	def __init__(self, message, uart, subcode: int):
		self.subcode = subcode
		self.message = message
		self.uart = uart

		self.origin_register, self.code, self.subcode, self.temperature, self.crc = self.get_temperature()

	def get_temperature(self):
		self.alarm_running = True
		msg = self.message.create_package(0x01, 0x23, [self.subcode])
		self.uart.write(msg)

		time.sleep(0.2)

		res = self.uart.read(bytes=9)
		self.origin_register, self.code, self.subcode, self.temperature, self.crc = struct.unpack(f'<BBBfH', res)

		if self.crc != get_crc16(res[:-2]):
			print('Broken CRC! Requesting data again...')
			self.origin_register, self.code, self.subcode, self.temperature, self.crc = self.get_temperature()

		return self.origin_register, self.code, self.subcode, self.temperature, self.crc