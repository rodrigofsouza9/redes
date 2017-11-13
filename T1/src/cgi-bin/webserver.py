#!/usr/bin/env python
# -*- coding: utf-8 -*-
# WEBSERVER.PY
# Referencias: http://www.tutorialspoint.com/python/python_cgi_programming.htm

# Import modules for CGI handling
import cgi, cgitb
import subprocess
import socket
import os
import sys
import thread
import binascii

# Ativa o cgi
cgitb.enable()

# Função CRC16;
# Referência http://www.feng.pucrs.br/~stemmer/processadores2/trab2-2012-2/crc.html;
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
    	headerckecksum = "{:016b}".format(Header_Checksum)
    	sourceaddress = "{:032b}".format(Source_Address)
    	destinationaddress = "{:032b}".format(Destination_Address)
    	opcoes = ''

    	Options.strip()
    	for c in Options:
        	opcoes += "{:08b}".format(ord(c))

    	soma = versao + ihl + typeofservice + totallenght + identification + flags + fragmentoffset + timetolive + protocol + sourceaddress + destinationaddress + opcoes;

    	headerchecksum = "{:016b}".format(crc16(soma));
   
	novoCabecalho = versao + ihl + typeofservice + totallenght + identification + flags + fragmentoffset + timetolive + protocol + headerchecksum + sourceaddress + destinationaddress + opcoes	

    	return novoCabecalho
		
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
        	if '|' in Options or ';' in Options or '>' in Options:
            		cabecalho['Options'] = ''
        	else:
            		cabecalho['Options'] = Options
    	else:
        	cabecalho['Options'] = ''

    	return cabecalho

def maquina1(form, host, port, saida_maq1):
	# Valores padroes de cabecalho dos pacotes
    	# Version recebe 2
    	Version = 2
    	# IHL recebe 5 que eh o seu valor padrao
    	IHL = 5
    	# Type of service recebe 0
    	Type_of_Service = 0
    	# Tamanho do pacote
    	Total_Length = 24
    	Identification = 1
    	# Flags recebe o 0
    	Flags = 0x000
    	# Fragment_Offset recebe 0
    	Fragment_Offset = 0
    	# TTL recebe 127 que eh o padrao(128 -1)
    	Time_to_Live = 127
    	Header_Checksum = 0
    	# o ip 192.168.56.101 convertido para int equivale a 3232249957
    	# Source_address recebe o endereco ip 192.168.56.101 do html
    	Source_Address = 3232249957
    	# Destination_Address recebe o endereco ip 127.0.0.1 que equivale ao inteiro
    	# 2130706433
    	Destination_Address = 2130706433
    	Options = ''

    	if form.getvalue('maq1_ps'):

        	Protocol = 1;
        	saida_maq1 += 'Comando PS<br><br>'

        	pacoteEnvio = recriaCabecalho(Version, IHL, Type_of_Service, Total_Length, Identification, Flags, Fragment_Offset, Time_to_Live, Protocol, Header_Checksum, Source_Address, Destination_Address, Options)

        	# Cria um socket TCP
        	serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        	# Conecta socket
        	serverSocket.connect((host, port))

        	# Envia pacote criado
        	serverSocket.send(pacoteEnvio)

        	# Recebe pacote resposta
        	pacoteResposta = serverSocket.recv(1024)

        	pacoteResposta = descompactaPacote(pacoteResposta)
        	pacoteEnvio = descompactaPacote(pacoteEnvio)

        	# Verifica parâmetro Time_to_Live
        	if (int(pacoteEnvio['Time_to_Live'], 2) != (int(pacoteResposta['Time_to_Live'], 2) + 1)):
            		return "Erro no parâmetro Time_to_live<br><br>"

        	# Verifica parâmetro Identification
        	elif (int(pacoteEnvio['Identification'], 2) != (int(pacoteResposta['Identification'], 2) - 1)):
            		return "Erro no parâmetro Identification<br><br>"

        	# Verifica parâmetro Flags
        	elif (pacoteResposta['flags'] != '111'):
            		return "Erro no parâmetro Flags<br><br>"

        	checksum = pacoteResposta['Header_Checksum']

        	headerchecksum = crc16(pacoteResposta['Version'] + pacoteResposta['IHL'] + pacoteResposta['Type_of_Service'] + pacoteResposta['Total_Length'] + pacoteResposta['Identification'] + pacoteResposta['Flags'] + pacoteResposta['Fragment_Offset'] + pacoteResposta['Time_to_Live'] + pacoteResposta['Protocol'] + pacoteResposta['Source_Address'] + pacoteResposta['Destination_Address'])

        	# Verifica parâmetro Header_Checksum
        	if (headerchecksum != checksum):
            		return "Erro no parâmetro Header_Checksum<br><br>"

        	# Encerra socket
        	serverSocket.close()

        	return (saida_maq1)

	if form.getvalue('maq1_df'):
        	Protocol = 2;
        	saida_maq1 += 'Comando DF<br><br>'

        	pacoteEnvio = recriaCabecalho(Version, IHL, Type_of_Service, Total_Length, Identification, Flags, Fragment_Offset, Time_to_Live, Protocol, Header_Checksum, Source_Address, Destination_Address, Options)

        	# Cria um socket TCP
        	serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        	# Conecta socket
        	serverSocket.connect((host, port))

        	# Envia pacote criado
        	serverSocket.send(pacoteEnvio)

        	# Recebe pacote resposta
        	pacoteResposta = serverSocket.recv(1024)

        	pacoteResposta = descompactaPacote(pacoteResposta)
        	pacoteEnvio = descompactaPacote(pacoteEnvio)

        	# Verifica parâmetro Time_to_Live
       	 	if (int(pacoteEnvio['Time_to_Live'], 2) != (int(pacoteResposta['Time_to_Live'], 2) + 1)):
            		return "Erro no parâmetro Time_to_live<br><br>"

        	# Verifica parâmetro Identification
        	elif (int(pacoteEnvio['Identification'], 2) != (int(pacoteResposta['Identification'], 2) - 1)):
            		return "Erro no parâmetro Identification<br><br>"

        	# Verifica parâmetro Flags
        	elif (pacoteResposta['flags'] != '111'):
            		return "Erro no parâmetro Flags<br><br>"

        	checksum = pacoteResposta['Header_Checksum']

        	headerchecksum = crc16(pacoteResposta['Version'] + pacoteResposta['IHL'] + pacoteResposta['Type_of_Service'] + pacoteResposta['Total_Length'] + pacoteResposta['Identification'] + pacoteResposta['Flags'] + pacoteResposta['Fragment_Offset'] + pacoteResposta['Time_to_Live'] + pacoteResposta['Protocol'] + pacoteResposta['Source_Address'] + pacoteResposta['Destination_Address'])

        	# Verifica parâmetro Header_Checksum
        	if (headerchecksum != checksum):
            		return "Erro no parâmetro Header_Checksum<br><br>"

        	# Encerra socket
        	serverSocket.close()

        	return (saida_maq1)

	if form.getvalue('maq1_finger'):
        	Protocol = 3;
        	saida_maq1 += 'Comando FINGER<br><br>'

       	 	pacoteEnvio = recriaCabecalho(Version, IHL, Type_of_Service, Total_Length, Identification, Flags, Fragment_Offset, Time_to_Live, Protocol, Header_Checksum, Source_Address, Destination_Address, Options)

        	# Cria um socket TCP
        	serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        	# Conecta socket
        	serverSocket.connect((host, port))

        	# Envia pacote criado
        	serverSocket.send(pacoteEnvio)

        	# Recebe pacote resposta
        	pacoteResposta = serverSocket.recv(1024)

        	pacoteResposta = descompactaPacote(pacoteResposta)
        	pacoteEnvio = descompactaPacote(pacoteEnvio)

        	# Verifica parâmetro Identification
        	if (int(pacoteEnvio['Identification'], 2) != (int(pacoteResposta['Identification'], 2) - 1)):
            		return "Erro no parâmetro Identification<br><br>"

            	# Verifica parâmetro Flags
        	elif (pacoteResposta['flags'] != '111'):
            		return "Erro no parâmetro Flags<br><br>"

        	# Verifica parâmetro Time_to_Live
        	elif (int(pacoteEnvio['Time_to_Live'], 2) != (int(pacoteResposta['Time_to_Live'], 2) + 1)):
            		return "Erro no parâmetro Time_to_live<br><br>"

        	checksum = pacoteResposta['Header_Checksum']

        	headerchecksum = crc16(pacoteResposta['Version'] + pacoteResposta['IHL'] + pacoteResposta['Type_of_Service'] + pacoteResposta['Total_Length'] + pacoteResposta['Identification'] + pacoteResposta['Flags'] + pacoteResposta['Fragment_Offset'] + pacoteResposta['Time_to_Live'] + pacoteResposta['Protocol'] + pacoteResposta['Source_Address'] + pacoteResposta['Destination_Address'])

        	# Verifica parâmetro Header_Checksum
        	if (headerchecksum != checksum):
            		return "Erro no parâmetro Header_Checksum<br><br>"

        	# Encerra socket
        	serverSocket.close()

        	return (saida_maq1)

	if form.getvalue('maq1_uptime'):
        	Protocol = 4;
        	saida_maq1 += 'Comando UPTIME<br><br>'

        	pacoteEnvio = recriaCabecalho(Version, IHL, Type_of_Service, Total_Length, Identification, Flags, Fragment_Offset, Time_to_Live, Protocol, Header_Checksum, Source_Address, Destination_Address, Options)

        	# Cria um socket TCP
        	serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        	# Conecta socket
        	serverSocket.connect((host, port))

        	# Envia pacote criado
       	 	serverSocket.send(pacoteEnvio)

        	# Recebe pacote resposta
        	pacoteResposta = serverSocket.recv(1024)

        	pacoteResposta = descompactaPacote(pacoteResposta)
        	pacoteEnvio = descompactaPacote(pacoteEnvio)

        	# Verifica parâmetro Time_to_Live
        	if (int(pacoteEnvio['Time_to_Live'], 2) != (int(pacoteResposta['Time_to_Live'], 2) + 1)):
        		return "Erro no parâmetro Time_to_live<br><br>"

        	# Verifica parâmetro Identification
        	elif (int(pacoteEnvio['Identification'], 2) != (int(pacoteResposta['Identification'], 2) - 1)):
        		return "Erro no parâmetro Identification<br><br>"

        	# Verifica parâmetro Flags
        	elif (pacoteResposta['flags'] != '111'):
        		return "Erro no parâmetro Flags<br><br>"

        	checksum = pacoteResposta['Header_Checksum']

       	 	headerchecksum = crc16(pacoteResposta['Version'] + pacoteResposta['IHL'] + pacoteResposta['Type_of_Service'] + pacoteResposta['Total_Length'] + pacoteResposta['Identification'] + pacoteResposta['Flags'] + pacoteResposta['Fragment_Offset'] + pacoteResposta['Time_to_Live'] + pacoteResposta['Protocol'] + pacoteResposta['Source_Address'] + pacoteResposta['Destination_Address'])

        	# Verifica parâmetro Header_Checksum
        	if (headerchecksum != checksum):
        		return "Erro no parâmetro Header_Checksum<br><br>"

        	# Encerra socket
        	serverSocket.close()

        	return (saida_maq1)

def main():
    	cgitb.enable()

    	# Cabecalho padrao do html
    	print("Content-type:text/html\r\n\r\n")
    	print('<html>')
    	print('<head>')
    	print('<title>Trabalho 1 de Redes</title>')
   	print('</head>')
    	print('<body>')

    	# Cria instância de FieldStorage
    	form = cgi.FieldStorage()

    	# Endereço de origem
    	host = '127.0.0.1'

    	saida_maq1 = 'Maquina 1<br><br>'
    	saida_maq2 = 'Maquina 2<br><br>'
    	saida_maq3 = 'Maquina 3<br><br>'

    	print(maquina1(form, host, 9001, saida_maq1))

    	print("</body>")
	print("</html>")

main()
