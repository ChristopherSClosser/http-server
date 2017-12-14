"""Simple server."""
import socket
import sys
import os
from mimetypes import guess_type
from email.utils import formatdate
from re import match

LOGS = []


def resolve_uri(uri):
    """Parse uri get contents and return response."""
    script_root_path = os.path.abspath(__file__).rsplit('/', 1)[0]

    root_path = script_root_path + '/dir_for_test'

    abs_uri = os.path.abspath(root_path + uri)

    if not abs_uri.startswith(root_path):
        raise OSError('Access Denied')

    if os.path.isfile(abs_uri):

        with open(abs_uri, 'rb') as file:
            body = file.read()

        file_type = guess_type(abs_uri)[0]

        return body, file_type or 'text/plain'

    elif os.path.isdir(abs_uri):

        body = """<!DOCTYPE html>
<html>
<body>
"""
        for item in os.listdir(abs_uri):
            body += item + '\n'
        body += """</body>
</html>
"""
        return body.encode('utf8'), 'text/html'

    else:
        raise IOError('No such file or directory.')


def parse_request(req):
    """Look for a well formed get request."""
    if b'\r\nHost: ' not in req:
        raise ValueError('Host header missing from request')

    req_lines = req.split(b'\r\n')

    if len(req_lines) < 4:
        raise ValueError('Improper request length')

    if req_lines[-1] or req_lines[-2]:
        raise ValueError('Improper request formatting')

    method_uri_protocol = req_lines[0].split()

    if len(method_uri_protocol) != 3:
        raise ValueError('Improper request formatting')

    if method_uri_protocol[0] != b'GET':
        raise NotImplementedError('Server only accepts GET requests')

    if not method_uri_protocol[1].startswith(b'/'):
        raise ValueError('Improper resource path formatting')

    if method_uri_protocol[2] != b'HTTP/1.1':
        raise NotImplementedError('Server only accepts HTTP/1.1 requests')

    uri = method_uri_protocol[1]

    for header in req_lines[1:-2]:
        if header[0:1].isspace():
            raise ValueError('Improper header formatting')

        name, value = header.split(None, 1)
        if name[-1:] != b':':
            raise ValueError('Improper header formatting')

        if b'Host' in name:
            if not match('^[A-Za-z0-9_.-~]+$', value.decode('utf8')):
                raise ValueError('Improper Host formatting')

    return uri


def response_ok(body, mime_type):
    """HTTP '200 OK' response object."""
    return 'HTTP/1.1 200 OK\r\n\
Date: {date}\r\n\
Content-Type: {mime_type}\r\n\
Content-Length: {length}\r\n\
\r\n'.format(date=formatdate(usegmt=True),
             mime_type=mime_type,
             length=len(body)).encode('utf8') + body

def response_logs(data):
    """Append data to logs."""
    LOGS.append(data)
    return LOGS


def response_error(code, phrase):
    """HTTP '500 Internal Server Error' response."""
    return 'HTTP/1.1 {code} {phrase}\r\n\
Date: {date}\r\n\
\r\n'.format(code=code,
             phrase=phrase,
             date=formatdate(usegmt=True)).encode('utf8')


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

            print(request.decode('utf8'))

            try:
                uri = parse_request(request)
                uri = uri if isinstance(uri, str) else uri.decode('utf8')
                response = response_ok(*resolve_uri(uri))

            except ValueError:
                response = response_error(400, 'Bad Request')

            except NotImplementedError as error:
                if 'GET' in error.args[0]:
                    response = response_error(405, 'Method Not Allowed')
                else:
                    response = response_error(501, 'Not Implmented')

            except (OSError, IOError) as error:
                response = response_error(404, 'Not Found')

            conn.sendall(response)
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
