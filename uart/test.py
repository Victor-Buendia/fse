import struct
command = 0xB1
message = 456
identifier = '0601'

byte_array = [
	command,
	*list(struct.pack("i" if isinstance(message, int) else "f", message)),
	*[int(i) for i in identifier]
]

print(byte_array)
print(bytes(byte_array))