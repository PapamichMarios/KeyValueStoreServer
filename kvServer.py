import argparse
import socket

from trie import Trie

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)
BUFFER_SIZE = 1024

# arg parsing
parser = argparse.ArgumentParser(description="Process arguments for data creation")
parser.add_argument('-a', type=str, help="ip address", default=HOST)
parser.add_argument('-p', type=int, help="port", default=PORT)
args = parser.parse_args()


def main():

    # init Trie
    trie = Trie()

    # listen for connections
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

        print('Listening on ' + args.a + ':' + str(args.p))
        s.bind((args.a, args.p))
        s.listen()

        while True:
            conn, addr = s.accept()
            with conn:

                while True:
                    # receive request size
                    request_size = conn.recv(BUFFER_SIZE)
                    if not request_size:
                        break

                    # ack for request size
                    conn.sendall("OK".encode())

                    # read data from request
                    request = conn.recv(BUFFER_SIZE)
                    method = request.decode().split(" ")[0]
                    while len(request) < int(request_size):
                        data = conn.recv(BUFFER_SIZE)
                        request = request + data

                    # process request
                    if method == "PUT":
                        trie.put()
                    elif method == "GET":
                        trie.get()
                    elif method == "QUERY":
                        trie.query()
                    elif method == "DELETE":
                        trie.delete()

                    # send ok
                    print('Received: ' + request)
                    conn.sendall("OK".encode())


if __name__ == "__main__":
    main()
