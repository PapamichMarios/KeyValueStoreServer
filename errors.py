from socket import socket

from logging import log_error
from properties import ERROR, NOT_FOUND, ALREADY_EXISTS, BAD_SYNTAX


def send_error(code: str, reason: str) -> bytes:
    return (code + ": " + reason).encode()


def not_found(s: socket, request: str):
    log_error(code=ERROR, request=request, reason=NOT_FOUND)
    s.sendall(send_error(code=ERROR, reason=NOT_FOUND))


def bad_syntax(s: socket, request: str):
    log_error(code=ERROR, request=request, reason=BAD_SYNTAX)
    s.sendall(send_error(code=ERROR, reason=BAD_SYNTAX))


def already_exists(s: socket, request: str):
    log_error(code=ERROR, request=request, reason=ALREADY_EXISTS)
    s.sendall(send_error(code=ERROR, reason=ALREADY_EXISTS))