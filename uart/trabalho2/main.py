import serial

uart0_filestream = None

try:
	uart0_filestream = serial.Serial('/dev/serial0', 9600, timeout=1)  # Open UART port
	print("UART inicializada!")

	matricula = 601
	tx_buffer = [0xA1, 601]
	aa = bytes(tx_buffer)

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
