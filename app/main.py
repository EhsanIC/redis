import socket
import time  # noqa: F401


clients = []

storage = {}

NULL_BULK = b"$-1\r\n"

MULTIPLIER = {b"EX": 1000, b"PX": 1}

# storage[key] = ['value' , 1000] # mili second
# storage[key] = ['value' , 100]  # mili second
#

def main():
    print("Logs from your program will appear here!")


    server_socket = socket.create_server(("localhost", 6379))
    server_socket.setblocking(False)

    while True:

        try:
            conn , _ = server_socket.accept()
            conn.setblocking(False)
            clients.append(conn)
        except BlockingIOError:
            pass # nobody is trying to connect right now

        for conn in clients[:] :

            try:
                data = conn.recv(1024)
            except BlockingIOError:
                continue # this client sent nothing, check the next one
            except ConnectionResetError:
                data = b""


            if not data:
                clients.remove(conn)
                conn.close()
                continue

            # *2\r\n$4\r\nECHO\r\n$3\r\nhey\r\n
            result = handle_command(data.split(b"\r\n"))
            conn.sendall(result)
    # server_socket.settimeout(1.0)

def is_alive(expire_time):
    if expire_time == None:
        return True
    else:
        return expire_time > now_ms()

def now_ms():
    return time.monotonic() * 1000

def bulk_string(value):
    return b"$" + str(len(value)).encode() + b"\r\n" + value + b"\r\n"


# handing commands
def handle_command(parts):

    command = parts[2].upper()

    match command:

        case b"ECHO":
            args = parts[4]
            return bulk_string(args)

        case b"SET":
            key = parts[4]
            value = parts[6]

            if len(parts) > 8 and parts[8].upper() in MULTIPLIER:

                time_value = int(parts[10])

                multiplier = MULTIPLIER[parts[8].upper()]
                expire_at = now_ms() + time_value * multiplier

                storage[key] = [value , expire_at]

            else:
                storage[key] = [value , None]

            return b"+OK\r\n"

        case b"GET":

            key = parts[4]
            if key in storage :
                value , expire_time = storage[key]
                if is_alive(expire_time):
                    return bulk_string(value)

                else:
                    return NULL_BULK
            else:
                return NULL_BULK
        case _:
            return b"+PONG\r\n"





if __name__ == "__main__":
    # print > time.monotonic())
    # print(time.time())
    main()

# adding comment -> Implement the SET & GET commands
