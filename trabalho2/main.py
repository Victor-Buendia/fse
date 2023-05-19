import serial

try:
	uart0_filestream = serial.Serial('/dev/serial0', 9600)  # Open UART port
	print("UART inicializada!")

	uart0_filestream.flushInput()
	uart0_filestream.flushOutput()

	tx_buffer = bytearray()
	tx_buffer.extend((0xA1).to_bytes(1, 'big'))
	for i in str(601):
		tx_buffer.extend(int(i).to_bytes(1, 'big'))

	print("Buffers de memória criados!")

	if uart0_filestream is not None:
		print("Escrevendo caracteres na UART ...")
		count = uart0_filestream.write(tx_buffer)
		if count < 0:
			print("UART TX error")
		else:
			print("escrito.")

	# Sleep for 1 second

	uart0_filestream.timeout = 1

finally:
	if uart0_filestream is not None:
		uart0_filestream.close()
