import struct
from modbus import desconecta, le_comando_usuario, solicita_mensagem, envia_mensagem
from constants import codigos, subcodigos, comandos
import RPi.GPIO as GPIO
from pid import pid_controle
import time
from i2c import get_temperatura_bmp
import serial
from menu import main_menu, menu_pre_programado
from log import save_logs, verify_log_file

verify_log_file()

ventoinha = 24
resistor = 23

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(ventoinha, GPIO.OUT)
GPIO.setup(resistor, GPIO.OUT)

ventoinha_pwm = GPIO.PWM(ventoinha,60)
resistor_pwm = GPIO.PWM(resistor,60)

Kp = 20
Ki = 0.2
Kd = 400.0

    

def cozinha(tempo_total, tempo_atual):
        
        temp_interna = solicita_mensagem(codigos['solicitacao'], subcodigos['solicita_temperatura_interna'])
        temp_referencial = solicita_mensagem(codigos['solicitacao'], subcodigos['solicita_temperatura_referencial'])
        temp_ambiente = get_temperatura_bmp()
        envia_mensagem(codigos['envio'], subcodigos['envia_temperatura_ambiente'], temp_ambiente)

        # CALCULA PID E PWM
        valor_pid = 0
        
        valor_pid = pid_controle(int(temp_interna[0]),referencia = temp_referencial[0],Kp=Kp,Ki=Ki,Kd=Kd)
        if valor_pid < 0:

            ventoinha_pwm.start(valor_pid * -1)
            resistor_pwm.stop()
            valor_ventoinha = valor_pid
            valor_resistor = 0

        else:
            #Ligou resistor
            resistor_pwm.start(valor_pid)
            ventoinha_pwm.stop()
            valor_resistor = valor_pid
            valor_ventoinha = 0 


        pid_binario = int(valor_pid).to_bytes(4,'little',signed = True)
        envia_mensagem(codigos['envio'], subcodigos['envia_sinal_controle'], pid_binario)

        print(f'Tempo até terminar:{tempo_total - tempo_atual} Temperatura Interna: {temp_interna[0]} Temperatura Referencial: {temp_referencial[0]} Temperatura Ambiente: {temp_ambiente}\n')

        log = {
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'temperatura_interna': temp_interna[0],
            'temperatura_ambiente': temp_ambiente,
            'temperatura_referencial': temp_referencial[0],
            'ventoinha': f'{valor_ventoinha}%',
            'resistor': f'{valor_resistor}%'
        }

        save_logs(log)

        if temp_interna[0] > temp_referencial[0]:
            global count
            count += 1
            time.sleep(1)
            if count == tempo:
                envia_mensagem(codigos['envio'], subcodigos['modo_controle_temperatura_referencia'], 0)
                envia_mensagem(codigos['envio'], subcodigos['envia_estado_funcionamento'], 0)
                envia_mensagem(codigos['envio'], subcodigos['envia_estado_sistema'], 0)
                resistor_pwm.stop()
                ventoinha_pwm.stop()
                desconecta()
                return True
            else:
                return False
        
        
    
count = 0
while True:
    try:
        modo = main_menu()
        if modo == '1':
            print('Modo manual')

        elif modo == '2':
            print('Modo pre-programado')
            alimento = menu_pre_programado()

            if alimento == -1:
                continue

            print(f'Alimento escolhido: {alimento[0]}')
            
            tempo = int(alimento[1]) * 60
            finished = False
            while not finished:
                finished = cozinha(tempo, tempo_atual=count)


        

    except KeyboardInterrupt:
        envia_mensagem(codigos['envio'], subcodigos['modo_controle_temperatura_referencia'], 0)
        envia_mensagem(codigos['envio'], subcodigos['envia_estado_funcionamento'], 0)
        envia_mensagem(codigos['envio'], subcodigos['envia_estado_sistema'], 0)        
        resistor_pwm.stop()
        ventoinha_pwm.stop()
        break
