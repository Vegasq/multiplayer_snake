class Cell(object):
    printable_symbol = "?"

    def __init__(self, x, y, hardness=5):
        """
        Initialize a Cell with x and y cordinates and a hardness value

        A hardness value of 0 means that the cell won't be considered for collisions
        A hardness value of 1 means that the cell will always loose.
        A hardness value of 10 means the cell will always win

        A wall might have a hardness value of 10
        An apple might have a hardness value of 1
        A decoritive cell would have a value of 0
        """
        
        assert type(x) == int
        assert type(y) == int
        assert type(hardness) == int
        assert 0 <= hardness <= 10
        
        self._x = x
        self._y = y
        self._hardness = hardness

        self._alive = True
        self._owner = None

        # Color as an RGB tuple
        self.color = (0, 0, 0)

    def set_owner(self, owner):
        self._owner = owner

    def get_owner(self):
        return self._owner

    def get_hardness(self):
        return self._hardness

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

    @property
    def hardness(self):
        return self._hardness

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


class Killable(object):
    alive = True

    def kill(self):
        self.alive = False


class CellStack(object):
    def __init__(self):
        self._cells = []

    def add_cell(self, cell):
        self._cells.append(cell)

    def get_cells(self):
        return [c for c in self._cells if c.alive]

    def do(self, command):
        raise Exception(command)
