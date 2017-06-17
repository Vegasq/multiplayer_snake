import pprint
import time
import context

from messages import GO_UP, GO_DOWN, GO_RIGHT, GO_LEFT



def get_empty_position():
    return (5, 5)


def get_new_position_from_direction(cell, direction):
    x, y = cell.get_position()
    if direction == GO_UP:
        return x, y + 1
    elif direction == GO_DOWN:
        return x, y - 1
    elif direction == GO_LEFT:
        return x - 1, y
    elif direction == GO_RIGHT:
        return x + 1, y
    return x, y


class Cell(object):
    printable_symbol = "?"

    def __init__(self, x, y):
        self._x = x
        self._y = y

        self._alive = True

    def __unicode__(self):
        return self.__str__()

    def __str__(self):
        return self.printable_symbol

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._x

    @property
    def position(self):
        return (self._x, self._y)

    def set_position(self, x, y):
        self._x = x
        self._y = y

    def get_position(self):
        return self._x, self._y

    def kill(self):
        self._alive = False

    @property
    def alive(self):
        return self._alive


class SnakeCell(Cell):
    printable_symbol = "#"


class CellStack(object):
    def __init__(self):
        self._cells = []

    def add_cell(self, cell):
        self._cells.append(cell)

    def get_cells(self):
        return [c for c in self._cells if c.alive]

    def do(self, command):
        raise Exception(command)


class Empty(Cell):
    printable_symbol = " "


class Apple(CellStack):
    def __init__(self):
        super(Apple, self).__init__()
        c = Cell(**get_empty_position())
        self.add_cell(c)


class Snake(CellStack):
    def __init__(self, client_uuid):
        super(Snake, self).__init__()
        x, y = get_empty_position()
        self.uuid = client_uuid
        self.add_cell(SnakeCell(x, y))
        self.add_cell(SnakeCell(x, y - 1))
        self.add_cell(SnakeCell(x, y - 2))

    def move(self, direction):
        for i, c in enumerate(self.get_cells()):
            if i == 0:
                old_x, old_y = c.get_position()
                new_x, new_y = get_new_position_from_direction(c, direction)
                c.set_position(new_x, new_y)
            else:
                prev = c.get_position()
                c.set_position(old_x, old_y)
                old_x, old_y = prev

    def grow(self, direction):
        head = self.get_cells()[0]
        x, y = get_new_position_from_direction(head, direction)
        self.add_cell(SnakeCell(x, y))

    def do(self, direction):
        self.move(direction)


class World(object):
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
            self._w[cell.y][cell.x] = cell

    def printable(self):
        sw = ""
        for row in self._w:
            sr = ""
            for col in row:
                sr += col.__str__()
            sw += sr + "\n"
        return sw


class Game(object):
    def __init__(self):
        self._snakes = []

        self.world = World()
        self.world.create()

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
        self._snakes.append(Snake(client_uuid))

    def loop(self):
        while True:
            print('Server tick')
            for client_uuid in context.clients.keys():
                if not self.is_snake_exist(client_uuid):
                    self.create_snake(client_uuid)
                snake = self.get_snake_by_uuid(client_uuid)
                snake.do(context.clients[client_uuid]["direction"])

            self.world.reset()
            for snake in self._snakes:
                self.world.update(snake)

            print(self.world.printable())

            time.sleep(1)
