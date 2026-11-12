import time  # noqa: F401

NULL_BULK = b"$-1\r\n"

ZERO_INT = b":0\r\n"

EMPTY_LIST = b"*0\r\n"

MULTIPLIER = {b"EX": 1000, b"PX": 1}

NULL_ARRAY = b"*-1\r\n"

def is_alive(expire_time):
    return expire_time is None or expire_time > now_ms()


def now_ms():
    return time.monotonic() * 1000

def bulk_string(value):
    return b"$" + str(len(value)).encode() + b"\r\n" + value + b"\r\n"

def bulk_number(value):
    return b":" + str(value).encode() + b"\r\n"


def bulk_list(list):
    result = b"*" + str(len(list)).encode() + b"\r\n"
    for item in list:
        result += bulk_string(item)

    return result

def parse_resp(data):
    parts = data.split(b"\r\n")
    return parts[2::2]
