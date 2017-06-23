import threading

from game import Game
from networking import Server


def start():
    threads = []
    ts = threading.Thread(name="tcp serv", target=Server.start)
    threads.append(ts)

    console_printer = Game()
    cp = threading.Thread(name="game logic", target=console_printer.loop)
    threads.append(cp)

    ts.start()
    cp.start()


if __name__ == "__main__":
    start()
