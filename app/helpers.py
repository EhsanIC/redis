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
    # [b"command", b"key", b"value", b"PX", b"100"]
    # [b"command", b"key", b"value", b"option"]
    # Raw bytes in                                                          ->  Python list out
    # *1\r\n$4\r\nPING\r\n                                                  ->  [b"PING"]
    # *2\r\n$4\r\nECHO\r\n$3\r\nhey\r\n                                     ->  [b"ECHO", b"hey"]
    # *3\r\n$3\r\nGET\r\n$3\r\nfoo\r\n  (GET foo)                           ->  [b"GET", b"foo"]
    # *3\r\n$3\r\nSET\r\n$3\r\nfoo\r\n$3\r\nbar\r\n                         ->  [b"SET", b"foo", b"bar"]
    # *5\r\n$3\r\nSET\r\n$4\r\ntemp\r\n$1\r\n1\r\n$2\r\nPX\r\n$3\r\n100\r\n ->  [b"SET", b"temp", b"1", b"PX", b"100"]                                                   
    # *5\r\n$5\r\nRPUSH\r\n$1\r\nl\r\n$1\r\na\r\n$1\r\nb\r\n$1\r\nc\r\n     ->  [b"RPUSH", b"l", b"a", b"b", b"c"]                                                               
    # LRANGE l 0 -1                                                         ->  [b"LRANGE", b"l", b"0", b"-1"]
    # LPOP l 2                                                              ->  [b"LPOP", b"l", b"2"]
    # BLPOP l 0.5                                                           ->  [b"BLPOP", b"l", b"0.5"]

    
        # key = parts[4]
        # value = parts[6]
        
    test = "nigga"
    testNIgaa = "nigga"

    ...
