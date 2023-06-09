import os
import csv

alimentos = 'csv/opcoes.csv'

def main_menu():
    os.system('clear')
    print('Escolha os modos de operação:')
    print('1 - Manual')
    print('2 - Pré-programado')

    modo = input('Digite o modo: ')

    while modo != '1' and modo != '2':
        print('Modo inválido')
        modo = input('Digite o modo: ')
    
    return modo


def menu_pre_programado():

    opcoes = []  # Lista para armazenar as opções

    with open(alimentos, 'r') as arquivo:
        leitor_csv = csv.reader(arquivo, delimiter=';')
        next(leitor_csv)  # Pular a primeira linha (cabeçalho)

        print('Escolha o alimento:\n')

        for indice, linha in enumerate(leitor_csv, start=1):

            opcao = [linha[0], linha[1]]
            opcoes.append(opcao)
            print(f"{indice}:{opcao[0]} - tempo: {opcao[1]} minuto(s)")

        print(f"{indice+1}:Voltar")

        escolha = input('Digite a opção: ')

        
        
        while (int(escolha) < 1 or int(escolha) > indice+1):
            print('Opção inválida')
            escolha = input('Digite a opção: ')

        if (escolha == str(indice+1)):
            return -1
        
        return opcoes[int(escolha)-1]
