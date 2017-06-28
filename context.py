import threading
from messages import NEW_CLIENT, GO_UP, GO_DOWN, GO_RIGHT, GO_LEFT, GET_WORLD


lock = threading.Lock()

clients = {}

world = []

server_alive = False


def set_direction(snake_uuid, dest):
    if snake_uuid in clients.keys():
        cdest = clients[snake_uuid]["direction"]

        if cdest in [GO_UP, GO_DOWN] and dest in [GO_UP, GO_DOWN]:
            print("Current dst is %s, new is %s" % (cdest, dest))
        elif cdest in [GO_RIGHT, GO_LEFT] and dest in [GO_RIGHT, GO_LEFT]:
            print("Current dst is %s, new is %s" % (cdest, dest))
        else:
            clients[snake_uuid]["direction"] = dest


def set_head_position(snake_uuid, x, y):
    with lock:
        if snake_uuid in clients.keys():
            clients[snake_uuid]["position"] = (x, y)


def get_head_position(snake_uuid):
    with lock:
        return clients[snake_uuid]["position"]


def is_client_exists(client_uuid):
    if client_uuid in clients.keys():
        return True
    print("Client %s not found in %s" % (client_uuid, clients.keys()))
    return False
