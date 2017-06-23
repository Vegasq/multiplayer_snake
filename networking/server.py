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
            context.clients[user_uuid] = {
                "direction": GO_UP,
                "address": self.client_address[0]
            }
        self.request.sendall(bytes("OK", "utf-8"))

    def send_world_message(self) -> None:
        self.request.sendall(bytes(json.dumps(context.world), "utf-8"))

    def set_direction(self, user_uuid: str, message: str) -> None:
        with context.lock:
            context.set_direction(user_uuid, message)
        self.request.sendall(bytes("OK", "utf-8"))

    def handle(self) -> None:
        data = self.request.recv(1024).strip().decode()
        user_uuid, message = utils_messages.unpack(data)

        if message == GET_WORLD:
            self.send_world_message()
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
