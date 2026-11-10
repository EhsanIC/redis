from collections import deque

from app.helpers import is_alive, now_ms, bulk_string, bulk_list, NULL_BULK, MULTIPLIER , EMPTY_LIST , NULL_ARRAY, ZERO_INT


class Commands:

    def __init__(self) -> None:
        self.storage = {}
        self.storage_list = {}
        self.waiters = {}

    def handle(self , parts , conn):

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

            case b"LPUSH":
                return self.lpush(parts)

            case b"LRANGE":
                return self.lrange(parts)

            case b"LLEN":
                return self.llen(parts)

            case b"LPOP":
                return self.lpop(parts)

            case b"BLPOP":
                return self.blpop(parts , conn)

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

        self.storage_list.setdefault(key , []).extend(value_list)
        length = len(self.storage_list[key])
        self._server_waiter(key)

        return b":" + str(length).encode() + b"\r\n"

        # if key in self.storage_list:
        #     self.storage_list[key].extend(value_list)
        # else:
        #     self.storage_list[key] = value_list

        # length = len(self.storage_list[key])                        # 2. read length
                                        # 3. wake one waiter





    def lrange(self , parts):
        key = parts[4]
        # [b'a', b'b']
        rangs = parts[6:len(parts):2]
        start = int(rangs[0])
        stop = int(rangs[1]) + 1
        if stop == 0 : stop = None




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


        return bulk_list(value_list[start:stop])

    def lpush(self, parts):
        key = parts[4]
        value_list = parts[6:len(parts):2]

        self.storage_list[key] = value_list[::-1] + self.storage_list.get(key , [])
        length = len(self.storage_list[key])
        self._server_waiter(key)

        return b":" + str(length).encode() + b"\r\n"


    def llen(self, parts):
        key = parts[4]
        if key in self.storage_list :
            return b":" + str(len(self.storage_list[key])).encode() + b"\r\n"
        else:
            return ZERO_INT

    def lpop(self, parts):
        key = parts[4]
        remove_num = int(parts[6]) if len(parts) > 6 else None
        removed = []

        if remove_num != None:
            remove_num = int(parts[6])
            for _ in range(remove_num):
                removed.append(self.storage_list[key].pop(0))

            return bulk_list(removed)

        return bulk_string(self.storage_list[key].pop(0))


    def blpop(self, parts , conn):
        key = parts[4]
        time_out = int(parts[6])

        if self.storage_list.get(key):
            return bulk_list([key , self.storage_list[key].pop(0)])

        deadline = (now_ms() / 1000) + time_out if time_out != 0 else None

        self.waiters.setdefault(key, deque()).append((conn, deadline))
        return None

        # set the deadline
        # chekcing the deadlines
        # remove the daedline if needed

        # with self.cond:
        #     while not self.storage_list.get(key):
        #         self.cond.wait()
        #     item = self.storage_list[key].pop(0)

        # if the list has an item:
        #     pop the front item, reply [key, item] now
        # else:
        #     wait until a push happens (timeout 0 = no deadline)

        # RESP encoding of ["list_key", "foo"]
        # *2\r\n
        # $8\r\n
        # list_key\r\n
        # $3\r\n
        # foo\r\n


    def _server_waiter(self , key):
        queue = self.waiters.get(key)
        while queue and self.storage_list.get(key):
            conn, _ = queue.popleft()
            item = self.storage_list[key].pop(0)
            conn.sendall(bulk_list([key, item]))

    def disconnect(self , conn):
        for key, queue in self.waiters.items():
            self.waiters[key] = deque(w for w in queue if w[0] != conn)

    def expire_waiters(self):
        for key, queue in self.waiters.items():
            alive = deque()

            for conn, deadline in queue:
                if is_alive(deadline):
                    alive.append((conn, deadline))
                else:
                    conn.sendall(NULL_ARRAY)

            self.waiters[key] = alive

#-> Parking blocked clients
