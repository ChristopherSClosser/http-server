# -*- coding: utf-8 -*-

"""Simple echo server."""
import socket
import sys
import os
from datetime import datetime
LOGS = []

# 'GET resource HTTP/1.1\r\nHost: www.some.com\r\n\r\n'


def resolve_uri(uri):
    """Parse uri and return response."""
    body = ['', '']  # intialize empty list

    html_str = ""
    contents = []
    if os.path.isdir(uri):
        html_str += "<ul>"
        contents = os.listdir(uri)
        body[0] = contents

        for i in range(len(contents)):
            html_str += "<li>" + contents[i] + "</li>"

        html_str += "</ul>"

    elif os.path.isfile(uri):

        extension = os.path.splitext(uri)

        if extension[1] == ".txt":
            file = open(uri, 'r')
            html_str += "<div>" + file.read() + "</div>"
            file.close()
            body[1] = html_str
        elif extension[1] == ".png":
            file = open(uri, 'r')
            html_str += "<img>" + file.read() + "</img>"
            file.close()
            body[1] = html_str

    else:
        return 'FileNotFoundError: 404\nYou did not enter a valid file or path!'

    return body


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
        res = "HTTP/1.1 200 OK " + req_list[1]
        response_logs(res)
        return res


def response_ok(data):
    """Send an ok 200 message."""
    response = {}
    response['HTTP Version'] = "HTTP/1.1 200 OK"

    dt = datetime.now()
    response['Date:'] = dt.strftime("%a, %d. %b %y %H: %M: %S GMT")

    response['Server:'] = sys.version
    content = resolve_uri(data)
    response['Content-Length'] = (sys.getsizeof(content) // 8)
    if '<img>' in content:
        response['Content-Type:'] = 'image/html'
    elif '<div>' in content:
        response['Content-Type:'] = 'text/html'
    response['Content'] = content

    return response


def response_error():
    """Server error response."""
    return "HTTP/1.1 500 Internal Server Error"


def response_logs(data):
    """Append data to logs."""
    LOGS.append(data)
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
                # print("received %s" % data)
                if data:
                    connection.sendall(data.encode())
                else:
                    break

        except KeyboardInterrupt:
            connection.shutdown(socket.SHUT_WR)
            connection.close()
            sys.exit()


if __name__ == '__main__':
    from gevent.server import StreamServer
    from gevent.monkey import patch_all
    patch_all()
    server = StreamServer(('localhost', 8080), server_main, spawn=pool)
    server.serve_forever()
