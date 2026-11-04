import socket  # noqa: F401


clients = []

storage = {}

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

            if command == b"ECHO":
                args = parts[4]
                reply = b"$" + str(len(args)).encode() + b"\r\n" + args + b"\r\n"
                conn.sendall(reply)

            elif command == b"SET":
                key = parts[4]
                value = parts[6]
                storage[key] = value
                conn.sendall(b"+OK\r\n")

            elif command == b"GET":
                paramName = parts[4]
                if paramName in storage :
                    paramValue = storage[paramName]
                    reply = b"$" + str(len(paramValue)).encode() + b"\r\n" + paramValue + b"\r\n"
                    conn.sendall(reply)


            else:
                conn.sendall(b"+PONG\r\n")



    # server_socket.settimeout(1.0)

if __name__ == "__main__":
    main()

# adding comment -> Implement the ECHO command
