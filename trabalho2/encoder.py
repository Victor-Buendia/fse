# uart = serial.Serial('/dev/serial0')
endereco = 1
codigo = 22
subcodigo = 211
matricula = 2386
codigo2 = 1
mensagem = ([endereco, codigo, subcodigo] + [int(digito) for digito in str(matricula)] + [codigo2])

print(mensagem)