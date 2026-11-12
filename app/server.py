import socket

clients = []

def Server(command_handler , waiters):
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


        # command_handler.expire_waiters() # check deadlines every pass

        waiters.expire()

        for conn in clients[:] :

            try:
                data = conn.recv(1024)
            except BlockingIOError:
                continue # this client sent nothing, check the next one
            except ConnectionResetError:
                data = b""


            if not data:
                waiters.disconnect(conn)
                clients.remove(conn)
                conn.close()
                continue

            # *2\r\n$4\r\nECHO\r\n$3\r\nhey\r\n
            result = command_handler.handle(data , conn)
            if result is not None:
                conn.sendall(result)

            # server_socket.settimeout(1.0)
