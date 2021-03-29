import json
import socket
import argparse
import random

from properties import BUFFER_SIZE, PUT, GET, QUERY, DELETE, ERROR, BAD_SYNTAX, NOT_FOUND, REPLICA_IS_DOWN, \
    CANNOT_EXECUTE, CANNOT_GUARANTEE_CORRECT_OUTPUT, OK, WARNING
from utils import print_response


def check_method(method: str) -> bool:
    if method != PUT and method != GET and method != QUERY and method != DELETE:
        return False

    return True


def send_request(s: socket, request: bytes) -> str:

    # send request size & ack
    s.send(str(len(request)).encode())
    response = s.recv(BUFFER_SIZE)

    # send request
    s.sendall(request)

    # receive response size
    response_size = int(s.recv(BUFFER_SIZE))
    s.send(OK.encode())

    # receive response
    request = s.recv(BUFFER_SIZE)
    while len(request) < response_size:
        data = s.recv(BUFFER_SIZE)
        request = request + data

    return request.decode()


def main():
    # arg parsing
    parser = argparse.ArgumentParser(description="Process arguments for data creation")
    parser.add_argument('-s', type=str, help="file containing server ips and ports", default="serverFile.txt")
    parser.add_argument('-i', type=str, help="file containing data for indexing",
                        default="./data_creation/dataToIndex.txt")
    parser.add_argument('-k', type=int, help="post", default=2)
    args = parser.parse_args()

    with open(args.s, 'r') as server_file:
        servers = [[str(x) for x in line.split()] for line in server_file]

    with open(args.i, 'r') as index_file:
        records = [str(line) for line in index_file]

    i = 0
    # indexing data
    for record in records:
        print('Record ', i)

        # replicas: uniquely generated numbers of range [0, len(servers)]
        replicas = random.sample(range(0, len(servers)), args.k)
        for replica in replicas:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                # connect
                try:
                    s.connect((servers[replica][0], int(servers[replica][1])))
                except ConnectionRefusedError:
                    print("\tServer " + str(replica) + ": " + REPLICA_IS_DOWN)
                    continue

                # send request size & request
                request = ("PUT " + record.replace('\n', '')).encode()
                response = send_request(s, request)
                response = json.loads(response.replace(";", ","))
                print('\tServer ' + str(replica) + ': ' + json.dumps(response["data"])[1:-1])

        i += 1

    # keyboard requests
    while True:
        request = input("kv_broker$: ")
        method = request.split(" ")[0]
        if not check_method(method):
            print("\t" + ERROR + ": " + BAD_SYNTAX)
            continue

        down_servers = []
        sockets = []
        # connect to servers
        for x in range(0, len(servers)):

            sockets.append(socket.socket(socket.AF_INET, socket.SOCK_STREAM))

            # connect
            try:
                sockets[x].connect((servers[x][0], int(servers[x][1])))
            except ConnectionRefusedError:
                down_servers.append(x)

        # print warnings
        if len(down_servers) > 0 and method == DELETE:
            print("\t" + ERROR + " - " + REPLICA_IS_DOWN + ": " + CANNOT_EXECUTE)
            continue

        if len(down_servers) >= args.k and (method == GET or method == QUERY):
            print("\t" + WARNING + " - " + REPLICA_IS_DOWN + ": " + CANNOT_GUARANTEE_CORRECT_OUTPUT)

        # send requests
        responses = set()
        for x in range(0, len(servers)):

            # check if server is down
            is_down = False
            for server in down_servers:
                if server == x:
                    is_down = True

            if is_down:
                continue

            # send request size & request
            response = send_request(sockets[x], request.encode())
            print('\tServer ' + str(x) + ': ' + response)

            # print response
            responses.add(response)
            sockets[x].close()

        # print result
        has_printed = False
        for response in responses:
            response = json.loads(response.replace(";", ","))
            if response["success"]:
                has_printed = True
                print_response(response=response)

        if not has_printed:
            response = json.loads(next(iter(responses)).replace(";", ","))
            print_response(response=response)


if __name__ == "__main__":
    main()
