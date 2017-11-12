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

    	print("</body>")
	print("</html>")

main()
