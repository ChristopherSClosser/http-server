"""Concurrent server."""

import sys
import socket
from gevent.server import StreamServer
from gevent.monkey import patch_all
from server import resolve_uri, response_error, response_ok, parse_request


def server():
    """server to continue serving."""
    try:
        patch_all()
        server = StreamServer(('127.0.0.1', 8000), send_response)
        print('Serving on 8000')
        server.serve_forever()

    except KeyboardInterrupt:
        server.close()
        print('closed server')
        sys.exit()


def send_response(conn, addr):
    """Send response to client."""
    conn.settimeout(2)
    req = b''
    try:
        packet = conn.recv(8)
        req = packet
        while b'\r\n\r\n' not in req:
            packet = conn.recv(8)
            req += packet
    except socket.timeout:
        pass

    print(req.decode('utf8'))

    try:
        uri = parse_request(req)
        uri = uri if isinstance(uri, str) else uri.decode('utf8')
        res = response_ok(*resolve_uri(uri))

    except ValueError:
        res = response_error(400, 'Bad Request')

    except NotImplementedError as error:
        if 'GET' in error.args[0]:
            res = response_error(405, 'Method Not Allowed')
        else:
            res = response_error(501, 'Not Implmented')

    except (OSError, IOError) as error:
        res = response_error(404, 'Not Found')

    conn.sendall(res)
    conn.close()

if __name__ == "__main__":  # pragma: no cover
    server()
