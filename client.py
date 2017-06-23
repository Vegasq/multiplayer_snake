import uuid
import json
from messages import NEW_CLIENT, GO_UP, GO_DOWN, GO_RIGHT, GO_LEFT, GET_WORLD, CLIENT_RESET
import ui

from networking import Client


class SnakeClient(object):
    def __init__(self, stupid=False):
        self.uuid = None
        self.ui = None

        self.net_cli = Client()

        if not stupid:
            self.ui = ui.SnakeUI()

    def create(self):
        self.uuid = str(uuid.uuid1())
        self.net_cli.set_uuid(self.uuid)
        self.net_cli.send(NEW_CLIENT)

    def get_world(self):
        res = self.net_cli.send(GET_WORLD)
        try:
            return json.loads(res)
        except json.decoder.JSONDecodeError:
            with open("dump", "w") as fl:
                print("Broken world recieved.")
                fl.write(res)
            return self.get_world()

    def commands_handler(self):
        cmd = self.ui.get_event()
        if cmd in [GO_UP, GO_DOWN, GO_RIGHT, GO_LEFT]:
            self.net_cli.send(cmd)
        if cmd == CLIENT_RESET:
            self.create()

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
