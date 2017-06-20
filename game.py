import time
import context
import random

from objects.empty import Empty
from objects.snake import Snake


class World(object):
    def __init__(self):
        self._w = []

    def get_empty_position(self):
        while True:
            random_x = random.randint(0, len(self._w[0]) - 1)
            random_y = random.randint(0, len(self._w) - 1)

            if self._w[random_y][random_x].__class__ == Empty:
                return random_x, random_y

    def create(self):
        self._w = []
        for row_number in range(0, 10):
            row = []
            for col_number in range(0, 50):
                row.append(Empty(col_number, row_number))
            self._w.append(row)

    def reset(self):
        self.create()

    def update(self, cell_stack):
        for cell in cell_stack.get_cells():

            print("X:")
            print(cell.x)
            print(len(self._w[0]))
            print(cell.x >= len(self._w[0]))

            print("")

            print("Y:")
            print(cell.y)
            print(len(self._w))
            print(cell.y >= len(self._w))

            if (
                cell.x < 0 or cell.y < 0 or
                cell.x >= len(self._w[0]) or cell.y >= len(self._w)
            ):
                cell.get_owner().kill()
                continue

            if self._w[cell.y][cell.x].__class__ != Empty:
                cell.get_owner().kill()
                continue

            self._w[cell.y][cell.x] = cell

    def flush_world(self):
        p_w = []
        for r in self._w:
            p_r = []
            for c in r:
                p_r.append(c.printable_symbol)
            p_w.append(p_r)

        context.world = p_w

        return p_w


class Game(object):
    def __init__(self):
        self._snakes = []

        self.world = World()
        self.world.create()

    @property
    def alive_snakes(self):
        for s in self._snakes:
            if s.alive:
                yield s

    def is_snake_exist(self, client_uuid):
        for snake in self._snakes:
            if snake.uuid == client_uuid:
                return True
        return False

    def get_snake_by_uuid(self, client_uuid):
        for snake in self._snakes:
            if snake.uuid == client_uuid:
                return snake
        raise Exception("Snake with %s not found." % client_uuid)

    def create_snake(self, client_uuid):
        x, y = self.world.get_empty_position()
        self._snakes.append(Snake(client_uuid, x, y))

    def loop(self):
        while True:
            print('Server tick')
            if not context.server_alive:
                time.sleep(1)
                print("Waiting for server...")
                continue
            print(self._snakes)
            for client_uuid in context.clients.keys():
                if not self.is_snake_exist(client_uuid):
                    self.create_snake(client_uuid)
                snake = self.get_snake_by_uuid(client_uuid)
                if snake.alive:
                    print("We have Snake: %s" % snake)
                    snake.do(context.clients[client_uuid]["direction"])

            self.world.reset()
            for snake in self.alive_snakes:
                print("Update world with %s" % snake)
                self.world.update(snake)

            self.world.flush_world()

            time.sleep(1)
