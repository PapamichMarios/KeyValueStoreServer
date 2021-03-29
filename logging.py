from datetime import datetime


def log_error(code: str, request: str, reason: str):
    now = datetime.now()
    dt_string = now.strftime("%d-%m-%Y %H:%M:%S")
    print(dt_string + " " + code + " - " + reason + ": " + request)


def log(code: str, request: str):
    now = datetime.now()
    dt_string = now.strftime("%d-%m-%Y %H:%M:%S")
    print(dt_string + " " + code + ": " + request)