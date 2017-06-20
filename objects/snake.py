from objects.common import Cell, CellStack
from messages import GO_UP, GO_DOWN, GO_RIGHT, GO_LEFT


class SnakeCell(Cell):
    printable_symbol = "#"


class Snake(CellStack):
    def __init__(self, client_uuid, x, y):
        super(Snake, self).__init__()

        self.alive = True

        self.uuid = client_uuid

        c1 = SnakeCell(x, y)
        c1.set_owner(self)

        c2 = SnakeCell(x, y+1)
        c2.set_owner(self)

        c3 = SnakeCell(x, y+2)
        c3.set_owner(self)

        self.add_cell(c1)
        self.add_cell(c2)
        self.add_cell(c3)

    def kill(self):
        print("Snake killed")
        self.alive = False

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

    def grow(self, direction):
        head = self.get_cells()[0]
        x, y = self.get_new_position_from_direction(head, direction)
        self.add_cell(SnakeCell(x, y))

    def do(self, direction):
        self.move(direction)
