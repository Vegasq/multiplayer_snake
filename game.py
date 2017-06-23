import time
import context
import random
import settings

from typing import List

from objects.common import Cell, CellStack
from objects.empty import Empty
from objects.snake import Snake, SnakeCell
from objects.apple import Apple, AppleCell


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
        for row_number in range(0, settings.rows):
            row = []
            for col_number in range(0, settings.columns):
                row.append(Empty(col_number, row_number))
            self._w.append(row)

    def reset(self):
        self.create()

    # def who_will_die(self, a: Cell, b: Cell) -> List[CellStack]:
    #     if a.hardness == b.hardness:
    #         return [a.get_owner(), b.get_owner()]
    #     elif a.hardness > b.hardness:
    #         return [b.get_owner()]
    #     elif b.hardness > a.hardness:
    #         return [a.get_owner()]

    def update(self, cell_stack):
        for cell in cell_stack.get_cells():

            # print("X:")
            # print(cell.x)
            # print(len(self._w[0]))
            # print(cell.x >= len(self._w[0]))
            #
            # print("")
            #
            # print("Y:")
            # print(cell.y)
            # print(len(self._w))
            # print(cell.y >= len(self._w))

            if (
                cell.x < 0 or cell.y < 0 or
                cell.x >= len(self._w[0]) or cell.y >= len(self._w)
            ):
                cell.get_owner().kill()
                continue

            if self._w[cell.y][cell.x].__class__ != Empty:
                # objs_to_die = self.who_will_die(cell, self._w[cell.y][cell.x])
                # for o in objs_to_die:
                #     o.kill()

                dest_cell = self._w[cell.y][cell.x]

                if (
                    cell.is_head() and  # If we move HEAD
                    dest_cell.__class__ == SnakeCell and  # Over another SNAKE
                    not dest_cell.is_head()  # And it's not head-to-head
                ):
                    cell.get_owner().kill()
                    continue
                elif (
                    cell.is_head() and  # If we move HEAD
                    dest_cell.__class__ == SnakeCell and  # Over another SNAKE
                    dest_cell.is_head()  # And it's head-to-head
                ):
                    cell.get_owner().kill()
                    dest_cell.get_owner().kill()
                    continue
                elif (
                    dest_cell.__class__ == SnakeCell and
                    not cell.is_head() and dest_cell.is_head()
                ):
                    dest_cell.get_owner().kill()
                elif (
                    cell.is_head() and
                    dest_cell.__class__ == AppleCell
                ):
                    cell.get_owner().grow()
                    dest_cell.get_owner().kill()

            self._w[cell.y][cell.x] = cell

    def flush_world(self):
        p_w = []
        for r in self._w:
            p_r = []
            for c in r:
                if hasattr(c, "serialize_cell"):
                    p_r.append(c.serialize_cell())
                else:
                    p_r.append(c.printable_symbol)
            p_w.append(p_r)

        context.world = p_w

        return p_w


class Stack(object):
    def __init__(self) -> None:
        self._snakes = []
        self._apples = []

    def add(self, obj) -> None:
        if obj.__class__ == Snake:
            self._snakes.append(obj)
        elif obj.__class__ == Apple:
            self._apples.append(obj)

    @property
    def all_alive_snakes(self) -> Snake:
        for s in self._snakes:
            if s.alive:
                yield s

    @property
    def all_alive_apples(self) -> Apple:
        for a in self._apples:
            if a.alive:
                yield a

    @property
    def all(self):
        for i in self.all_alive_apples:
            yield i
        for i in self.all_alive_snakes:
            yield i

    @property
    def alive_apples_count(self) -> None:
        return len([a for a in self._apples if a.alive])

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


class Game(object):
    def __init__(self):
        self.stack = Stack()

        self.world = World()
        self.world.create()

    def create_apple(self):
        x, y = self.world.get_empty_position()
        self.stack.add(Apple(x, y))

    def create_snake(self, client_uuid):
        x, y = self.world.get_empty_position()
        self.stack.add(Snake(client_uuid, x, y))

    def loop(self):
        while True:
            if not context.server_alive:
                time.sleep(1)
                print("Waiting for server...")
                continue

            # Create new Snakes at the start of step
            with context.lock:
                for client_uuid in context.clients.keys():
                    if not self.stack.is_snake_exist(client_uuid):
                        self.create_snake(client_uuid)

            # Generate apples
            if self.stack.alive_apples_count < 10:
                self.create_apple()

            # Move snakes
            for snake in self.stack.all_alive_snakes:
                snake.do(context.clients[snake.uuid]["direction"])

            # Empty current world
            self.world.reset()

            # Fill world + collision
            for obj in self.stack.all:
                self.world.update(obj)

            # Dump new map to public
            self.world.flush_world()

            time.sleep(settings.game_speed)
