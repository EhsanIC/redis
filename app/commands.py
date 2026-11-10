from app.helpers import is_alive, now_ms, bulk_string, bulk_list, NULL_BULK, MULTIPLIER , EMPTY_LIST

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
        start = int(rangs[0])
        stop = int(rangs[1])
        if not stop < 0 :
            stop += 1
        elif stop < 0:
            stop -= 1



        # If the list doesn't exist, an empty array is returned.
        if key not in self.storage_list:
            print("the list is empty")
            return EMPTY_LIST

        value_list = self.storage_list[key]

        # # If the start index is greater than or equal to the list's length, an empty array is returned.
        # if start >= len(self.storage_list[key]):
        #     return EMPTY_LIST

        # if stop == None:
        #     return value_list[start:]


        # # If the stop index is greater than or equal to the list's length, the stop index is treated as the last element.
        # if stop >= len(self.storage_list[key]):
        #     return value_list[start:]

        # # If the start index is greater than the stop index, an empty array is returned.
        # if start > stop :
        #     return EMPTY_LIST


        # if 0 > (len(self.storage_list[key]) + stop):
        #     return bulk_list(value_list[0:stop])


        print(value_list[start:stop])
        return bulk_list(value_list[start:stop])
