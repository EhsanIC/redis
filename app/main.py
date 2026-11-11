from app.commands import Commands
from app.server import Server


def main():
    commands = Commands()
    Server(commands)


if __name__ == "__main__":
    main()

# adding comment -> full refactor
