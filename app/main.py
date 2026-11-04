import socket  # noqa: F401


clients = []

def main():
    print("Logs from your program will appear here!")


    server_socket = socket.create_server(("localhost", 6379))

    while True:
        
        conn , _ = server_socket.accept()
        clients.append(conn)
        
        for conn in clients[:] :
            data = conn.recv(1024)

            if not data:
                clients.remove(conn)
                conn.close()
                continue
                
            conn.sendall(b"+PONG\r\n")



    # server_socket.settimeout(1.0)

if __name__ == "__main__":
    main()
