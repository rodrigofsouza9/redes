#!/usr/bin/env python
# -*- coding: utf-8 -*-
# DAEMON.PY
# Referências: https://docs.python.org/3.6/howto/sockets.html;

import socket
import os
import sys
import thread

# Função CRC16;
# Referência: http://www.feng.pucrs.br/~stemmer/processadores2/trab2-2012-2/crc.html;
def crc16(data):
	POLICRC = 0x14003  # Valor do polinomio de crc invertido em hexa;
	CRC = 0x00000  # Valor inicial do CRC16 (geralmente inicia com 0);

    	# 1-Pegar um byte da mensagem;
    	for byte in data:
        	# 2-Fazer um XOR deste byte valor corrente do CRC;
        	CRC = CRC ^ int(byte)

        	# 3-Repetir 8 vezes:
        	for i in range(8):
            		# 3.1-Se o bit mais da direita CRC atual for 1,fazer XOR com o polinômio de CRC refletido;
            		if (CRC & 1):
                		CRC = CRC ^ POLICRC
            		# 3.2Deslocar o valor corrente CRC 1 bit para a direita;
            		CRC = CRC >> 1

    	return CRC

# Função que transforma os bits de opções em uma string;
# Referência https://stackoverflow.com/questions/10237926/convert-string-to-list-of-bits-and-viceversa;
def BitsToString(opcoes):
	saida = ''
	tam = int(len(opcoes) / 8)
    	for b in range(tam):
        	byte = opcoes[b * 8:(b + 1) * 8]
        	saida = saida + chr(int(byte, 2))

    	return saida

# Função que executa o comando;
# Padrão definido na documentação do projeto;
# Retorna resultado da execução;
def executaComando(comando, opcoes):
	aux = int(comando, 2)

    	# Comando PS;
   	if (aux == 1):
        	cmd = 'ps ' + opcoes
        	resultado = os.popen(cmd)
        	saida = resultado.read()

    	# Comando DF;
    	elif (aux == 2):
        	cmd = 'df ' + opcoes
        	resultado = os.popen(cmd)
        	saida = resultado.read()

    	# Comando FINGER;
    	elif (aux == 3):
        	cmd = 'finger ' + opcoes
        	resultado = os.popen(cmd)
        	saida = resultado.read()

    	# Comando UPTIME;
    	elif (aux == 4):
        	cmd = 'uptime ' + opcoes
        	resultado = os.popen(cmd)
        	saida = resultado.read()

    	return saida


# Função que descompacta o pacote;
# Padrão de cabeçalho estabelecido na descrição do projeto;
def descompactaPacote(pacote):    	
	cabecalho = {}
	cabecalho['Version'] = pacote[0:4]
    	cabecalho['IHL'] = pacote[4:8]
    	cabecalho['Type_of_Service'] = pacote[8:16]
    	cabecalho['Total_Length'] = pacote[16:32]
    	cabecalho['Identification'] = pacote[32:48]
    	cabecalho['Flags'] = pacote[48:51]
    	cabecalho['Fragment_Offset'] = pacote[51:64]
    	cabecalho['Time_to_Live'] = pacote[64:72]
    	cabecalho['Protocol'] = pacote[72:80]
    	cabecalho['Header_Checksum'] = pacote[80:96]
    	cabecalho['Source_Address'] = pacote[96:128]
    	cabecalho['Destination_Address'] = pacote[128:160]

    	# Chama função que transforma bits em uma string
    	Options = pacote[160:len(pacote) - 8]
    	Options = BitsToString(Options)

    	# Verifica se campo opções possui argumentos
    	# Verifica se argumentos são malicosos
    	# Elimina argumentos maliciosos
    	if (Options):
        	if ('|' in Options or ';' in Options or '>' in Options):
            		cabecalho['Options'] = ''
        	else:
            		cabecalho['Options'] = Options
    	else:
        	cabecalho['Options'] = ''

    	return cabecalho

# Função que recria um cabecalho para o pacote resposta
def recriaCabecalho(Version, IHL, Type_of_Service, Total_Length, Identification, Flags, Fragment_Offset, Time_to_Live, Protocol, Header_Checksum, Source_Address, Destination_Address, Options):
	versao = "{:04b}".format(Version)
    	ihl = "{:04b}".format(IHL)
    	typeofservice = "{:08b}".format(Type_of_Service)
    	totallenght = "{:016b}".format(Total_Length)
    	identification = "{:016b}".format(Identification)
    	flags = "{:03b}".format(Flags)
    	fragmentoffset = "{:013b}".format(Fragment_Offset)
    	timetolive = "{:08b}".format(Time_to_Live)
    	protocol = "{:08b}".format(Protocol)
    	headerchecksum = "{:016b}".format(Header_Checksum)
    	sourceaddress = "{:032b}".format(Source_Address)
    	destinationaddress = "{:032b}".format(Destination_Address)
    	opcoes = ''
	Options.strip()
    	for c in Options:
        	opcoes += "{:08b}".format(ord(c))

    	novoCabecalho = versao + ihl + typeofservice + totallenght + identification + flags + fragmentoffset + timetolive + protocol + headerchecksum + sourceaddress + destinationaddress + opcoes

    	return novoCabecalho


#Funcao que sera chamada na criacao da Thread
def conectaServidor(connectionSocket): 
	while 1:
        	# Recebe o pacote do webserver
        	pacote = connectionSocket.recv(1024)

        	# Se pacote vier vazio
        	if pacote == '': break

        	# Descompacta o pacote recebido
        	pacoteRecebido = descompactaPacote(pacote)

        	# Altera os dados para o pacote resposta
        	# Valores padroes definidos conforme a seguinte referencia :http://www.erg.abdn.ac.uk/users/gorry/course/inet-pages/ip-packet.html
        	# Valores tambem colocados como solicitados pelo projeto
        	# Version recebe 2

        	resposta = {}

        	resposta['Version'] = 2
        	# IHL recebe 5 que eh o seu valor padrao
        	resposta['IHL'] = 5
        	# Type of service recebe 0
        	resposta['Type_of_Service'] = 0
        	# Total_Length recebe 0 pra ser calculado com o tamanho do pacote
        	resposta['Total_Length'] = 0
        	# Identification recebe a sua sequencia
        	resposta['Identification'] = (int(pacoteRecebido['Identification']) + 1)
        	# Flags recebe o 7 (111)
        	resposta['Flags'] = 7
        	# Fragment_Offset recebe 0
        	resposta['Fragment_Offset'] = 0
        	# Decrementa o TTL
        	resposta['Time_to_Live'] = int(pacoteRecebido['Time_to_Live']) - 1
        	# Header_Checksum recebe 0
        	resposta['Header_Checksum'] = 0
        	# Source_address recebe o Destination_Address que chegou
        	resposta['Source_Address'] = int(pacoteRecebido['Destination_Address'])
        	# Destination_Address recebe o source_address que chegou
        	resposta['Destination_Address'] = int(pacoteRecebido['Source_Address'])
        	# Campo de Options
        	resposta['Options'] = BitsToString(pacoteRecebido['Options'])

        	# Atualiza valor do total length com o comprimento do pacote
        	resposta['Total_Length'] = int(len(pacoteRecebido))
			
		headerchecksum = crc16(pacoteRecebido['Version'] + pacoteRecebido['IHL'] + pacoteRecebido['Type_of_Service'] + pacoteRecebido['Total_Length'] + pacoteRecebido['Identification'] + pacoteRecebido['Flags'] + pacoteRecebido['Fragment_Offset'] + pacoteRecebido['Time_to_Live'] + pacoteRecebido['Protocol'] + pacoteRecebido['Source_Address'] + pacoteRecebido['Destination_Address'])

        	# Compara o crc calculado com o recebido no header
        	if headerchecksum != pacoteRecebido['Header_Checksum']:
            		return 'HeaderChecksum diferente'

        	if pacoteRecebido['Flags'] != 0x000:
           		return 'Flag incompátivel'

        	if pacoteRecebido['Version'] != 0x0010:
            		return 'Erro de versão'

        	# Armazena a saida conforme o comando executado
        	comando = executaComando(pacoteRecebido['Protocol'], pacoteRecebido['Options'])

        	# Cria o pacote resposta concatenando todos os valores do cabecalho
        	pacoteResposta = recriaCabecalho(resposta['Version'], resposta['IHL'], resposta['Type_of_Service'], resposta['Total_Length'], resposta['Identification'], resposta['Flags'], resposta['Fragment_Offset'], resposta['Time_to_Live'], comando, resposta['Header_Checksum'], resposta['Source_Address'], resposta['Destination_Address'], resposta['Options'])

        	# Envia o pacote resposta pelo socket
        	connectionSocket.sendall(pacoteResposta.bin.encode())

    	# Encerra a conexao
    	connectionSocket.close()


# Define a main do programa
# Referência capítulo 2 do livro Computer Networks and the Internet
def main():
	# Endereço IP do host
    	host = '127.0.0.1'

    	# Estabelece a porta de conexao passando como argumento pelo terminal
    	port = int(sys.argv[1])

    	# Cria um socket TCP
    	serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    	# Liga o socket com um host e uma porta já conhecida
    	serverSocket.bind((host, port))

    	# Faz a ligacao com o socket e aguarda a conexao, o parametro utilizado
    	# com o listen define o tamanho maximo da fila de espera de conexoes
    	# no caso 3 conexoes
    	serverSocket.listen(3)

    	while 1:
        	# Cria conexao TCP com o webserver
        	connectionSocket, addr = serverSocket.accept()
        	print('Connection address:', addr)

        	# Cria uma thread para cada porta
        	thread.start_new_thread(conectaServidor, (connectionSocket,))


main()
