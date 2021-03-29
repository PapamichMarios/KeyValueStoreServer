from socket import socket

from logging import log_error
from properties import ERROR, NOT_FOUND, ALREADY_EXISTS, BAD_SYNTAX
from utils import construct_response


def not_found_response(s: socket, request: str):
    log_error(code=ERROR, request=request, reason=NOT_FOUND)
    construct_response(s=s, data=ERROR + ": " + NOT_FOUND, success=False)


def bad_syntax_response(s: socket, request: str):
    log_error(code=ERROR, request=request, reason=BAD_SYNTAX)
    construct_response(s=s, data=ERROR + ": " + BAD_SYNTAX, success=False)


def already_exists_response(s: socket, request: str):
    log_error(code=ERROR, request=request, reason=ALREADY_EXISTS)
    construct_response(s=s, data=ERROR + ": " + ALREADY_EXISTS, success=False)
