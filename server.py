"""Simple echo server."""
import socket
import sys
LOGS = []

# 'GET resource HTTP/1.1\r\n www.some.com\r\n\r\n'


def parse_request(request):
    """Look for a well formed get request."""
    if "GET" not in request:
        return "400 BAD REQUEST"
    elif "HTTP/1.1" not in request:
        return "412 PRECONDITION FAILED - HTTP v. 1.1 required"
    elif "Host" not in request:
        return "412 PRECONDITION FAILED - Host required"
    else:
        req_list = request.split()
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
                    connection.sendall(data.encode("utf8"))
                    response_logs(data)
                else:
                    response_error()
                    print(sys.stderr, "no more data from", client_address)
                    break

        finally:
            connection.close()


if __name__ == '__main__':
    server_main()
