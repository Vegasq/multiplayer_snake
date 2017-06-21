import socket
import uuid
import json
import time
from messages import NEW_CLIENT, GO_UP, GO_DOWN, GO_RIGHT, GO_LEFT, GET_WORLD
import settings
import threading


class SnakeClient(object):
    def __init__(self):
        self.uuid = str(uuid.uuid1())

    def pack_message(self, message):
        return json.dumps({
            "uuid": self.uuid,
            "message": message
        })

    def _send(self, message):
        if message is None:
            return
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((settings.host, settings.port))
        s.sendall(self.pack_message(message))
        resp = s.recv(8192)
        s.close()

        return resp

    def create(self):
        self._send(NEW_CLIENT)

    def get_world(self):
        res = self._send(GET_WORLD)
        return json.loads(res)

    def loop(self):
        while True:

            for i in [
                GO_RIGHT, GO_RIGHT, GO_RIGHT, GO_RIGHT, GO_RIGHT,
                GO_DOWN, GO_DOWN, GO_DOWN, GO_DOWN,
                GO_LEFT, GO_LEFT, GO_LEFT, GO_LEFT, GO_LEFT, GO_LEFT, GO_LEFT,
                GO_DOWN,
                GO_RIGHT, GO_RIGHT,
                GO_UP
            ]:
                self._send(i)
                w = self.get_world()
                print("\n" * 10)
                for r in w:
                    print("".join(r).replace(" ", "."))
                time.sleep(0.2)

    def commands_handler(self):
        while True:
            for i in [
                GO_RIGHT, GO_RIGHT, GO_RIGHT, GO_RIGHT, GO_RIGHT,
                GO_DOWN, GO_DOWN, GO_DOWN, GO_DOWN,
                GO_LEFT, GO_LEFT, GO_LEFT, GO_LEFT, GO_LEFT, GO_LEFT, GO_LEFT,
                GO_DOWN,
                GO_RIGHT, GO_RIGHT,
                GO_UP
            ]:
                self._send(i)
                time.sleep(1)

    def display_map(self):
        while True:
            w = self.get_world()
            print("\n" * 10)
            for r in w:
                print("".join(r).replace(" ", "."))
            time.sleep(0.01)


client = SnakeClient()
client.create()

dm = threading.Thread(name="tcp serv", target=client.display_map)
cm = threading.Thread(name="game logic", target=client.commands_handler)

dm.start()
cm.start()
