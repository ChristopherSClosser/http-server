"""Simple echo server."""
import socket
import sys


def response_ok():
    """Send an ok 200 message."""
    return "HTTP/1.1 200 OK"


def resonse_error():
    """Server error response."""
    return "HTTP/1.1 500 Internal Server Error"


def server_main():
    """Main server function."""
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
                data = connection.recv(16).decode('utf8')
                print(sys.stderr, "received %s" % data)
                if data:
                    response_ok()
                    print(sys.stderr, "sending data back to the client")
                    connection.sendall(data.encode("utf8"))
                else:
                    resonse_error()
                    print(sys.stderr, "no more data from", client_address)
                    break

        finally:
            connection.close()


if __name__ == '__main__':
    server_main()
