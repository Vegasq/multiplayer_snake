import socketserver
from messages import NEW_CLIENT, GO_UP, GO_DOWN, GO_RIGHT, GO_LEFT, GET_WORLD
import settings
import json
import context


class SnakeServer(socketserver.BaseRequestHandler):
    def unpack_message(self, message):
        message = str(message)
        print("Unpacking %s" % message)
        m = json.loads(message)
        return m["uuid"], m["message"]

    def handle(self):
        data = self.request.recv(1024).strip().decode()

        print("{} wrote:".format(self.client_address[0]))
        print(data)

        user_uuid, message = self.unpack_message(data)

        if message == GET_WORLD:
            self.request.sendall(bytes(json.dumps(context.world), "utf-8"))

        elif message == NEW_CLIENT and user_uuid not in context.clients:
            context.clients[user_uuid] = {"direction": GO_UP}
            self.request.sendall(bytes(data, "utf-8"))

        elif user_uuid in context.clients and message in [GO_UP, GO_DOWN, GO_RIGHT, GO_LEFT]:
            context.clients[user_uuid]["direction"] = message
            self.request.sendall(bytes(data, "utf-8"))

    @staticmethod
    def tcp_server():
        server = socketserver.TCPServer(
            (settings.host, settings.port), SnakeServer)

        try:
            server.serve_forever()
        except KeyboardInterrupt:
            server.shutdown()
