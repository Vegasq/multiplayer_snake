import socket
import hashlib
import uuid
import json
import time

from messages import NEW_CLIENT, GO_UP, GO_DOWN, GO_RIGHT, GO_LEFT
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
        resp = s.recv(1024)
        s.close()

    def create(self):
        self._send(NEW_CLIENT)

    def loop(self):
        COMMANDS = [GO_UP, GO_DOWN, GO_RIGHT, GO_LEFT]
        for i in COMMANDS:
            time.sleep(3)
            self._send(i)


client = SnakeClient()
client.create()
client.loop()