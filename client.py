import socket
import hashlib
import uuid
import json
import time
import random
from messages import NEW_CLIENT, GO_UP, GO_DOWN, GO_RIGHT, GO_LEFT, GET_WORLD
import settings


class SnakeClient(object):
    def __init__(self):
        self.uuid = str(uuid.uuid1())

    def pack_message(self, message):
        return json.dumps({
            "uuid": self.uuid,
            "message": message
        })

    def _send(self, message):
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
        for i in range(10):
            self._send(random.choice([GO_UP, GO_RIGHT]))
            w = self.get_world()
            for r in w:
                print("".join(r))
            time.sleep(1)

        # COMMANDS = [GO_DOWN, GO_LEFT, GO_UP, GO_RIGHT]
        # for i in COMMANDS:
        #     time.sleep(3)
        #     self._send(i)


client = SnakeClient()
client.create()
client.loop()