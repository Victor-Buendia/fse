def enviar_envio_dados(comando, dado, matricula):
    if isinstance(dado, str):
        tamanho_string = len(dado)  # Tamanho da string (1 byte)
        mensagem = [comando, tamanho_string] + [ord(caractere) for caractere in dado] + [int(digito) for digito in str(matricula)]
        print(bytes(mensagem))

    if isinstance(dado, int):
        mensagem = [comando] + list(struct.pack('i', dado)) + [int(digito) for digito in str(matricula)]
    
    if isinstance(dado, float):
        mensagem = [comando] + list(struct.pack('f', dado)) + [int(digito) for digito in str(matricula)]
        print(struct.pack('f', dado))

    uart.write(bytes(mensagem))  # Envio da mensagem