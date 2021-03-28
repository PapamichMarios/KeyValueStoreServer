import argparse
import json
import socket

from trie import Trie

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)
BUFFER_SIZE = 1024

# methods
PUT = "PUT"
QUERY = "QUERY"
GET = "GET"
DELETE = "DELETE"

# messages
OK = "OK"
ERROR = "ERROR"
SUCCESS = "SUCCESS"
NOT_FOUND = "NOT FOUND"

# arg parsing
parser = argparse.ArgumentParser(description="Process arguments for data creation")
parser.add_argument('-a', type=str, help="ip address", default=HOST)
parser.add_argument('-p', type=int, help="port", default=PORT)
args = parser.parse_args()


def log(code: str, request: str):
    print(code + ": " + request)


def get(conn: socket, request: str, trie: Trie):
    get_request = request
    key = get_request[len(GET):].strip()

    value = trie.get(key=key)
    if not value:
        log(code=NOT_FOUND, request=request)
        conn.sendall(NOT_FOUND.encode())
        return

    value = json.dumps(value).replace(",", ";")
    log(code=SUCCESS, request=request)
    conn.sendall(("\"" + key + "\": " + value).encode())


def put(conn: socket, request: str, trie: Trie):
    try:
        put_request = request
        put_request = put_request.replace(';', ',')
        put_request = "{" + put_request[len(PUT):] + "}"
        put_request = json.loads(put_request)

        key = list(put_request.keys())[0]

        # check if already exists
        value = trie.get(key=key)
        if value:
            log(code=ERROR, request=request)
            conn.sendall(ERROR.encode())
            return

        trie.put(key=key, value=put_request[key])

        # send ok
        log(code=SUCCESS, request=request)
        conn.sendall(OK.encode())

    except:
        log(code=ERROR, request=request)
        conn.sendall(ERROR.encode())


def query(conn: socket, request: str, trie: Trie):
    query_request = request
    keys = query_request[len(QUERY):].strip()
    key = keys.split(".")[0]
    subkeys = keys.split(".")[1:]

    # get the top level key
    value = trie.get(key=key)
    if not value:
        log(code=NOT_FOUND, request=request)
        conn.sendall(NOT_FOUND.encode())
        return

    # if user only gave first level key return it
    if len(keys.split(".")) == 1:
        value = json.dumps(value).replace(",", ";")
        log(code=SUCCESS, request=request)
        conn.sendall(("\"" + keys + "\": " + value).encode())
        return

    result = trie.query(value=value, subkeys=subkeys, level=0)
    if not result:
        log(code=NOT_FOUND, request=request)
        conn.sendall(NOT_FOUND.encode())
        return

    # to string for print method based on return type
    log(code=SUCCESS, request=request)
    conn.sendall(("\"" + keys + "\": " + result).encode())


def delete(conn: socket, request: str, trie: Trie):
    delete_request = request
    key = delete_request[len(DELETE):].strip()

    # check if top level key exists
    value = trie.get(key=key)
    if not value:
        log(code=NOT_FOUND, request=request)
        conn.sendall(NOT_FOUND.encode())
        return

    trie.delete(key=key)

    log(code=DELETE, request=request)
    conn.sendall(OK.encode())


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
                    conn.sendall(OK.encode())

                    # read data from request
                    request = conn.recv(BUFFER_SIZE)
                    method = request.decode().split(" ")[0]
                    while len(request) < int(request_size):
                        data = conn.recv(BUFFER_SIZE)
                        request = request + data

                    # process request
                    request = request.decode()
                    if method == GET:
                        get(conn=conn, request=request, trie=trie)

                    elif method == PUT:
                        put(conn=conn, request=request, trie=trie)

                    elif method == QUERY:
                        query(conn=conn, request=request, trie=trie)

                    elif method == DELETE:
                        delete(conn=conn, request=request, trie=trie)


if __name__ == "__main__":
    main()
