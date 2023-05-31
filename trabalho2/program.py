from modbus import Modbus
from temperature import Temperature
from uart import UART
from gpio import GPIO
from crc import get_crc16

import constants as C
import time
import os
import struct # https://docs.python.org/3/library/struct.html
import signal
import threading

class Program:
	def __init__(self):
		self.message = Modbus()
		self.uart = UART()
		self.gpio = GPIO()

		self.intern = Temperature(self.message, self.uart, 0xC1)
		time.sleep(0.1)
		self.reference = Temperature(self.message, self.uart, 0xC2)

		self.alarm_running = False

		self.commands_description = {
			0x00: "Nada"
			, 0x01: "Ligar AirFryer"
			, 0x02: "Desligar AirFryer"
			, 0x03: "Iniciar Aquecimento"
			, 0x04: "Cancelar Processo"
			, 0x05: "Tempo +"
			, 0x06: "Tempo -"
			, 0x07: "Menu"
		}
		self.commands = {
			0x00: "Nada"
			, 0x01: self.turn_on_off
			, 0x02: self.turn_on_off
			, 0x03: self.start_stop
			, 0x04: self.start_stop
			, 0x05: "Tempo +"
			, 0x06: "Tempo -"
			, 0x07: "Menu"
		}

		signal.signal(signal.SIGINT, self.signal_handler)
		signal.signal(signal.SIGALRM, self.alarm)
	
	def start(self):
		# loop controle
		signal.alarm(1)

		# loop comandos
		while True:
			time.sleep(0.2)
			self.get_user_command()

		self.uart.close()

	def control_loop(self):
		self.intern.get_temperature()
		time.sleep(0.1)
		self.reference.get_temperature()
		
		print('INTERN TEMPERATURE: ', self.intern.temperature)
		print('REFERENCE TEMPERATURE: ', self.reference.temperature)
	
	def alarm(self, sig, frame):
		signal.alarm(1)

		if not self.alarm_running:
			self.alarm_thread = threading.Thread(target=self.control_loop)
			self.alarm_thread.start()
			self.alarm_thread.join()
			self.alarm_running = False

	def get_user_command(self):
		msg = self.message.create_package(0x01, 0x23, [0xC3])
		self.uart.write(msg)

		time.sleep(0.1)

		res = self.uart.read(bytes=9)
		origin_register, code, subcode, comm, crc = struct.unpack(f'<BBBiH', res)

		# print(hex(origin_register), hex(code), hex(subcode), comm, crc, '[CRC CALCULADO: ', get_crc16(res[:-2]), ']')
		
		if crc != get_crc16(res[:-2]):
			print('Broken CRC! Requesting data again...')
			self.get_user_command()
		else:
			if comm in [0x01, 0x02]:
				self.commands[comm](1 if comm == 0x01 else 0)
			elif comm in [0x03, 0x04]:
				self.commands[comm](1 if comm == 0x03 else 0)
			# print(self.commands_description[comm])

	def turn_on_off(self, value):
		msg = self.message.create_package(0x01, 0x16, [0xD3, value])
		print("EXECUTEI | Liga/Desliga")
		self.uart.write(msg)

	def start_stop(self, value):
		msg = self.message.create_package(0x01, 0x16, [0xD5, value])
		print("EXECUTEI | Iniciar/Parar")
		self.uart.write(msg)
	
	def clear(self):
		os.system('clear' if os.name == 'posix' else 'clear')

	def signal_handler(self, signal, frame):
		if hasattr(self, 'alarm_thread'):
			self.alarm_thread.join()

		self.uart.close()
		self.gpio.cleanup_pins()

		print("\nForcefully ending program...")
		exit(0)