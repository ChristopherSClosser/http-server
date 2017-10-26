# -*- coding: utf-8 -*-

"""Simple echo server."""
import socket
import sys
import os
LOGS = []

# 'GET resource HTTP/1.1\r\nHost: www.some.com\r\n\r\n'


def resolve_uri(URI):
    # body = ((),) #intialize empty tuple

    html_str = ""
    contents = []
  
    if os.path.isdir(URI):
        html_str += "<ul>"
        contents = os.listdir(URI)

        for i in range(len(contents)):
            html_str += "<li>" + contents[i] + "</li>"
            html_str += "</ul>"

    elif os.path.isfile(URI):
        file = open(URI, “r”) 
        html_str += "<div>"
        for i in file:
            html_str += i
        html_str +=  "</div>"

    return contents

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
    return LOGS


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
                    connection.sendall(data)
                    response_logs(data)
                else:
                    response_error()
                    print(sys.stderr, "no more data from", client_address)
                    break
            connection.close()
            sys.exit(1)

        finally:
            connection.close()
            sys.exit(1)


if __name__ == '__main__':
    server_main()
