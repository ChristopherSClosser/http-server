"""Simple echo server."""
import socket
import sys


server_address = ('localhost', 8080)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('server is: ', server, '\nserver_address: ', server_address)
server.bind(server_address)

server.listen(1)

while True:
    print(sys.stderr, "waiting for a connection")
    connection, client_address = server.accept()

    try:
        print(sys.stderr, "connection from", client_address)

        while True:
            data = connection.recv(16)
            print(sys.stderr, "received %s" %data)
            if data:
                print(sys.stderr, "sending data back to the client")
                connection.sendall(data)
            else:
                print(sys.stderr, "no more data from", client_address)
                break

    finally:
        connection.close()
