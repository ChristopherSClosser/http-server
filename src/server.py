"""Simple server."""

import socket
import sys
from email.utils import formatdate
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
        res = response_ok(), ' ', req_list[1]
        response_logs(res)
        return res


def response_logs(data):
    """Append data to logs."""
    LOGS.append(data)
    response_ok()
    return LOGS


def response_ok():
    """HTTP '200 OK' response."""
    return 'HTTP/1.1 200 OK\r\n\
Date: {}\r\n\
\r\n'.format(formatdate(usegmt=True)).encode('utf8')


def response_error():
    """HTTP '500 Internal Server Error' response."""
    return 'HTTP/1.1 500 Internal Server Error\r\n\
Date: {}\r\n\
\r\n'.format(formatdate(usegmt=True)).encode('utf8')


def server():
    """Start a new server until user presses control D."""
    try:
        s = socket.socket(socket.AF_INET,
                          socket.SOCK_STREAM,
                          socket.IPPROTO_TCP)
        s.bind(('127.0.0.1', 8000))
        s.listen(1)
        print('Server started')
        while True:
            conn, addr = s.accept()
            conn.settimeout(2)

            request = b''
            try:
                packet = conn.recv(8)
                request = packet
                while b'\r\n\r\n' not in request:
                    packet = conn.recv(8)
                    request += packet
            except socket.timeout:
                pass

            print(request[:-4].decode('utf8'))
            conn.sendall(response_ok())
            conn.close()

    except KeyboardInterrupt:
        if 'conn' in locals():
            conn.close()
            print('Connection closed')
        s.close()
        print('Server closed')
        sys.exit()


if __name__ == "__main__":
    server()
