class Cell(object):
    printable_symbol = "?"

    def __init__(self, x, y):
        self._x = x
        self._y = y

        self._alive = True
        self._owner = None

    def set_owner(self, owner):
        self._owner = owner

    def get_owner(self):
        return self._owner

    def __unicode__(self):
        return self.__str__()

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.printable_symbol

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    # @property
    # def position(self):
    #     return self._x, self._y

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


class CellStack(object):
    def __init__(self):
        self._cells = []

    def add_cell(self, cell):
        self._cells.append(cell)

    def get_cells(self):
        return [c for c in self._cells if c.alive]

    def do(self, command):
        raise Exception(command)
