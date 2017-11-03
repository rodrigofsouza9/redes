# Referências: https://docs.python.org/3.6/howto/sockets.html;

import socket
from threading import Thread
       
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
