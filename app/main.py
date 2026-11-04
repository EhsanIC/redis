import socket
import time  # noqa: F401


clients = []

storage = {}

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
            parts = data.split(b"\r\n")

            command = parts[2].upper()

            match command:

                case b"ECHO":
                    args = parts[4]
                    reply = b"$" + str(len(args)).encode() + b"\r\n" + args + b"\r\n"
                    conn.sendall(reply)

                case b"SET":
                    key = parts[4]
                    value = parts[6]

                    if len(parts) > 8 and parts[8].upper() in (b"EX", b"PX"):

                        time_value = int(parts[10])
                        current_time = time.monotonic() * 1000 # turn ot millisecond

                        match parts[8]:
                            case b"EX":
                                storage[key] = [value , current_time + time_value * 1000] # turn to millisecond
                                print("SET", key, storage[key], flush=True) # loges
                            case b"PX":
                                storage[key] = [value , current_time + time_value]
                                print("SET", key, storage[key], flush=True) # loges

                    else:
                        storage[key] = [value , None]
                        print("SET", key, storage[key], flush=True) # loges

                    conn.sendall(b"+OK\r\n")

                case b"GET":

                    key = parts[4]
                    if key in storage :
                        value , expire_time = storage[key]
                        if isExpire(expire_time):
                            reply = b"$" + str(len(value)).encode() + b"\r\n" + value + b"\r\n"
                            conn.sendall(reply)



                case _:
                    conn.sendall(b"+PONG\r\n")



    # server_socket.settimeout(1.0)

def isExpire(expire_time):
    # value , expire_time = storage[key]
    if expire_time == None:
        return True
    else:
        return expire_time > time.monotonic() * 1000

if __name__ == "__main__":
    # print > time.monotonic())
    # print(time.time())
    main()

# adding comment -> Implement the SET & GET commands
