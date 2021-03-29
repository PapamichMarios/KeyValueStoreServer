import socket
import argparse
import random

from errors import send_error
from properties import BUFFER_SIZE, PUT, GET, QUERY, DELETE, ERROR, BAD_SYNTAX


def check_method(method: str) -> bool:
    if method != PUT and method != GET and method != QUERY and method != DELETE:
        return False

    return True


def send_request(s: socket, request: bytes, index: int) -> str:
    s.send(str(len(request)).encode())
    data = s.recv(BUFFER_SIZE)
    s.sendall(request)

    # receive ack from server
    data = s.recv(BUFFER_SIZE)

    # print methods
    print('\tServer ' + str(index) + ': ' + data.decode())
    return data


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
                s.connect((servers[replica][0], int(servers[replica][1])))

                # send request size & request
                request = ("PUT " + record.replace('\n', '')).encode()
                send_request(s, request, replica)

        i += 1

    # keyboard requests
    while True:
        request = input("kv_broker$: ")
        method = request.split(" ")[0]
        if not check_method(method):
            print("\t" + send_error(code=ERROR, reason=BAD_SYNTAX).decode())
            continue

        for x in range(0, len(servers)):
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                # connect
                s.connect((servers[x][0], int(servers[x][1])))

                # send request size & request
                response = send_request(s, request.encode(), x)
                

if __name__ == "__main__":
    main()
