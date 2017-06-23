from objects.common import Cell, CellStack, Killable
from messages import GO_UP, GO_DOWN, GO_RIGHT, GO_LEFT
import context
import random
import json


class SnakeCell(Cell):
    printable_symbol = "#"

    def is_head(self):
        snake = self.get_owner()
        if snake.is_head(self):
            return True
        return False

    def serialize_cell(self):
        return {
            "type": "SnakeCell",
            "color": self.get_owner().color,
            "printable_symbol": "#"
        }


class Snake(CellStack, Killable):
    def __init__(self, client_uuid, x, y):
        super(Snake, self).__init__()

        self.uuid = client_uuid

        c1 = SnakeCell(x, y, hardness=4)
        c1.set_owner(self)

        c2 = SnakeCell(x, y+1, hardness=5)
        c2.set_owner(self)

        c3 = SnakeCell(x, y+2, hardness=5)
        c3.set_owner(self)

        c4 = SnakeCell(x, y+3, hardness=5)
        c4.set_owner(self)

        self.add_cell(c1)
        self.add_cell(c2)
        self.add_cell(c3)
        self.add_cell(c4)

        self.color = (random.randint(0, 255),
                      random.randint(64, 255),
                      random.randint(128, 255))

    def get_current_direction(self):
        return context.clients[self.uuid]["direction"]

    def get_head(self):
        return self.get_cells()[0]

    def is_head(self, cell):
        if cell.__class__ != SnakeCell:
            raise Exception("Non snake cell")

        head = self.get_head()
        if cell == head:
            return True

        return False

    def get_new_position_from_direction(self, cell, direction):
        x, y = cell.get_position()
        if direction == GO_UP:
            return x, y - 1
        elif direction == GO_DOWN:
            return x, y + 1
        elif direction == GO_LEFT:
            return x - 1, y
        elif direction == GO_RIGHT:
            return x + 1, y
        return x, y

    def move(self, direction):
        for i, c in enumerate(self.get_cells()):
            if i == 0:
                old_x, old_y = c.get_position()
                new_x, new_y = self.get_new_position_from_direction(
                    c, direction)

                c.set_position(new_x, new_y)
            else:
                prev = c.get_position()
                c.set_position(old_x, old_y)
                old_x, old_y = prev

    def grow(self):
        head = self.get_cells()[0]
        x, y = self.get_new_position_from_direction(
            head, self.get_current_direction())
        c = SnakeCell(x, y, hardness=5)
        c.set_owner(self)
        self.add_cell(c)

    def do(self, direction):
        self.move(direction)
