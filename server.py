"""Simple echo server."""
import socket
import sys


def response_ok():
    
    resp_msg = "HTTP/1.1 200 OK\n"
    '''
    try:
        while True:
            resp_socket, resp_address = servSock.accept()
            resp_socket.sendall(resp_msg.encode('utf8'))
    except:
        print("Invalid Response")
    finally:
         resp_socket.close()
         '''
    return resp_msg


def server_main():
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
                    print(sys.stderr, "sending data back to the client")
                    #connection.sendall(data)
                    connection.sendall(bytes(data, 'utf-8'))
                    response_ok()
                else:
                    print(sys.stderr, "no more data from", client_address)
                    break

        finally:
            connection.close()

if __name__ == '__main__':
    server_main()
