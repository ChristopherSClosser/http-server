"""Simple echo server."""
# -*- coding: utf-8 -*-

import socket
import sys
LOGS = []


def response_ok():
    """Send an ok 200 message."""
    return "HTTP/1.1 200 OK"


def response_error():
    """Server error response."""
    return "HTTP/1.1 500 Internal Server Error"


def response_logs(data):
    """Append data to logs."""
    LOGS.append(data)
    response_ok()
    return LOGS


def server_main():
    """Main server."""
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
                    print("sending data back to the client")
                    connection.sendall(data.encode())
                else:
                    print("no more data from", client_address)
                    break

        except KeyboardInterrupt:
            connection.shutdown(socket.SHUT_WR)
            connection.close()
            sys.exit()


if __name__ == '__main__':
    server_main()
