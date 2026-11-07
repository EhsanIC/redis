from helpers import is_alive , now_ms , bulk_string , NULL_BULK , MULTIPLIER

class Commands:

    def __init__(self) -> None:
        self.storage = {}
        self.storage_list = {}

    def handle(self , parts):

        command = parts[2].upper()

        match command:
            case b"ECHO":
                return self.echo(parts)

            case b"SET":
                return self.set(parts)

            case b"GET":
                return self.get(parts)

            case b"RPUSH":
                return self.rpush(parts)

            case b"LRANGE":
                return self.lrange(parts)

            case _:
                return b"+PONG\r\n"


    def echo(self , parts):
        return bulk_string(parts[4])


    def set(self , parts):
        key = parts[4]
        value = parts[6]

        if len(parts) > 8 and parts[8].upper() in MULTIPLIER:

            time_value = int(parts[10])

            multiplier = MULTIPLIER[parts[8].upper()]
            expire_at = now_ms() + time_value * multiplier

            self.storage[key] = [value , expire_at]

        else:
            self.storage[key] = [value , None]

        return b"+OK\r\n"


    def get(self , parts):
        key = parts[4]
        if key in self.storage :
            value , expire_time = self.storage[key]
            if is_alive(expire_time):
                return bulk_string(value)

            else:
                return NULL_BULK
        else:
            return NULL_BULK

    def rpush(self , parts):
        key = parts[4]
        # [b'pineapple', b'banana']
        value_list = parts[6:len(parts):2]

        if key in self.storage_list:
            self.storage_list[key].extend(value_list)
        else:
            self.storage_list[key] = value_list


        return b":" + str(len(self.storage_list[key])).encode() + b"\r\n"


    def lrange(self , parts):
        key = parts[4]
        # [b'a', b'b']
        rangs = parts[6:len(parts):2]
        min = rangs[0]
        max = rangs[1]

        value_list = self.storage_list[key]
        return value_list[min:max]
