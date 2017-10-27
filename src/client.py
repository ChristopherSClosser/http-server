"""Echo client."""

import sys
import socket


def main(message):
    """Main method for send client message."""
    server_address = ('localhost', 8080)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect(server_address)

    try:
        server.sendall(message.encode('utf8'))

        amount_rec = 0
        amount_ex = len(message)
        data = ''

        while amount_rec < amount_ex:
            data += server.recv(16).decode('utf8')
            # res += data
            amount_rec += len(data)
        print('received: %s ' % data)

    finally:
        server.close()
    return data


if __name__ == "__main__":
    # pragma: no cover
    main(sys.argv[1])
