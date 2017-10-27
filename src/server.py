"""Simple echo server."""
import socket
import sys


server_address = ('localhost', 8080)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
print('server_address: {}'.format(server_address))
server.bind(server_address)

server.listen(1)

while True:
    print("waiting for a connection\n")
    connection, client_address = server.accept()

    try:
        print("connection from", client_address)

        while True:
            data = connection.recv(16).decode('utf8')
            print(sys.stderr, "received %s" % data)
            if data:
                print(sys.stderr, "sending data back to the client")
                connection.sendall(data)
            else:
                print("no more data from", client_address)
                break

    except KeyboardInterrupt:
        connection.shutdown(socket.SHUT_WR)
        connection.close()
        sys.exit()
