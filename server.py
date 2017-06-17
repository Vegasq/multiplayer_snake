import threading
import json

import context
from objects import Game
from tcp_server import SnakeServer


def start():
    threads = []
    ts = threading.Thread(name="tcp serv", target=SnakeServer.tcp_server)
    threads.append(ts)

    console_printer = Game()
    cp = threading.Thread(name="game logic", target=console_printer.loop)
    threads.append(cp)

    ts.start()
    cp.start()


if __name__ == "__main__":
    start()
