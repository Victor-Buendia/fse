import RPi.GPIO as GPIO
import time
import menu
from datetime import datetime
from utils import get_diff_milliseconds

# INIT GLOBAL
date1 = datetime.now()

# Defina os pinos utilizados para conectar o encoder à Raspberry Pi
CLK_PIN = 25
DT_PIN = 24
SW_PIN = 23

# Configuração dos pinos GPIO da Raspberry Pi
GPIO.setmode(GPIO.BCM)
GPIO.setup(CLK_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(DT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(SW_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Variáveis para acompanhar o estado do encoder
temperatura = 0
estado_anterior_CLK = GPIO.input(CLK_PIN)

# Função para ler o valor atual do encoder
def ler_encoder(channel):
    global temperatura
    global estado_anterior_CLK

    estado_CLK = GPIO.input(CLK_PIN)
    estado_DT = GPIO.input(DT_PIN)

    if estado_CLK != estado_anterior_CLK:
        if estado_DT != estado_CLK:
            temperatura += 5
            print("girou pra horario")
        else:
            temperatura -= 5
            print("girou pra anti-horario")

    menu.initial(temperatura)

    estado_anterior_CLK = estado_CLK

# Função para lidar com a ação do botão do encoder
def lidar_com_botao(channel):
    global date1

    if get_diff_milliseconds(date1, datetime.now()) < 1000:
        print('Voltar! Apertou duas vezes')
    else:
        date1 = datetime.now()
        print("Botão pressionado!\a")


# Configuração das interrupções para os pinos do encoder e do botão
GPIO.add_event_detect(CLK_PIN, GPIO.BOTH, callback=ler_encoder)
GPIO.add_event_detect(SW_PIN, GPIO.FALLING, callback=lidar_com_botao, bouncetime=300)

# Loop principal do programa
try:
    while True:
        # Seu código principal aqui
        # Você pode usar o valor do contador para acompanhar a rotação do encoder

        time.sleep(0.1)  # Espera um pouco antes de ler novamente o encoder

except KeyboardInterrupt:
    pass

# Limpeza dos pinos GPIO antes de sair do programa
GPIO.cleanup()
