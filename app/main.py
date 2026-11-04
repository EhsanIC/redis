import socket  # noqa: F401


clients = []

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

            conn.sendall(b"+PONG\r\n")



    # server_socket.settimeout(1.0)

if __name__ == "__main__":
    main()
