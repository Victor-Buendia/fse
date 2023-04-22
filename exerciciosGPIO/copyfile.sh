#!/bin/bash

echo "Criando arquivo .env ..."
touch .env
if [ ! -s .env ]
	then echo -e "matricula=\"\"\nusuario=\"\"" > .env
	echo -e "\nArquivo .env vazio. Insira as credenciais e rode o script novamente..."
	exit
fi
source .env set

matricula=$matricula
usuario=$usuario
expath="~/exerciciosGPIO"

echo -e "\n\nAcessando RaspberryPi com SSH..."
ssh -tt -i ~/.ssh/id_rsa $usuario@164.41.98.28 -p 13508 << EOF
	mkdir -p $expath -m 0777
	exit
EOF

echo -e "\n\n\nCopiando arquivos .C do diretório para a RPI..."
scp -i ~/.ssh/id_rsa  -P 13508 *.c Makefile $usuario@164.41.98.28:~/exerciciosGPIO

echo -e "\n\n\nCompilando exercícios..."
ssh -tt -i ~/.ssh/id_rsa $usuario@164.41.98.28 -p 13508 << EOF
	cd $expath
	make
	exit
EOF

#echo -e "\n\n\nAbrindo RPI..."
#ssh -i ~/.ssh/id_rsa $usuario@164.41.98.28 -p 13508