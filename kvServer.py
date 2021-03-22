import argparse
import socket

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)
BUFFER_SIZE = 16

# arg parsing
parser = argparse.ArgumentParser(description="Process arguments for data creation")
parser.add_argument('-a', type=str, help="ip address", default=HOST)
parser.add_argument('-p', type=int, help="port", default=PORT)
args = parser.parse_args()


def delete():
    print('Not implemented yet')


def put():
    print('Not implemented yet')


def get():
    print('Not implemented yet')


def query():
    print('Not implemented yet')


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

        print('Listening on ' + args.a + ':' + str(args.p))
        s.bind((args.a, args.p))
        s.listen()

        while True:
            conn, addr = s.accept()
            with conn:
                print('Connected by', addr)

                while True:

                    request = conn.recv(BUFFER_SIZE)
                    data = request
                    method = data.decode().split(" ")[0]
                    while len(data) == BUFFER_SIZE:
                        data = conn.recv(BUFFER_SIZE)
                        request = request + data

                    if method == "PUT":
                        put()
                    elif method == "GET":
                        get()
                    elif method == "QUERY":
                        query()
                    elif method == "DELETE":
                        delete()

                    s.sendall("OK".encode())

                    break


if __name__ == "__main__":
    main()
