matricula = 601

print(matricula.to_bytes(4, 'big'))

a = b'\x00\x00\x02Y'

print(int.from_bytes(a, 'big'))