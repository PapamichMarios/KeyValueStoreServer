import json
from socket import socket

from properties import BUFFER_SIZE


def construct_response(s: socket, data, success: bool):
    obj = {
        "success": success,
        "data": data
    }
    response = json.dumps(obj).replace(",", ";")

    # send length of request & ack
    s.send(str(len(response)).encode())
    s.recv(BUFFER_SIZE)

    s.sendall(response.encode())


def print_response(response: dict):
    print("\t" + json.dumps(response["data"])[1:-1])
