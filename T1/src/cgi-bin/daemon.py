# Referências: https://docs.python.org/3.6/howto/sockets.html;

import socket
import os
from threading import Thread

# Função CRC16;
# Referência http://www.feng.pucrs.br/~stemmer/processadores2/trab2-2012-2/crc.html;
def crc16(data):
    POLICRC = 0x14003  # Valor do polinomio de crc invertido em hexa;
    CRC = 0x00000  # Valor inicial do CRC16 (geralmente inicia com 0);

    # 1-Pegar um byte da mensagem;
    for byte in data:
        # 2-Fazer um XOR deste byte valor corrente do CRC;
        CRC = CRC ^ byte

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
        resultado = os.popen(cmd) -
        saida = resultado.read()

    # Comando UPTIME;
    elif (aux == 4):
        cmd = 'uptime ' + opcoes
        resultado = os.popen(cmd)
        saida = resultado.read()

    return saida
       
#Funcao que sera chamada na criacao da Thread
def conectaServidor(connectionSocket): 
	while true:
		# Recebe o pacote do webserver
		pacote = connectionSocket.recv(1024)
		
		# Se pacote vier vazio
		if pacote == '': break
		
		# Encerra a conexao
		connectionSocket.close()
  
# Define a main do programa
# Referência capítulo 2 do livro Computer Networks and the Internet
def main(): 
 
	# Estabelece a porta de conexao
	serverPort = 12000

	# Endereço IP do host
	serverHost = ''
	
	# Criando um socket TCP
	serverSocket = socket(AF_INET,SOCK_STREAM)

	# Liga o socket com um host e uma porta já conhecida
	serverSocket.bind((serverHost, serverPort))

	# Faz a ligacao com o socket e aguarda a conexao, o parametro utilizado
	# com o listen define o tamanho maximo da fila de espera de conexoes
	# no caso 1 conexao
	serverSocket.listen(1)

	while True:
		
		# Cria conexao TCP com o webserver
		connectionSocket, addr = serverSocket.accept()

		# Cria uma thread para cada porta
		thread.start_new_thread(target=conectaServidor, args=(connectionSocket, addr]))
			

# Executa a main	
main()
