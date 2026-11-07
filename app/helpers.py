import time  # noqa: F401

NULL_BULK = b"$-1\r\n"

EMPTY_LIST = b"*0\r\n"

MULTIPLIER = {b"EX": 1000, b"PX": 1}

def is_alive(expire_time):
    if expire_time == None:
        return True
    else:
        return expire_time > now_ms()

def now_ms():
    return time.monotonic() * 1000

def bulk_string(value):
    return b"$" + str(len(value)).encode() + b"\r\n" + value + b"\r\n"
