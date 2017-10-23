"""Simple echo server."""
import socket
import sys


server_address = ('localhost', 8080)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('server is: ', server, '\nserver_address: ', server_address)
