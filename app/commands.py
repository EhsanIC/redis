from app.helpers import bulk_number, is_alive, now_ms, bulk_string, bulk_list, NULL_BULK, MULTIPLIER , EMPTY_LIST , ZERO_INT, parse_resp, simple_string
from app.waiters import Waiters


class Commands:

    def __init__(self) -> None:
        self.storage = {}
        self.storage_list = {}
        self.waiters = Waiters()

    def handle(self , parts , conn):

        # giving to handler

        # command = parts[2].upper()
        command , *args = parse_resp(parts)



        match command.upper():
            case b"ECHO":
                return self.echo(args)

            case b"SET":
                return self.set(args)

            case b"GET":
                return self.get(args)

            case b"RPUSH":
                return self.rpush(args)

            case b"LPUSH":
                return self.lpush(args)

            case b"LRANGE":
                return self.lrange(args)

            case b"LLEN":
                return self.llen(args)

            case b"LPOP":
                return self.lpop(args)

            case b"BLPOP":
                return self.blpop(args , conn)

            case b"TYPE":
                return self.type(args)

            case _:
                return b"+PONG\r\n"


    def echo(self , args):
        return bulk_string(args[0])

    def set(self , args):
        key , value , *options  = args
        expire_at = None

        if options and options[0].upper() in MULTIPLIER:

            multiplier_type , time_limit = options
            multiplier = MULTIPLIER[multiplier_type.upper()]
            expire_at = now_ms() + int(time_limit) * multiplier

        self.storage[key] = [value , expire_at]
        return b"+OK\r\n"


    def get(self , args):
        key = args[0]
        if key in self.storage :
            value , expire_time = self.storage[key]
            if is_alive(expire_time):
                return bulk_string(value)

            else:
                return NULL_BULK
        else:
            return NULL_BULK

    def rpush(self , args):
        key , *value_list = args

        self.storage_list.setdefault(key , []).extend(value_list)
        length = len(self.storage_list[key])
        self._serve(key)

        return bulk_number(length)







    def lrange(self , args):
        key , start , stop = args
        start , stop = int(start) , int(stop) + 1
        if stop == 0 : stop = None

        # If the list doesn't exist, an empty array is returned.
        if key not in self.storage_list:
            return EMPTY_LIST

        value_list = self.storage_list[key]

        return bulk_list(value_list[start:stop])

    def lpush(self, args):
        key , *value_list = args

        self.storage_list[key] = value_list[::-1] + self.storage_list.get(key , [])
        length = len(self.storage_list[key])
        self._serve(key)

        return bulk_number(length)


    def llen(self, args):
        key = args[0]
        if key in self.storage_list :
            return bulk_number(len(self.storage_list[key]))
        else:
            return ZERO_INT

    def lpop(self, args):
        key = args[0]
        remove_num = int(args[1]) if len(args) > 1 else None
        removed = []

        if remove_num != None:
            for _ in range(remove_num):
                removed.append(self.storage_list[key].pop(0))

            return bulk_list(removed)

        return bulk_string(self.storage_list[key].pop(0))


    def blpop(self, args , conn):
        key , time_out = args
        time_out = float(time_out)

        if self.storage_list.get(key):
            return bulk_list([key , self.storage_list[key].pop(0)])

        deadline = now_ms() + (time_out * 1000) if time_out != 0 else None

        self.waiters.register(key , conn , deadline)
        return None


    def _serve(self, key):
        while self.storage_list.get(key) and self.waiters.notify(key ,self.storage_list[key][0]):
            self.storage_list[key].pop(0)


    def type(self, args):
        key = args[0]

        if key in self.storage:
            return simple_string(b"string")
        return simple_string(b"none")

        # string, list, set, zset, hash, stream, and vectorset
