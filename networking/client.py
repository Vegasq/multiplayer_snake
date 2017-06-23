import socket
import settings

from utils import messages as utils_messages


class Client(object):
    def __init__(self):
        self.uuid = None

    def _read_from_socket(self, sock: socket.socket) -> str:
        buffer = 4096
        data = ""
        while True:
            part = sock.recv(buffer)
            data += part.strip().decode()
            if len(part) < buffer:
                # either 0 or end of data
                break
        return data

    def set_uuid(self, client_uuid: str) -> None:
        self.uuid = client_uuid

    def get_socket(self) -> socket.socket:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((settings.host, settings.port))
        return sock

    def send(self, message: int) -> str:
        sock = self.get_socket()
        sock.sendall(utils_messages.pack(self.uuid, message))
        response = self._read_from_socket(sock)

        sock.close()

        return response
