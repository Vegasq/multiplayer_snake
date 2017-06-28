import socketserver
from messages import NEW_CLIENT, GO_UP, GO_DOWN, GO_RIGHT, GO_LEFT, GET_WORLD
import settings
import json
import context
import time

from utils import messages as utils_messages


class Server(socketserver.BaseRequestHandler):
    def register_new_client(self, user_uuid: str) -> None:
        with context.lock:
            if user_uuid in context.clients:
                return

            context.clients[user_uuid] = {
                "direction": GO_UP,
                "position": (0, 0),
                "address": self.client_address[0]
            }
        self.request.sendall(bytes("OK", "utf-8"))

    def send_world_message(self) -> None:
        self.request.sendall(bytes(json.dumps(context.world), "utf-8"))

    def send_sub_world_message(self, user_uuid) -> None:
        if not context.is_client_exists(user_uuid):
            return

        x, y = context.get_head_position(user_uuid)

        cells_around = 16

        top_delim = y - cells_around
        bot_delim = y + cells_around

        if y < cells_around:
            top_delim = 0
            bot_delim = cells_around * 2

        if y+cells_around > len(context.world):
            bot_delim = len(context.world)
            top_delim = bot_delim - cells_around * 2

        sub_1 = context.world[top_delim:bot_delim]

        left_delim = x - cells_around
        right_delim = x + cells_around

        if x < cells_around:
            left_delim = 0
            right_delim = cells_around * 2

        if x+cells_around > len(context.world):
            right_delim = len(context.world)
            left_delim = right_delim - cells_around * 2

        sub_2 = [r[left_delim:right_delim] for r in sub_1]

        self.request.sendall(
            bytes(
                json.dumps(sub_2), "utf-8"))

    def set_direction(self, user_uuid: str, message: str) -> None:
        with context.lock:
            context.set_direction(user_uuid, message)
        self.request.sendall(bytes("OK", "utf-8"))

    def handle(self) -> None:
        data = self.request.recv(1024).strip().decode()
        user_uuid, message = utils_messages.unpack(data)

        if message == GET_WORLD:
            # self.send_world_message()
            self.send_sub_world_message(user_uuid)
        elif message == NEW_CLIENT and user_uuid not in context.clients:
            self.register_new_client(user_uuid)
        elif user_uuid in context.clients and message in [
            GO_UP, GO_DOWN, GO_RIGHT, GO_LEFT
        ]:
            self.set_direction(user_uuid, message)
        else:
            print("Unknown message: %s\nfrom uuid: %s" % (message, user_uuid))

    @staticmethod
    def start() -> None:
        try:
            server = socketserver.TCPServer(
                (settings.host, settings.port), Server)
            context.server_alive = True
        except OSError as err:
            print("Can't start server: %s" % err)
            context.server_alive = False
            time.sleep(5)
            return Server.start()

        try:
            server.serve_forever()
        except KeyboardInterrupt:
            server.shutdown()
