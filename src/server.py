<<<<<<< HEAD
# -*- coding: utf-8 -*-
"""Simple echo server."""

import socket
import sys
LOGS = []


def parse_request(request):
    """Look for a well formed get request."""
    req_list = request.split()

    if "GET" not in req_list[0]:
        return "400 BAD REQUEST"
    elif "HTTP/1.1" not in req_list[2]:
        return "412 PRECONDITION FAILED - HTTP v. 1.1 required"
    elif "Host" not in req_list[3]:
        return "412 PRECONDITION FAILED - Host required"
    else:
        res = response_ok() + ' ' + req_list[1]
        response_logs(res)
        return res


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
=======
"""Simple echo server."""
# -*- coding: utf-8 -*-

import socket
import sys
>>>>>>> master


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
<<<<<<< HEAD
                    print("sending data back to the client")
=======
                    print(sys.stderr, "sending data back to the client")
>>>>>>> master
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
