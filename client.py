"""Echo client."""

import sys
import socket

server_address = ('localhost', 8080)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print(sys.stderr, 'Connecting to port: %s' % server_address)
server.connect(server_address)


try:
    message = 'A message'
    server.sendall(message)

    amount_rec = 0
    amount_ex = len(message)

    while amount_rec < amount_ex:
        data = server.recv(16)
        amount_rec += len(data)
        print(sys.stderr, 'received %s ' % data)

finally:
    server.close()
