import socket
import argparse
import random

BUFFER_SIZE = 1024


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
    for record in records:

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

            print('Record ', i)
            # replicas: uniquely generated numbers of range [0, len(servers)]
            replicas = random.sample(range(0, len(servers)), args.k)
            for replica in [0]:  # replicas:

                # connect
                s.connect((servers[replica][0], int(servers[replica][1])))

                # send request size & request
                request = ("PUT " + record.replace('\n', '')).encode()
                s.send(str(len(request)).encode())
                data = s.recv(BUFFER_SIZE)
                s.sendall(request)

                # receive ack from server
                data = s.recv(BUFFER_SIZE)

                # print methods
                print('\tServer ' + str(replica) + ': ' + data.decode())

        i += 1


if __name__ == "__main__":
    main()
