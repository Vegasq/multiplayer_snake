from messages import NEW_CLIENT, GO_UP, GO_DOWN, GO_RIGHT, GO_LEFT, GET_WORLD


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
