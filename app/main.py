import socket
from commands import Commands
from server import Server

clients = []

def main():
    commands = Commands()
    Server(commands)


if __name__ == "__main__":
    main()

# adding comment -> full refactor
