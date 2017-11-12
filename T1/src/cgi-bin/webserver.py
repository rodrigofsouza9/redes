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
