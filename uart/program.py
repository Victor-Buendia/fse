from message import Message
from uart import UART
import time
import os

class Program:
	def __init__(self):
		self.message = Message()
		self.uart = UART()
	
	def clear(self):
		os.system('clear' if os.name == 'posix' else 'clear')

	def start(self):

		# while True:
		self.clear()
		self.menu()
		option = input()

		try:
			option = int(option)
		except:
			pass
			# continue

		if option == 0:
			exit()
		elif option == 1:
			self.send_message()
		elif option == 2:
			pass

	def menu(self):
		print('------------ MENU -----------')
		print('(0) Exit')
		print('(1) Send data')
		print('(2) Request data')

	def send_message(self):
		msg = input('Type in your message: ')
		self.uart.write(self.message.get_package(command=0xB1, message=msg))
		time.sleep(1)
		self.uart.close()