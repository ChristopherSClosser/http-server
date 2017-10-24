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
        # res = ''

        while amount_rec < amount_ex:
            data = server.recv(16)
            # res += data
            amount_rec += len(data)
            print(sys.stderr, 'received %s ' % data)

    finally:
        server.close()
    return amount_rec


if __name__ == "__main__":
    # pragma: no cover
    main(sys.argv[1])
