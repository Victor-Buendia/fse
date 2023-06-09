import os

STATES_MENU = [
    'INITIAL',
    'MAN',
    'AUTO',
    'TEMP',
    'TIME',
]


def initial(option):
    os.system('clear' if os.name == 'posix' else 'clear')
    print('Modo:')
    print('[x] ' if option % 2 == 0 else '[ ] ', end='')
    print('Auto')
    print('[x] ' if option % 2 == 1 else '[ ] ', end='')
    print('Manual')
    print(f'TEMPERATURA: {option} °C')
