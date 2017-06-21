import socket
import uuid
import json
import time
from messages import NEW_CLIENT, GO_UP, GO_DOWN, GO_RIGHT, GO_LEFT, GET_WORLD
import settings
import threading
import ui


class SnakeClient(object):
    def __init__(self, stupid=False):
        self.uuid = str(uuid.uuid1())

        if not stupid:
            self.ui = ui.SnakeUI()

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
        s.sendall(bytes(self.pack_message(message), "utf-8"))
        resp = self.recvall(s)
        s.close()

        return resp

    def recvall(self, sock):
        BUFF_SIZE = 4096  # 4 KiB
        data = ""
        while True:
            part = sock.recv(BUFF_SIZE)

            print("~" * 100)
            print(part)
            print(len(part))

            data += part.strip().decode()
            if len(part) < BUFF_SIZE:
                # either 0 or end of data
                break
        return data

    def create(self):
        self._send(NEW_CLIENT)

    def get_world(self):
        res = self._send(GET_WORLD)
        try:
            return json.loads(res)
        except json.decoder.JSONDecodeError:
            with open("dump", "w") as fl:
                fl.write(res)
            raise

    def commands_handler(self):
        direction = self.ui.get_event()
        self._send(direction)

    def display_map(self):
        w = self.get_world()
        self.ui.draw(w)

    def run(self):
        while True:
            self.commands_handler()
            self.display_map()


if __name__ == "__main__":
    client = SnakeClient()
    client.create()

    client.run()
