import time  # noqa: F401

NULL_BULK = b"$-1\r\n"

ZERO_INT = b":0\r\n"

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


# ["a" , "b" , "c"]
# *3\r\n
# $1\r\n
# a\r\n
# $1\r\n
# b\r\n
# $1\r\n
# c\r\n
#
def bulk_list(list):
    result = b"*" + str(len(list)).encode() + b"\r\n"
    for item in list:
        result += bulk_string(item)

    return result
    # return b"$" + str(len(list)).encode() + b"\r\n" + list + b"\r\n"
